"""
setup.py - Quick setup helper for Smart Book Q&A Crew

This script helps you set up the project quickly.
Run this first before using the app.
"""

import os
import sys


def check_python_version():
    """Check if Python version is 3.10 or higher."""
    if sys.version_info < (3, 10):
        print("❌ Error: Python 3.10 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def check_env_file():
    """Check if .env file exists."""
    if os.path.exists(".env"):
        print("✅ .env file found")
        
        # Check if API key is configured
        with open(".env", "r") as f:
            content = f.read()
            if "GOOGLE_API_KEY=" in content and "your_api_key_here" not in content:
                print("✅ Google API Key appears to be configured")
                return True
            else:
                print("⚠️  .env file exists but API key may not be set correctly")
                print("   Please edit .env and add your Google Gemini API key")
                return False
    else:
        print("⚠️  .env file not found")
        print("   Creating .env from .env.example...")
        if os.path.exists(".env.example"):
            import shutil
            shutil.copy(".env.example", ".env")
            print("✅ Created .env file")
            print("   ⚠️  IMPORTANT: Edit .env and add your Google Gemini API key")
            print("   Get your free API key from: https://aistudio.google.com/apikey")
            return False
        else:
            print("❌ .env.example not found either")
            return False


def check_dependencies():
    """Check if required packages are installed."""
    required_packages = [
        "streamlit",
        "crewai",
        "langchain",
        "langchain_chroma",
        "langchain_google_genai",
        "chromadb",
        "pypdf",
        "python_dotenv"
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All required packages are installed")
        return True


def check_docs_folder():
    """Check if docs folder exists."""
    if os.path.exists("docs"):
        doc_files = [f for f in os.listdir("docs") if f.endswith(('.pdf', '.txt'))]
        if doc_files:
            print(f"✅ docs/ folder found with {len(doc_files)} document(s)")
        else:
            print("ℹ️  docs/ folder exists but is empty")
            print("   You can upload documents through the web interface")
    else:
        print("ℹ️  docs/ folder will be created when you upload documents")
    
    return True


def main():
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
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 60)
    
    if all(results):
        print("✅ Everything looks good!")
        print("\nYou can now run the Streamlit app:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some issues need attention (see above)")
        print("\nTo fix missing dependencies:")
        print("   pip install -r requirements.txt")
        print("\nTo get your API key:")
        print("   1. Go to: https://aistudio.google.com/apikey")
        print("   2. Sign in with Google")
        print("   3. Click 'Create API Key'")
        print("   4. Copy the key to your .env file")
    
    print("=" * 60)


if __name__ == "__main__":
    main()
