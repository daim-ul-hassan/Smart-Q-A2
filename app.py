import os
import streamlit as st
from dotenv import load_dotenv
import shutil
from crew import run_crew
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

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
    
    if os.path.exists("chroma_db"):
        shutil.rmtree("chroma_db")
        
    Chroma.from_documents(chunks, GoogleGenerativeAIEmbeddings(model="models/embedding-001"), persist_directory="chroma_db")
    progress.progress(100)
    st.success("Vector store ready!")

def main():
    st.title("Smart Book Q&A Crew")
    page = st.sidebar.radio("Menu", ["Home", "Upload", "Build Index", "Ask"])

    if page == "Home":
        st.info("This app uses 3 agents: Retriever, Writer, and Checker.")
    elif page == "Upload":
        files = st.file_uploader("Upload PDFs/TXT", type=['pdf', 'txt'], accept_multiple_files=True)
        if files and st.button("Save Files"):
            save_uploaded_files(files)
            st.success("Files saved to docs/")
    elif page == "Build Index":
        if st.button("Index Documents"):
            build_store()
    elif page == "Ask":
        q = st.text_input("Question:")
        if st.button("Ask Crew"):
            if os.path.exists("chroma_db"):
                with st.spinner("Agents are working..."):
                    res = run_crew(q)
                    st.write("**Final Answer:**", res)
            else:
                st.warning("Please build the index first.")

if __name__ == "__main__":
    main()
