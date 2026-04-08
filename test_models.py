from google import genai
import os
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

client = genai.Client()
models_to_test = [
    'gemini-2.0-flash', 
    'gemini-flash-latest', 
    'gemini-pro-latest', 
    'gemini-2.5-pro',
    'gemini-3-flash-preview'
]

for m in models_to_test:
    try:
        print(f"testing {m}...")
        res = client.models.generate_content(model=m, contents='hello')
        print(f'=> {m} works!')
        break
    except Exception as e:
        print(f'=> {m} failed: {e}')
