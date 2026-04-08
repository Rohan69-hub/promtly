from google import genai
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

client = genai.Client()
for model in client.models.list():
    if "gemini" in model.name:
        print(model.name)
