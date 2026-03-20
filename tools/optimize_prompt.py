import os
import sys
import json

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from google import genai
from pydantic import BaseModel, Field

# Define the expected output structure globally using Pydantic (compatible with Gemini structured output)
class PromptOptimizationResult(BaseModel):
    perfected_prompt: str = Field(description="The highly optimized, ready-to-copy prompt")
    friendly_message: str = Field(description="A firm yet friendly message understanding the user's intent and explaining the improvements")
    status: str = Field(description="'success' or 'error'")

def optimize_prompt():
    input_path = os.path.join(".tmp", "input.json")
    output_path = os.path.join(".tmp", "output.json")
    
    # Error handling initialization
    error_result = {
        "perfected_prompt": "",
        "friendly_message": "",
        "status": "error"
    }
    
    def write_output(data):
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

    if not os.path.exists(input_path):
        error_result["friendly_message"] = f"Input file not found at {input_path}"
        write_output(error_result)
        sys.exit(1)

    with open(input_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            error_result["friendly_message"] = "Invalid JSON format in input.json"
            write_output(error_result)
            sys.exit(1)

    imperfect_prompt = data.get("imperfect_prompt", "")
    target_llm = data.get("target_llm", "Any AI")

    if not imperfect_prompt.strip():
        error_result["friendly_message"] = "The provided prompt was empty. Please provide a prompt to optimize."
        write_output(error_result)
        sys.exit(0)

    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        error_result["friendly_message"] = "Server Error: GEMINI_API_KEY is not set."
        write_output(error_result)
        sys.exit(1)

    print("Optimizing prompt with Gemini...")
    try:
        client = genai.Client(api_key=gemini_key)
        
        system_instruction = (
            "You are a world-class Prompt Engineer. Your job is to take an imperfect user prompt "
            "and craft the perfect, deterministic, and highly-effective prompt for the target LLM. "
            "CRITICAL RULES:\n"
            "1. You are NOT answering the user's prompt (e.g., you do not retrieve CBSE papers or answer their questions). "
            "2. You are WRITING A SET OF INSTRUCTIONS for the target LLM to execute. "
            "3. Assume the target LLM has FULL CAPABILITIES (internet access, web browsing, file parsing). Do NOT add disclaimers about limitations like 'As an AI I cannot browse'. Your prompt should instruct the LLM to use its browsing tools to find the information. "
            "4. Also, generate a friendly, empathetic, and firm message (friendly_message) explaining what you improved."
        )
        
        user_message_content = f"Target LLM: {target_llm}\nImperfect Prompt: {imperfect_prompt}"
        
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message_content,
            config={
                'system_instruction': system_instruction,
                'response_mime_type': 'application/json',
                'response_schema': PromptOptimizationResult
            }
        )
        
        raw_output = response.text
        # Safety check to ensure parsing works
        final_output = json.loads(raw_output)
        
        write_output(final_output)
        print(f"✅ Optimization complete. See {output_path}")

    except Exception as e:
        error_result["friendly_message"] = f"Failed to contact AI service: {str(e)}"
        write_output(error_result)
        sys.exit(1)

if __name__ == "__main__":
    optimize_prompt()
