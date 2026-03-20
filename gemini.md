# Gemini Schema

## Input Shape
```json
{
  "imperfect_prompt": "string (The original, unoptimized prompt from the user)",
  "target_llm": "string (Optional: e.g., 'ChatGPT', 'Claude', 'Gemini')"
}
```

## Output Shape
```json
{
  "perfected_prompt": "string (The highly optimized, ready-to-copy prompt)",
  "friendly_message": "string (A firm yet friendly message understanding the user's intent and explaining the improvements)",
  "status": "string ('success' or 'error')"
}
```

## Maintenance Log
[Empty]

## Rules
- Coding only begins once this Payload shape is confirmed by the user.
- Any change to logic must be recorded in architecture SOPs before the code is updated.
