from __future__ import annotations

import os
from pathlib import Path

import streamlit as st

from smart_book_qa.config import DOCS_DIR, INDEX_DIR, configure_llm_api_key, get_api_key
from smart_book_qa.crew import run_crew
from smart_book_qa.indexing import build_vector_store


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #000000;
            color: #ffffff;
        }
        .main-shell {
            border: 1px solid #1f1f1f;
            border-radius: 18px;
            padding: 1.2rem;
            background: linear-gradient(180deg, #050505 0%, #0d0d0d 100%);
        }
        .hero-title {
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            color: #ffffff;
        }
        .hero-copy {
            color: #d8d8d8;
            font-size: 1rem;
            margin-bottom: 0.3rem;
        }
        .hero-flow {
            color: #ffffff;
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 0;
        }
        .step-card {
            border: 1px solid #1f1f1f;
            border-radius: 16px;
            padding: 0.85rem 1rem;
            background: #0b0b0b;
            min-height: 96px;
        }
        .step-icon {
            font-size: 0.95rem;
            margin-bottom: 0.25rem;
        }
        .step-title {
            font-size: 1rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.15rem;
        }
        .step-text {
            font-size: 0.92rem;
            color: #cfcfcf;
            margin-bottom: 0;
        }
        .reply-box {
            border: 1px solid #232323;
            border-radius: 16px;
            background: #090909;
            padding: 1rem 1.1rem;
        }
        .reply-label {
            color: #d0d0d0;
            font-size: 0.92rem;
            margin-bottom: 0.35rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def save_uploaded_files(uploaded_files: list) -> int:
    DOCS_DIR.mkdir(exist_ok=True)
    saved_count = 0
    for uploaded_file in uploaded_files:
        safe_name = Path(uploaded_file.name).name
        destination = DOCS_DIR / safe_name
        destination.write_bytes(uploaded_file.getbuffer())
        saved_count += 1
    return saved_count


def sidebar_settings() -> str:
    with st.sidebar:
        st.markdown("### Student")
        user_name = st.text_input("Name (optional)", placeholder="Enter your name")
        sidebar_api_key = st.text_input(
            "🔑 API Key",
            type="password",
            placeholder="Paste only if not using .env or secrets",
        )
        if sidebar_api_key.strip():
            st.session_state.api_key_override = sidebar_api_key.strip()

        st.divider()
        st.caption("Flow: Upload -> Vector -> Ask")
        st.caption(f"Docs folder: `{DOCS_DIR.name}/`")
        st.caption(f"Index status: {'Ready' if INDEX_DIR.exists() else 'Not built yet'}")
        st.caption("Storage on Streamlit Cloud is temporary.")

    return user_name.strip()


def greeting_prefix(user_name: str) -> str:
    if user_name:
        return f"{user_name}, here is your answer:"
    return "Here is your answer:"


def main() -> None:
    st.set_page_config(
        page_title="Smart Book Q&A Crew",
        page_icon="📚",
        layout="wide",
    )
    apply_theme()

    if "answer_text" not in st.session_state:
        st.session_state.answer_text = ""

    user_name = sidebar_settings()

    if st.session_state.get("api_key_override"):
        api_key = st.session_state["api_key_override"]
        os.environ["GOOGLE_API_KEY"] = api_key
        os.environ["GEMINI_API_KEY"] = api_key

    configure_llm_api_key()

    if not get_api_key():
        st.error(
            "Missing API key. Add `GOOGLE_API_KEY` to `.env` locally or set "
            "`[google].api_key` in Streamlit secrets before using the app."
        )
        st.stop()

    st.markdown(
        """
        <div class="main-shell">
            <div class="hero-title">Smart Book Q&amp;A</div>
            <div class="hero-copy">Upload one PDF, build the vector database, and ask questions from the document.</div>
            <div class="hero-flow">Upload -&gt; Vector -&gt; Ask</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    step_col_1, step_col_2, step_col_3 = st.columns(3)
    with step_col_1:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-icon">&#128196;</div>
                <div class="step-title">Upload PDF</div>
                <div class="step-text">Add the file the student wants to ask about.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with step_col_2:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-icon">&#128451;</div>
                <div class="step-title">Build Vector DB</div>
                <div class="step-text">Create the searchable index from the uploaded file.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with step_col_3:
        st.markdown(
            """
            <div class="step-card">
                <div class="step-icon">&#10067;</div>
                <div class="step-title">Enter Your Question</div>
                <div class="step-text">Ask about the PDF and get a polite answer back.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    control_col_1, control_col_2 = st.columns([1.05, 0.95], gap="large")

    with control_col_1:
        st.subheader("Upload PDF")
        uploaded_file = st.file_uploader(
            "Choose a PDF file",
            type=["pdf"],
        )

        if st.button("Save PDF", use_container_width=True):
            if not uploaded_file:
                st.warning("Choose a PDF file first.")
            else:
                saved_count = save_uploaded_files([uploaded_file])
                st.success(f"Saved {saved_count} file(s) to `{DOCS_DIR.name}/`.")

        existing_docs = sorted(path.name for path in DOCS_DIR.glob("*") if path.is_file())
        if existing_docs:
            st.caption("Available files: " + ", ".join(existing_docs))

        st.subheader("Build Vector DB")
        if st.button("Build Database", use_container_width=True):
            progress_bar = st.progress(0)
            status = st.empty()

            def on_progress(percent: int, message: str) -> None:
                progress_bar.progress(percent)
                status.write(message)

            try:
                build_vector_store(progress_callback=on_progress)
            except Exception as error:
                progress_bar.progress(0)
                status.empty()
                st.error(f"Index build failed: {error}")
            else:
                st.success("Vector database is ready.")

    with control_col_2:
        st.subheader("Enter Your Question")
        question = st.text_input(
            "Ask about the uploaded PDF",
            placeholder="For example: Summarize chapter 1",
        )

        if st.button("Ask PDF", type="primary", use_container_width=True):
            if not question.strip():
                st.warning("Type a question before running the crew.")
            elif not INDEX_DIR.exists():
                st.warning("Build the document index first.")
            else:
                try:
                    with st.spinner("The crew is reading the PDF and preparing an answer..."):
                        answer = run_crew(question.strip())
                except Exception as error:
                    st.error(f"The crew could not finish the request: {error}")
                else:
                    st.session_state.answer_text = (
                        f"{greeting_prefix(user_name)}\n\n{answer}"
                    )
                    st.success("Answer generated.")

        if st.session_state.answer_text:
            st.markdown(
                """
                <div class="reply-box">
                    <div class="reply-label">Polite reply</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(st.session_state.answer_text)
