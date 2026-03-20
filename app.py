from flask import Flask, request, jsonify
import subprocess
import json
import os

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/optimize', methods=['POST'])
def optimize():
    data = request.json
    imperfect_prompt = data.get('imperfect_prompt', '')
    
    # Write to .tmp/input.json for SOP execution model
    os.makedirs('.tmp', exist_ok=True)
    with open('.tmp/input.json', 'w') as f:
        json.dump({"imperfect_prompt": imperfect_prompt}, f)
        
    # Execute the proven script from Phase 3
    result = subprocess.run(['python3', 'tools/optimize_prompt.py'], capture_output=True, text=True)
    
    # Send standardized payload back to browser
    if os.path.exists('.tmp/output.json'):
        with open('.tmp/output.json', 'r') as f:
            output_data = json.load(f)
            return jsonify(output_data)
    else:
        return jsonify({
            "perfected_prompt": "",
            "friendly_message": f"Engine Error: {result.stderr}",
            "status": "error"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
