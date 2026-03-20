# Project Constitution (claude.md)

## Data schemas
- **Input**: Imperfect prompt text from the UI.
- **Output**: Optimized perfect prompt text, accompanied by a friendly explanation.
- *See `gemini.md` for exact JSON structure.*

## Behavioral rules
1. **Friendly**: Tone must be welcoming and approachable.
2. **Firm**: The system must confidently provide the best prompt without diluting the quality.
3. **Empathetic**: The AI must demonstrate it understands where the user is coming from and their underlying intent.

## Architectural invariants
1. **3-Layer Architecture**: UI/Routing (Navigation), SOPs (Architecture), and Execution Python Scripts (Tools).
2. **Phase Isolation**: Integrations (Dashboard, Database) are delayed; MVP will rely on local state or simple file-based source-of-truth first.
3. **Data-First**: No tool code will be written until data shapes are strictly defined and approved.
