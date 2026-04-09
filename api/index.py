from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import sys

# Ensure the root directory is in sys.path so we can import 'tools'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.optimize_prompt import run_optimization

app = Flask(__name__)

# ── Security: CORS ────────────────────────────────────────────────────────────
# Only allow requests from our own Vercel deployment.
# Update ALLOWED_ORIGIN if your domain changes.
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN", "https://promptly-xi.vercel.app")
CORS(app, origins=[ALLOWED_ORIGIN], methods=["POST", "OPTIONS"])

# ── Security: Rate Limiting ───────────────────────────────────────────────────
# 10 requests per minute per IP. Adjust as needed.
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"],
    headers_enabled=True  # sends X-RateLimit-* headers to client
)

# ── Constants ─────────────────────────────────────────────────────────────────
MAX_PROMPT_CHARS = 5000  # Hard cap on incoming prompt size


@app.route('/')
def root():
    return "API is running. Please use /api/optimize for prompt optimization."


@app.route('/api/optimize', methods=['POST'])
@limiter.limit("10 per minute")
def optimize():
    # ── Validate Content-Type & body ─────────────────────────────────────────
    data = request.get_json(silent=True)
    if not data or not isinstance(data.get('imperfect_prompt'), str):
        return jsonify({
            "status": "error",
            "friendly_message": "Invalid request. Expected JSON with an 'imperfect_prompt' string."
        }), 400

    # ── Enforce input size cap ────────────────────────────────────────────────
    raw_prompt = data['imperfect_prompt']
    if len(raw_prompt) > MAX_PROMPT_CHARS:
        return jsonify({
            "status": "error",
            "friendly_message": f"Prompt is too long. Please keep it under {MAX_PROMPT_CHARS} characters."
        }), 413

    imperfect_prompt = raw_prompt.strip()
    if len(imperfect_prompt) <= 5:
        return jsonify({
            "status": "error",
            "friendly_message": "Prompt is too short. Please provide more detail."
        }), 400

    # ── Run optimization ──────────────────────────────────────────────────────
    result = run_optimization(imperfect_prompt)
    return jsonify(result)


# ── Rate limit error handler ──────────────────────────────────────────────────
@app.errorhandler(429)
def rate_limit_exceeded(e):
    return jsonify({
        "status": "error",
        "friendly_message": "You're sending requests too fast. Please wait a moment and try again."
    }), 429


if __name__ == '__main__':
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode)
