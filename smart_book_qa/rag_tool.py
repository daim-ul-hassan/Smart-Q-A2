from crewai.tools import tool
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from smart_book_qa.config import INDEX_DIR, get_api_key

EMBEDDING_MODEL = "models/gemini-embedding-001"


def _embeddings() -> GoogleGenerativeAIEmbeddings:
    api_key = get_api_key()
    if not api_key:
        raise ValueError("Google Gemini API key is not configured.")

    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=api_key,
    )


@tool("RAG Search Tool")
def rag_search_tool(query: str) -> str:
    """Search the indexed documents and return the top 3 matching chunks."""
    if not INDEX_DIR.exists():
        return "Error: No vector store found. Build the index from the Streamlit app first."

    vector_store = FAISS.load_local(
        str(INDEX_DIR),
        _embeddings(),
        allow_dangerous_deserialization=True,
    )
    results = vector_store.similarity_search(query, k=3)

    if not results:
        return "No relevant information found in the indexed documents."

    output = ["Here are the top 3 relevant chunks from the document set:"]
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "N/A")
        output.append(
            f"\n--- Chunk {i} (Source: {source}, Page: {page}) ---\n{doc.page_content}"
        )
    return "\n".join(output)
