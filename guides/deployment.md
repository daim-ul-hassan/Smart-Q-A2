# Streamlit Cloud Deployment

## App Settings

- Repository: your GitHub repo
- Branch: your deployment branch
- Main file path: `app.py`

## Secrets

Add this in Streamlit Cloud app settings:

```toml
[google]
api_key = "your_actual_api_key_here"
```

## Important Notes

- `docs/` and `faiss_index/` are created at runtime.
- Streamlit Cloud storage is temporary, so uploads and indexes may disappear between sessions.
- If you change dependencies or Python runtime, Streamlit Cloud will rebuild the app on the next deploy.

## Local Verification Before Deploying

```bash
pip install -r requirements.txt
streamlit run app.py
```
