import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY", ""))

print("Available embedding models:")
for model in genai.list_models():
    if "embedContent" in model.supported_generation_methods:
        print(model.name)
