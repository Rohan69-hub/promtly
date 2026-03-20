from flask import Flask, request, jsonify
import os
import sys

# Ensure the root directory is in sys.path so we can import 'tools'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools.optimize_prompt import run_optimization

app = Flask(__name__)

@app.route('/')
def root():
    return "API is running. Please use /api/optimize for prompt optimization."

@app.route('/api/optimize', methods=['POST'])
def optimize():
    data = request.json
    imperfect_prompt = data.get('imperfect_prompt', '')
    
    # Run the optimization logic module-to-module
    result = run_optimization(imperfect_prompt)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
