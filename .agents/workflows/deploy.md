---
description: standard deployment workflow for promptly
---

This workflow ensures that all changes are committed to Git, deployed to the Modal news scraper, and published to the Vercel production environment.

// turbo-all
1. Verify the changes locally by running `python3 app.py` and checking the browser.
2. Stage and commit all changes to Git:
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```
3. Push changes to the main branch:
   ```bash
   git push origin main
   ```
4. Deploy the AI News Scraper to Modal:
   ```bash
   modal deploy tools/modal_news_scraper.py
   ```
5. Deploy the frontend to Vercel production:
   ```bash
   vercel --prod
   ```
