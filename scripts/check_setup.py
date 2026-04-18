"""Quick project health check for local development."""

import os
import sys
from importlib import import_module
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from smart_book_qa.config import DOCS_DIR


def check_python_version() -> bool:
    if sys.version_info < (3, 11):
        print("Error: Python 3.11 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"OK: Python version {sys.version.split()[0]}")
    return True


def check_env_file() -> bool:
    if os.path.exists(".env"):
        print("OK: .env file found")
        with open(".env", "r", encoding="utf-8") as file:
            lines = file.readlines()
        key_value = ""
        for line in lines:
            if line.startswith("GOOGLE_API_KEY="):
                key_value = line.split("=", 1)[1].strip()
                break
        if key_value:
            print("OK: Google API key appears to be configured")
            return True
        print("Info: .env exists and the API key is blank.")
        print("      Users can paste their own API key in the app sidebar.")
        return True

    if os.path.exists(".streamlit/secrets.toml"):
        print("OK: Streamlit secrets file found")
        return True

    print("Info: no local .env or .streamlit/secrets.toml file found.")
    print("      Users can paste their own API key in the app sidebar.")
    return True


def check_dependencies() -> bool:
    required_modules = [
        "streamlit",
        "crewai",
        "langchain_community",
        "langchain_google_genai",
        "langchain_text_splitters",
        "pypdf",
        "dotenv",
    ]

    missing = []
    for module_name in required_modules:
        try:
            import_module(module_name)
        except ImportError:
            missing.append(module_name)

    if missing:
        print(f"Warning: missing modules: {', '.join(missing)}")
        print("         Run: pip install -r requirements.txt")
        return False

    print("OK: All required packages are installed")
    return True


def check_docs_folder() -> bool:
    if DOCS_DIR.exists():
        doc_files = [f.name for f in DOCS_DIR.iterdir() if f.suffix.lower() in {".pdf", ".txt"}]
        if doc_files:
            print(f"OK: docs/ folder contains {len(doc_files)} document(s)")
        else:
            print("Info: docs/ exists but is empty")
            print("      Upload documents through the Streamlit app when needed.")
    else:
        print("Info: docs/ will be created automatically after your first upload.")
    return True


def main() -> None:
    print("=" * 60)
    print("  Smart Book Q&A Crew - Setup Checker")
    print("=" * 60)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies),
        ("Documents Folder", check_docs_folder),
    ]

    results = []
    for name, check_func in checks:
        print(f"\nChecking {name}...")
        results.append(check_func())

    print("\n" + "=" * 60)

    if all(results):
        print("Everything looks good.")
        print("\nYou can now run the Streamlit app:")
        print("   streamlit run app.py")
    else:
        print("Some items still need attention.")
        print("\nTo fix missing dependencies:")
        print("   pip install -r requirements.txt")
        print("\nTo get your API key:")
        print("   1. Go to: https://aistudio.google.com/apikey")
        print("   2. Sign in with Google")
        print("   3. Click 'Create API Key'")
        print("   4. Paste the key into the app sidebar")

    print("=" * 60)


if __name__ == "__main__":
    main()
