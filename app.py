"""
app.py - Smart Book Q&A Crew with Streamlit Web Interface

This is a complete web application that provides:
1. Document Upload - Upload PDF and TXT files directly through the browser
2. Vector Store Setup - Build the ChromaDB index with visual feedback
3. Q&A Interface - Ask questions and get answers from the 3-agent crew
4. Process Visualization - See how each agent contributes

Run this app with:
    streamlit run app.py
"""

import os
import streamlit as st
from dotenv import load_dotenv
import shutil

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Smart Book Q&A Crew",
    page_icon="📚",
    layout="wide"
)


def save_uploaded_files(uploaded_files, docs_folder="docs"):
    """Save uploaded files to the docs folder."""
    os.makedirs(docs_folder, exist_ok=True)
    
    saved_files = []
    for uploaded_file in uploaded_files:
        file_path = os.path.join(docs_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        saved_files.append(uploaded_file.name)
    
    return saved_files


def check_prerequisites():
    """Check if all prerequisites are met."""
    issues = []
    
    # Check Google API Key
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    if not api_key:
        issues.append("❌ Google API Key not found. Please add it to your .env file.")
    else:
        st.success("✅ Google API Key configured")
    
    # Check if vector store exists
    if os.path.exists("chroma_db"):
        st.success("✅ Vector store found (ChromaDB)")
    else:
        st.warning("⚠️ No vector store found. You need to build it first.")
    
    # Check docs folder
    if os.path.exists("docs") and len(os.listdir("docs")) > 0:
        doc_count = len([f for f in os.listdir("docs") if f.endswith(('.pdf', '.txt'))])
        st.success(f"✅ Found {doc_count} document(s) in docs/ folder")
    else:
        st.warning("⚠️ No documents found in docs/ folder")
    
    return len(issues) == 0, issues


def main():
    # Title and description
    st.title("📚 Smart Book Q&A Crew")
    st.markdown("""
    An AI-powered system where **three agents work together** like a real research team 
    to read your documents and answer questions about them.
    """)
    
    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to:", ["🏠 Home", "📤 Upload Documents", "🔧 Build Vector Store", "❓ Ask Questions"])
    
    # Page routing
    if page == "🏠 Home":
        show_home_page()
    elif page == "📤 Upload Documents":
        show_upload_page()
    elif page == "🔧 Build Vector Store":
        show_build_vector_store_page()
    elif page == "❓ Ask Questions":
        show_qa_page()


def show_home_page():
    """Display the home page with explanation of how the system works."""
    
    st.header("How It Works")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("""
        **Agent 1: Document Retriever** 🔍
        
        Searches the vector store and finds the most relevant text chunks for your question.
        """)
    
    with col2:
        st.info("""
        **Agent 2: Answer Writer** ✍️
        
        Reads the retrieved chunks and writes a clear, accurate answer in simple language.
        """)
    
    with col3:
        st.info("""
        **Agent 3: Quality Checker** ✅
        
        Verifies the answer against the source chunks to ensure accuracy and completeness.
        """)
    
    st.markdown("---")
    
    st.header("System Workflow")
    
    workflow_steps = """
    1. **Upload Documents** → Add your PDF or TXT files
    2. **Build Vector Store** → System processes and indexes your documents
    3. **Ask Questions** → Three agents work together to find and verify answers
    """
    
    st.markdown(workflow_steps)
    
    st.markdown("---")
    
    st.header("Current Status")
    all_good, issues = check_prerequisites()
    
    if issues:
        st.error("**Issues to fix:**")
        for issue in issues:
            st.write(issue)
    
    st.markdown("---")
    
    st.header("Tech Stack")
    tech_info = """
    - **Python** - Programming language
    - **CrewAI** - Multi-agent framework
    - **LangChain** - Document processing
    - **ChromaDB** - Vector database
    - **Google Gemini** - AI model (embeddings + LLM)
    - **Streamlit** - Web interface
    """
    st.markdown(tech_info)


def show_upload_page():
    """Display the document upload page."""
    
    st.header("📤 Upload Documents")
    st.markdown("""
    Upload your PDF or TXT files here. These documents will be processed and indexed 
    so the AI agents can search and answer questions about them.
    """)
    
    # Show current documents
    if os.path.exists("docs"):
        current_docs = [f for f in os.listdir("docs") if f.endswith(('.pdf', '.txt'))]
        if current_docs:
            st.subheader("Current Documents:")
            for doc in current_docs:
                st.write(f"📄 {doc}")
            
            if st.button("🗑️ Clear All Documents", type="secondary"):
                shutil.rmtree("docs")
                os.makedirs("docs", exist_ok=True)
                st.rerun()
    
    st.markdown("---")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Choose PDF or TXT files",
        type=['pdf', 'txt'],
        accept_multiple_files=True,
        help="Select one or more PDF or TXT files to upload"
    )
    
    if uploaded_files:
        st.write(f"**Selected {len(uploaded_files)} file(s):**")
        for f in uploaded_files:
            st.write(f"- {f.name} ({f.size / 1024:.1f} KB)")
        
        if st.button("📥 Upload Files", type="primary"):
            with st.spinner("Uploading files..."):
                saved = save_uploaded_files(uploaded_files)
                st.success(f"✅ Successfully uploaded {len(saved)} file(s)!")
                st.write("Files saved to `docs/` folder:")
                for filename in saved:
                    st.write(f"  - {filename}")
                
                st.info("💡 Next step: Go to **Build Vector Store** to process these documents.")
                st.rerun()


