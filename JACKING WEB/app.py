from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import os
import sys

app = Flask(__name__)

# Base directory setup to find scripts inside 'JACKING WEB'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Global variables for stats
stats = {
    "hits": 0,
    "bad": 0,
    "active_script": "None"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_stats', methods=['POST'])
def update_stats():
    global stats
    data = request.json
    stat_type = data.get('type')
    if stat_type == 'hit':
        stats['hits'] += 1
    elif stat_type == 'bad':
        stats['bad'] += 1
    return jsonify({"status": "updated", "current_hits": stats['hits']})

@app.route('/get_stats')
def get_stats():
    return jsonify(stats)

@app.route('/start', methods=['POST'])
def start_script():
    global stats
    data = request.json
    script_id = data.get('script')
    user_id = data.get('id')
    user_token = data.get('token')

    if not user_id or not user_token:
        return jsonify({"status": "error", "message": "ID/Token Required!"})

    file_map = {
        "btn1": "high followers 😎 by peter (2).py",
        "btn2": "2k14 to 2k15 file.py",
        "btn3": "high followers file  by team tx.py",
        "btn4": "5L by Peter .py",
        "btn5": "2k13 to 2k15 by peter.py.py"
    }
    
    file_name = file_map.get(script_id)
    
    if file_name:
        script_path = os.path.join(BASE_DIR, file_name)
        stats["active_script"] = file_name
        
        def run_proc():
            python_exe = sys.executable or 'python3'
            try:
                # Running with full absolute path for Render
                subprocess.Popen([python_exe, script_path, user_id, user_token])
            except Exception as e:
                print(f"Error: {str(e)}")

        threading.Thread(target=run_proc, daemon=True).start()
        return jsonify({"status": "started", "message": f"Exploit {script_id} Initiated!"})
    
    return jsonify({"status": "error", "message": "Script not found!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
