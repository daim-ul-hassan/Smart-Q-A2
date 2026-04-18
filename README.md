# Smart Book Q&A Crew

Streamlit app for uploading PDF or TXT files, building a FAISS index, and using a 3-agent CrewAI workflow to answer questions from those documents.

## Run Locally

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` from `.env.example` and add your Gemini key:
```bash
copy .env.example .env
```

3. Start the Streamlit app:
```bash
streamlit run app.py
```

## Streamlit Deployment

- Main file: `app.py`
- Secrets format:
```toml
[google]
api_key = "your_actual_api_key_here"
```
- Extra deployment notes: [guides/deployment.md](guides/deployment.md)

## Project Layout

```text
python_ai/
|-- app.py
|-- smart_book_qa/
|   |-- agents.py
|   |-- config.py
|   |-- crew.py
|   |-- indexing.py
|   |-- rag_tool.py
|   `-- streamlit_app.py
|-- scripts/
|   |-- check_setup.py
|   |-- cli.py
|   |-- list_embedding_models.py
|   `-- list_text_models.py
|-- guides/
|   |-- deployment.md
|   `-- legacy/
|-- docs/
|-- requirements.txt
`-- runtime.txt
```

## Notes

- `docs/` and `faiss_index/` are runtime folders and should not be committed.
- Streamlit Cloud storage is temporary, so uploaded files and indexes can disappear between sessions.
- The app now uses one shared configuration and path layer to reduce deployment mistakes.
