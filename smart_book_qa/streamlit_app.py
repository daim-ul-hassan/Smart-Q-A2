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
        .hero-greet {
            color: #cfcfcf;
            font-size: 0.95rem;
            margin-bottom: 0.2rem;
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
            margin-bottom: 0;
        }
        .step-wrap {
            max-width: 92%;
        }
        .step-card {
            border: 1px solid #1f1f1f;
            border-radius: 16px;
            padding: 0.8rem 0.95rem;
            background: #0b0b0b;
            min-height: 92px;
        }
        .step-head {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            margin-bottom: 0.35rem;
        }
        .step-icon {
            font-size: 0.9rem;
            line-height: 1;
        }
        .step-title {
            font-size: 0.98rem;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
        }
        .step-text {
            font-size: 0.9rem;
            color: #cfcfcf;
            margin-bottom: 0;
        }
        .reply-box {
            border: 1px solid #232323;
            border-radius: 16px;
            background: #090909;
            padding: 1rem 1.1rem;
        }
        a {
            color: #ffffff !important;
        }
        .stButton > button {
            background: #000000 !important;
            color: #ffffff !important;
            border: 1px solid #2d2d2d !important;
        }
        .stButton > button:hover {
            border-color: #5a5a5a !important;
            color: #ffffff !important;
        }
        .stButton > button:focus {
            color: #ffffff !important;
            box-shadow: none !important;
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
        st.markdown("### User")
        user_name = st.text_input("Name (optional)", placeholder="Enter your name")
        st.caption("Need a key first?")
        st.markdown("[Get a Google Gemini API key](https://aistudio.google.com/apikey)")
        sidebar_api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="Paste your API key here",
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


def intro_greeting(user_name: str) -> str:
    if user_name:
        return f"Welcome, {user_name}."
    return "Welcome."


def clean_answer_text(answer: str) -> str:
    cleaned_lines = []
    for line in answer.splitlines():
        stripped = line.strip()
        lower = stripped.lower()
        if not stripped:
            cleaned_lines.append("")
            continue
        if lower.startswith("--- chunk"):
            continue
        if lower.startswith("[status:"):
            continue
        if "supporting chunk" in lower:
            continue
        if lower.startswith("verdict:"):
            continue
        cleaned_lines.append(line)

    cleaned = "\n".join(cleaned_lines).strip()
    return cleaned or answer.strip()


def step_card(icon: str, title: str, text: str) -> None:
    st.markdown(
        f"""
        <div class="step-wrap">
            <div class="step-card">
                <div class="step-head">
                    <div class="step-icon">{icon}</div>
                    <div class="step-title">{title}</div>
                </div>
                <div class="step-text">{text}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


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
        st.error("Missing API key. Paste your Google Gemini API key in the sidebar to use the app.")
        st.stop()

    st.markdown(
        f"""
        <div class="main-shell">
            <div class="hero-greet">{intro_greeting(user_name)}</div>
            <div class="hero-title">Smart Book Q&amp;A</div>
            <div class="hero-copy">This app helps you upload a PDF or TXT file and ask clear questions about its content.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    step_col_1, step_col_2, step_col_3, spacer_col = st.columns([1, 1, 1, 0.18])
    with step_col_1:
        step_card("&#128196;", "Upload File", "Add the PDF or TXT file you want to ask about.")
    with step_col_2:
        step_card("&#128451;", "Build Vector DB", "Create the searchable index from the uploaded file.")
    with step_col_3:
        step_card("&#10067;", "Enter Your Question", "Ask about the file and get a clear answer back.")
    with spacer_col:
        st.write("")

    st.write("")
    control_col_1, control_col_2 = st.columns([1.05, 0.95], gap="large")

    with control_col_1:
        st.subheader("Upload File")
        uploaded_file = st.file_uploader(
            "Choose a PDF or TXT file",
            type=["pdf", "txt"],
        )

        if st.button("Save File", use_container_width=True):
            if not uploaded_file:
                st.warning("Choose a PDF or TXT file first.")
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
        st.markdown("<div style='height: 2.2rem;'></div>", unsafe_allow_html=True)
        st.subheader("Enter Your Question")
        question = st.text_input(
            "Ask about the uploaded file",
            placeholder="For example: Summarize chapter 1",
        )

        if st.button("Ask PDF", type="primary", use_container_width=True):
            if not question.strip():
                st.warning("Type a question before running the crew.")
            elif not INDEX_DIR.exists():
                st.warning("Build the document index first.")
            else:
                try:
                    with st.spinner("The crew is reading the file and preparing an answer..."):
                        answer = run_crew(question.strip())
                except Exception as error:
                    st.error(f"The crew could not finish the request: {error}")
                else:
                    cleaned_answer = clean_answer_text(answer)
                    st.session_state.answer_text = (
                        f"{greeting_prefix(user_name)}\n\n{cleaned_answer}"
                    )
                    st.success("Answer generated.")

        if st.session_state.answer_text:
            st.markdown("<div class='reply-box'>", unsafe_allow_html=True)
            st.write(st.session_state.answer_text)
            st.markdown("</div>", unsafe_allow_html=True)
