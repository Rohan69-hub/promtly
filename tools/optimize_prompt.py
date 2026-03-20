import os
import json
from google import genai
from pydantic import BaseModel, Field

# Load env in case of local dev
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class PromptOptimizationResult(BaseModel):
    perfected_prompt: str = Field(description="The highly optimized, ready-to-copy prompt")
    friendly_message: str = Field(description="A firm yet friendly message understanding the user's intent and explaining the improvements")
    status: str = Field(description="'success' or 'error'")

def run_optimization(imperfect_prompt, target_llm="Any AI"):
    gemini_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_key:
        return {
            "perfected_prompt": "",
            "friendly_message": "Server Error: GEMINI_API_KEY is not set.",
            "status": "error"
        }

    if not imperfect_prompt.strip():
        return {
            "perfected_prompt": "",
            "friendly_message": "The provided prompt was empty. Please provide a prompt to optimize.",
            "status": "error"
        }

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
        
        return json.loads(response.text)

    except Exception as e:
        return {
            "perfected_prompt": "",
            "friendly_message": f"Failed to contact AI service: {str(e)}",
            "status": "error"
        }

if __name__ == "__main__":
    # For local script usage - backward compatibility
    import sys
    input_path = os.path.join(".tmp", "input.json")
    output_path = os.path.join(".tmp", "output.json")
    
    if os.path.exists(input_path):
        with open(input_path, 'r') as f:
            data = json.load(f)
            res = run_optimization(data.get("imperfect_prompt", ""))
            with open(output_path, 'w') as f_out:
                json.dump(res, f_out, indent=2)
