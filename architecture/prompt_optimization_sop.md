# Prompt Optimization SOP

## Goal
Transform an `imperfect_prompt` submitted by a user into a highly-optimized, copy-pasteable prompt intended for a target LLM. Return this alongside a firm and friendly explanation of the improvements.

## Inputs
Read from `.tmp/input.json`:
```json
{
  "imperfect_prompt": "string",
  "target_llm": "string (optional)"
}
```

## Logic (The AI Transformation)
1. **System Instruction**: The backend Gemini model must act as an expert prompt engineer. 
2. **Behavioral Constraint**: 
   - Friendly and Empathetic: Validate the user's intent. Let them know we understand what they are trying to achieve. 
   - Firm: Do not compromise the prompt's quality. Be authoritative in providing the final best prompt.
3. **Execution**: The script `tools/optimize_prompt.py` reads the input, passes it to `gemini-2.5-flash`, and forces the model to respond exactly in `gemini.md` JSON format.

## Output Shape
Write to `.tmp/output.json` conforming to `gemini.md` schema:
```json
{
  "perfected_prompt": "string",
  "friendly_message": "string",
  "status": "success | error"
}
```

## Error Handling
- If `GEMINI_API_KEY` is missing, status = error.
- If JSON parsing fails, status = error with the underlying exception message in `friendly_message`.
- If rate limited, exit with error message so the caller knows the service is unavailable.
