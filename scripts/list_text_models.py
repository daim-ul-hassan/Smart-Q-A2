import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY", ""))

print("Available text models:")
try:
    for model in genai.list_models():
        if "generateContent" in model.supported_generation_methods:
            print(model.name)
except Exception as error:
    print(error)