def show_build_vector_store_page():
    """Display the vector store building page."""
    
    st.header("🔧 Build Vector Store")
    st.markdown("""
    This step processes your documents and creates a searchable index (vector store).
    The system will:
    
    1. **Load** all PDF and TXT files from the docs/ folder
    2. **Split** them into small chunks (500 characters each)
    3. **Convert** each chunk into an embedding (numerical representation)
    4. **Store** everything in ChromaDB for fast searching
    
    This only needs to be done **once** per document set.
    """)
    
    # Check prerequisites
    if os.path.exists("docs"):
        doc_count = len([f for f in os.listdir("docs") if f.endswith(('.pdf', '.txt'))])
        st.info(f"Found {doc_count} document(s) ready to process")
    else:
        st.warning("No docs/ folder found. Please upload documents first.")
        return
    
    if st.button("🚀 Build Vector Store", type="primary"):
        build_vector_store_ui()


def build_vector_store_ui():
    """UI version of the build_vector_store function with progress tracking."""
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Import required libraries
        from langchain_community.document_loaders import PyPDFLoader, TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        from langchain_chroma import Chroma
        
        docs_folder = "docs"
        
        # Step 1: Load documents
        status_text.text("Step 1/4: Loading documents...")
        progress_bar.progress(25)
        
        all_documents = []
        for filename in os.listdir(docs_folder):
            file_path = os.path.join(docs_folder, filename)
            
            if filename.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
                all_documents.extend(loader.load())
            elif filename.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
                all_documents.extend(loader.load())
        
        if not all_documents:
            st.error("❌ No documents found! Please add PDF or TXT files to the 'docs/' folder first.")
            return
        
        st.success(f"✅ Loaded {len(all_documents)} pages total")
        
        # Step 2: Split into chunks
        status_text.text("Step 2/4: Splitting documents into chunks...")
        progress_bar.progress(50)
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(all_documents)
        st.success(f"✅ Split into {len(chunks)} chunks")
        
        # Step 3 & 4: Create embeddings and store in ChromaDB
        status_text.text("Step 3/4: Creating embeddings...")
        progress_bar.progress(75)
        
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        status_text.text("Step 4/4: Storing in ChromaDB...")
        vector_store = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory="chroma_db"
        )
        
        progress_bar.progress(100)
        status_text.text("Complete!")
        
        st.success(f"🎉 Vector store ready! Indexed {len(chunks)} chunks.")
        st.info("💡 You can now go to **Ask Questions** to start querying your documents.")
        
    except Exception as e:
        st.error(f"❌ Error building vector store: {str(e)}")
        st.exception(e)


def show_qa_page():
    """Display the Q&A page where users can ask questions."""
    
    st.header("❓ Ask Questions About Your Documents")
    st.markdown("""
    Type your question below and the three-agent crew will work together to find 
    and verify the answer from your uploaded documents.
    """)
    
    # Check if vector store exists
    if not os.path.exists("chroma_db"):
        st.warning("⚠️ No vector store found!")
        st.info("Please go to **Build Vector Store** first to process your documents.")
        return
    
    # Initialize session state for chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Previous Questions:")
        for i, (question, answer) in enumerate(st.session_state.chat_history, 1):
            with st.expander(f"Q{i}: {question}", expanded=False):
                st.markdown("**Answer:**")
                st.write(answer)
    
    st.markdown("---")
    
    # Question input
    question = st.text_input(
        "Your Question:",
        placeholder="e.g., What is the main topic discussed in the document?",
        key="question_input"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        ask_button = st.button("🔍 Ask", type="primary", use_container_width=True)
    
    with col2:
        if st.button("🗑️ Clear History", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    
    if ask_button and question:
        answer_question(question)


def answer_question(question):
    """Process the question using the 3-agent crew and display results."""
    
    with st.spinner("The crew is working on your question..."):
        try:
            # Import crew modules
            from main import run_crew
            
            # Create tabs for different views
            tab1, tab2 = st.tabs(["📋 Final Answer", "🔄 Agent Process"])
            
            with tab1:
                result = run_crew(question)
                
                st.markdown("### Final Verified Answer:")
                st.info(result)
                
                # Save to chat history
                st.session_state.chat_history.append((question, result))
                
                st.success("✅ Answer verified by Quality Checker!")
            
            with tab2:
                st.markdown("### Agent Collaboration Process")
                st.markdown("""
                **What happened behind the scenes:**
                
                1. **Document Retriever** searched the vector store for relevant chunks
                2. **Answer Writer** crafted a clear answer based on the retrieved information
                3. **Quality Checker** verified the answer against the source material
                
                The final answer you see above has been reviewed and verified for accuracy.
                """)
        
        except Exception as e:
            st.error(f"❌ Error processing question: {str(e)}")
            st.exception(e)
            st.info("💡 Make sure you have built the vector store first.")


if __name__ == "__main__":
    main()
