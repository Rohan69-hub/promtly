from flask import Flask, request, jsonify
import os
from tools.optimize_prompt import run_optimization

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/optimize', methods=['POST'])
def optimize():
    data = request.json
    imperfect_prompt = data.get('imperfect_prompt', '')
    
    # Run the prompt optimization logic directement as a python import
    result = run_optimization(imperfect_prompt)
    
    return jsonify(result)

if __name__ == '__main__':
    # Running locally for verification
    debug_mode = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug_mode, port=5000)
