# Promptly | Craft Your Best Prompt 🚀

**Promptly** is a premium, localized web application designed to take your "imperfect" prompts and optimize them using the **Gemini 2.5 Flash** engine. It provides you with a highly deterministic, effective version of your intent, ready for any AI model.

---

## ✨ Features
- **Local Optimization Engine**: Powered by Gemini API to ensure structured, world-class prompt engineering.
- **Micro-Animations**: A responsive, premium theme with smooth transitions and glassmorphic elements.
- **Voice Recognition**: Tap to speak and have your prompt automatically transcribed and ready for perfection.
- **One-Click Copy**: Optimized prompts are displayed in a clean code block for immediate use.

---

## 🛠️ Tech Stack
- **Backend**: Python / Flask
- **AI Core**: Google Gemini 2.5 SDK (GenAI)
- **Frontend**: Vanilla HTML5, CSS3, & JavaScript
- **Styling**: Strict custom Brand Guidelines (Black, Neon Green, No Round Borders)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.x
- A Google Gemini API Key

### 2. Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/Rohan69-hub/promtly.git
cd promtly
pip install -r requirements.txt
```

### 3. Environment Setup
Create a `.env` file in the root directory and add your API Key:
```env
GEMINI_API_KEY=your_key_here
```

### 4. Run the Engine
```bash
python3 app.py
```
Open your browser and visit `http://localhost:5000` to start crafting.

---

## 🏗️ Architecture
The project follows a strict **SOP (Standard Operating Procedure)** for AI optimization:
1. **Input**: User prompt via Flask API.
2. **Analysis**: Logic routed through `tools/optimize_prompt.py`.
3. **Structured Generation**: Pydantic-mapped JSON response from Gemini.
4. **Display**: Empathetic & firm feedback with the perfected payload.

---
*Built with ❤️ for Prompt Engineers.*
