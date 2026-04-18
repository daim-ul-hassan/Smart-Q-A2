from __future__ import annotations

import shutil
from pathlib import Path
from typing import Callable

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from smart_book_qa.config import DOCS_DIR, INDEX_DIR, get_api_key

ProgressCallback = Callable[[int, str], None] | None
EMBEDDING_MODEL = "models/gemini-embedding-001"


def _report(progress_callback: ProgressCallback, percent: int, message: str) -> None:
    if progress_callback:
        progress_callback(percent, message)


def _embeddings() -> GoogleGenerativeAIEmbeddings:
    api_key = get_api_key()
    if not api_key:
        raise ValueError("Google Gemini API key is not configured.")

    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=api_key,
    )


def _load_documents(docs_dir: Path) -> list:
    all_documents = []
    for file_path in sorted(docs_dir.iterdir()):
        if file_path.suffix.lower() == ".pdf":
            all_documents.extend(PyPDFLoader(str(file_path)).load())
        elif file_path.suffix.lower() == ".txt":
            all_documents.extend(TextLoader(str(file_path), encoding="utf-8").load())
    return all_documents


def build_vector_store(
    docs_dir: Path = DOCS_DIR,
    index_dir: Path = INDEX_DIR,
    progress_callback: ProgressCallback = None,
) -> FAISS:
    docs_dir.mkdir(exist_ok=True)
    _report(progress_callback, 10, "Loading documents...")

    all_documents = _load_documents(docs_dir)
    if not all_documents:
        raise ValueError("No PDF or TXT files were found in the docs folder.")

    _report(progress_callback, 45, "Splitting documents into chunks...")
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(all_documents)

    if index_dir.exists():
        shutil.rmtree(index_dir)

    _report(progress_callback, 75, "Creating embeddings and saving the index...")
    vector_store = FAISS.from_documents(chunks, _embeddings())
    vector_store.save_local(str(index_dir))

    _report(progress_callback, 100, f"Indexed {len(chunks)} chunks successfully.")
    return vector_store
