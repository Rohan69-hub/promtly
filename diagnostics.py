from google import genai
import os
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

client = genai.Client()
results = {}

models_to_test = [
    'gemini-2.5-flash',
    'gemini-1.5-flash',
    'gemini-1.5-pro',
    'gemini-pro',
    'gemini-2.0-flash',
    'gemini-2.0-flash-lite-001'
]

for m in models_to_test:
    try:
        print(f"Testing {m}...")
        client.models.generate_content(model=m, contents='Hi')
        results[m] = "WORKS"
        print(f"  {m} OK")
    except Exception as e:
        results[m] = str(e)
        print(f"  {m} FAILED")

with open('diagnostics_results.json', 'w') as f:
    json.dump(results, f, indent=2)
