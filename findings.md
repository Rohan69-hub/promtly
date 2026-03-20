# Findings

## Research
- Searched for existing prompt builder tools. Noteworthy open-source projects include: `meta-llama/prompt-ops` (for Llama model optimization), `automl/promptolution` (modular framework for optimization), `AIDotNet/auto-prompt`, and `Siddhesh2377/structured-prompt-builder` (browser-first with Gemini). 
- **Application**: These tools highlight the importance of structured prompt construction and iterative improvement algorithms, which validates our approach of "perfecting" the prompt behind the scenes using AI-driven refinement.

## Discoveries
- **North Star**: A web app that takes imperfect user prompts and returns "perfect" prompts for LLMs (ChatGPT, Claude, etc.).
- **Source of Truth**: Currently within the website/local. Database and dashboard will be tackled in a later phase.
- **Delivery**: The perfect prompt is returned directly to the user in a chat-like interface.

## Constraints
- **Integrations**: Deferred to a later stage.
- **UX/Behavior**: Interface must act friendly, firm, and understanding of the user's intent. It must simulate a short "thinking" phase before returning the prompt to feel like a powerful AI chatbot.
- **UI Design**: Must follow provided Design Guidelines. Instead of 'anwar', the landing page should greet the user specifically with: "hi there, lets craft your best promt".
- **Deployment**: Keep it strictly to localhost for now; do not deploy as a public website.
