import modal
import json
import os
from datetime import datetime

# Setup the Modal image with necessary packages
image = modal.Image.debian_slim().pip_install("google-genai", "requests")

app = modal.App("promptly-news-refresher")

@app.function(
    image=image,
    schedule=modal.Period(hours=12),
    secrets=[
        modal.Secret.from_name("gemini-api-key"),
        # You'll need to create a GitHub token secret in Modal to push updates
        modal.Secret.from_name("github-token") 
    ]
)
def refresh_ai_news():
    from google import genai
    from pydantic import BaseModel, Field

    print(f"Refreshing news at {datetime.now()}")

    GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
    GITHUB_TOKEN = os.environ["GITHUB_TOKEN"]
    REPO_NAME = "Rohan69-hub/promtly" # Note: matches your repo name exactly

    client = genai.Client(api_key=GEMINI_API_KEY)

    class NewsItem(BaseModel):
        category: str
        title: str
        snippet: str
        url: str

    class NewsResults(BaseModel):
        news: list[NewsItem]

    # Search for latest AI news using Gemini's knowledge
    prompt = "Get the 6 most groundbreaking AI news stories from the last 24 hours. Categories like Model Releases, Agents, Hardware, etc. Output as JSON."

    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
        config={
            'response_mime_type': 'application/json',
            'response_schema': NewsResults,
        }
    )

    news_data = response.text
    print("New news generated successfully.")

    # Update GitHub via API directly (since it's a small file)
    import requests
    import base64

    api_url = f"https://api.github.com/repos/{REPO_NAME}/contents/static/news.json"
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    # Get the current file's SHA to update it
    get_res = requests.get(api_url, headers=headers)
    sha = get_res.json().get("sha")

    # Push update
    payload = {
        "message": "Automated AI News Refresh via Modal",
        "content": base64.b64encode(news_data.encode()).decode(),
        "sha": sha,
        "branch": "main"
    }

    push_res = requests.put(api_url, headers=headers, json=payload)
    
    if push_res.status_code in [200, 201]:
        print("✅ News successfully pushed to GitHub!")
    else:
        print(f"❌ Failed to push: {push_res.text}")

if __name__ == "__main__":
    # Local test run
    modal.runner.deploy_app(app)
