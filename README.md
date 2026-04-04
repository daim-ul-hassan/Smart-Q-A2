# 📚 Smart Book Q&A Crew - Streamlit Web App

An AI-powered system where three agents work together like a real research team to read your documents and answer questions about them.

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Your API Key
1. Get a free Google Gemini API key from: https://aistudio.google.com/apikey
2. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
3. Edit `.env` and add your API key:
   ```
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

### Step 3: Run the Streamlit App
```bash
streamlit run app.py
```

The app will automatically open in your web browser at `http://localhost:8501`

---

## 📖 How to Use the Web Interface

### 1. Upload Documents (📤 Tab)
- Click "Upload Documents" in the sidebar
- Select your PDF or TXT files
- Click "Upload Files"
- Your files will be saved to the `docs/` folder

### 2. Build Vector Store (🔧 Tab)
- Click "Build Vector Store" in the sidebar
- Click the "Build Vector Store" button
- Wait for the process to complete (you'll see progress)
- This creates a searchable index of your documents

### 3. Ask Questions (❓ Tab)
- Click "Ask Questions" in the sidebar
- Type your question in the text box
- Click "Ask"
- Watch as the 3-agent crew works together to provide a verified answer!

---

## 🤖 Understanding the 3-Agent System

**Agent 1: Document Retriever** 🔍
- Searches through your documents
- Finds the most relevant paragraphs
- Returns top 3 matching text chunks

**Agent 2: Answer Writer** ✍️
- Takes the retrieved information
- Writes a clear, simple answer
- Only uses facts from the source material

**Agent 3: Quality Checker** ✅
- Verifies every fact in the answer
- Compares against original source chunks
- Confirms accuracy before presenting to you

---

## 🛠️ Alternative: Command Line Usage

If you prefer the command line instead of the web interface:

1. **Build vector store:**
   ```bash
   python rag_setup.py
   ```

2. **Ask questions:**
   ```bash
   python main.py
   ```

---

## ❓ Troubleshooting

**Problem: "No vector store found"**
- Solution: Go to "Build Vector Store" tab and click the build button

**Problem: "API key not configured"**
- Solution: Make sure your `.env` file exists with the correct GOOGLE_API_KEY

**Problem: "No documents found"**
- Solution: Upload documents via the "Upload Documents" tab or add files manually to the `docs/` folder

**Problem: Streamlit won't open in browser**
- Solution: Manually open http://localhost:8501 in your browser

**Problem: Module not found errors**
- Solution: Run `pip install -r requirements.txt` again

---

## 💡 Tips

- Upload multiple related documents for better context
- Ask specific questions for more accurate answers
- The system only knows what's in your uploaded documents
- Rebuild the vector store after adding new documents
- Chat history is saved during your session

---

## 📁 File Structure

```
python_ai/
├── app.py                 # Streamlit web interface (MAIN APP!)
├── rag_setup.py          # Command-line vector store builder
├── rag_tool.py           # Custom RAG search tool
├── main.py               # Command-line Q&A interface
├── requirements.txt      # Python dependencies
├── docs/                 # Put your PDF/TXT files here
├── chroma_db/            # Vector store (auto-created)
├── .env                  # Your API key (create this)
└── .env.example          # Template for .env file
```

---

## 🔧 Tech Stack

- **Python** - Programming language
- **CrewAI** - Multi-agent framework
- **LangChain** - Document processing
- **ChromaDB** - Vector database
- **Google Gemini** - AI model (embeddings + LLM)
- **Streamlit** - Web interface

---

## 🎯 Features

✅ Drag-and-drop document upload  
✅ Visual progress tracking for vector store building  
✅ Interactive Q&A with 3-agent collaboration  
✅ Chat history during session  
✅ Real-time status monitoring  
✅ Beautiful web interface  
✅ Mobile-friendly design  

---

Enjoy your Smart Book Q&A Crew! 📚✨
