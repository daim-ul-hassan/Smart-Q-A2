import os
import streamlit as st
from dotenv import load_dotenv
import shutil
from crew import run_crew
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

def get_api_key():
    try:
        if hasattr(st, 'secrets') and 'google' in st.secrets:
            return st.secrets['google']['api_key']
    except Exception:
        pass
    return os.environ.get("GOOGLE_API_KEY", "")

api_key = get_api_key()
if api_key:
    os.environ["GOOGLE_API_KEY"] = api_key
    os.environ["GEMINI_API_KEY"] = api_key

st.set_page_config(page_title="Smart Book Q&A Crew", page_icon="📚", layout="wide")

def save_uploaded_files(uploaded_files):
    os.makedirs("docs", exist_ok=True)
    for f in uploaded_files:
        with open(os.path.join("docs", f.name), "wb") as file:
            file.write(f.getbuffer())

def build_store():
    if not os.path.exists("docs") or not os.listdir("docs"):
        st.error("No documents in docs/ folder.")
        return
    
    progress = st.progress(0)
    all_docs = []
    for f in os.listdir("docs"):
        path = os.path.join("docs", f)
        if f.endswith(".pdf"):
            all_docs.extend(PyPDFLoader(path).load())
        elif f.endswith(".txt"):
            all_docs.extend(TextLoader(path, encoding="utf-8").load())
    
    progress.progress(33)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_docs)
    progress.progress(66)
    
    if os.path.exists("faiss_index"):
        shutil.rmtree("faiss_index")
        
    vector_store = FAISS.from_documents(chunks, GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001"))
    vector_store.save_local("faiss_index")
    progress.progress(100)
    st.success("Vector store ready!")

def main():
    st.title("Smart Book Q&A Crew")
    st.info("This app uses 3 agents: Retriever, Writer, and Checker.")

    st.divider()
    
    st.subheader("1. Document Setup")
    files = st.file_uploader("Upload PDFs or Text files:", type=['pdf', 'txt'], accept_multiple_files=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if files and st.button("💾 Save Files", use_container_width=True):
            save_uploaded_files(files)
            st.success("Files saved successfully!")
    with col2:
        if st.button("⚙️ Build Index", use_container_width=True):
            build_store()

    st.divider()

    st.subheader("2. Ask the Crew")
    q = st.text_input("What would you like to know about the documents?")
    if st.button("🚀 Ask Crew", type="primary"):
        if not q:
            st.warning("Please type a question first.")
        elif os.path.exists("faiss_index"):
            with st.spinner("Agents are researching..."):
                res = run_crew(q)
                st.success("Answer Generated!")
                st.write("### Final Answer")
                st.write(res)
        else:
            st.warning("⚠️ Please build the index first using the button above.")

if __name__ == "__main__":
    main()
