import os
import sys
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from google import genai

def check_connection():
    print("Initializing Link Verification with Google Gemini (google-genai)...")
    
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        print("❌ Error: GEMINI_API_KEY not found in environment.")
        sys.exit(1)
        
    try:
        client = genai.Client(api_key=gemini_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Hello! Reply with "Link Established" if you receive this.'
        )
        print("✅ Success: Received response from Gemini API.")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error connecting to Gemini API: {e}")
        sys.exit(1)

if __name__ == "__main__":
    check_connection()
