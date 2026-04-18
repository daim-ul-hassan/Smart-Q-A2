from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
INDEX_DIR = BASE_DIR / "faiss_index"

load_dotenv(BASE_DIR / ".env")


def get_api_key() -> str:
    """Read the Gemini API key from Streamlit secrets or the local environment."""
    try:
        import streamlit as st

        secrets = getattr(st, "secrets", None)
        if secrets and "google" in secrets and "api_key" in secrets["google"]:
            return secrets["google"]["api_key"].strip()
    except Exception:
        pass

    return (
        os.getenv("GOOGLE_API_KEY", "").strip()
        or os.getenv("GEMINI_API_KEY", "").strip()
    )


def configure_llm_api_key() -> str:
    """Expose the key in the environment for CrewAI/LiteLLM."""
    api_key = get_api_key()
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
    return api_key
