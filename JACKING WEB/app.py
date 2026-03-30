from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import os
import sys

app = Flask(__name__)

# Global variables for stats and configuration
stats = {
    "hits": 0,
    "bad": 0,
    "active_script": "None"
}

user_data = {
    "id": "",
    "token": ""
}

@app.route('/')
def index():
    return render_template('index.html')

# Save ID and Token configuration
@app.route('/save_config', methods=['POST'])
def save_config():
    global user_data
    data = request.json
    user_data["id"] = data.get("id")
    user_data["token"] = data.get("token")
    print(f"[*] Access Granted -> ID: {user_data['id']}")
    return jsonify({"status": "success", "message": "Credentials Secured!"})

# Endpoint to receive stats from running scripts
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

# Send real-time stats to frontend
@app.route('/get_stats')
def get_stats():
    return jsonify(stats)

@app.route('/start', methods=['POST']) # Updated to match index.html fetch
def start_script():
    global user_data, stats
    data = request.json
    script_id = data.get('script')
    user_data["id"] = data.get('id')
    user_data["token"] = data.get('token')

    if not user_data["id"] or not user_data["token"]:
        return jsonify({"status": "error", "message": "ACCESS DENIED: ID/Token Required!"})

    file_map = {
        "btn1": "high followers 😎 by peter (2).py",
        "btn2": "2k14 to 2k15 file.py",
        "btn3": "high followers file  by team tx.py",
        "btn4": "5L by Peter .py",
        "btn5": "2k13 to 2k15 by peter.py.py"
    }
    
    file_to_run = file_map.get(script_id)
    
    if file_to_run:
        stats["active_script"] = file_to_run
        
        def run_proc():
            # Launching script with ID and Token as arguments
            # Use 'python3' for Linux/Render servers, 'python' for local Windows
            python_cmd = 'python3' if os.name != 'nt' else 'python'
            cmd = [python_cmd, file_to_run, user_data["id"], user_data["token"]]
            subprocess.Popen(cmd)

        threading.Thread(target=run_proc).start()
        return jsonify({"status": "started", "message": f"Exploit {script_id} Initiated!"})
    
    return jsonify({"status": "error", "message": "Script not found in directory!"})

if __name__ == '__main__':
    # Detection for Render/Cloud deployment port
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' is mandatory for live servers
    app.run(host='0.0.0.0', port=port, debug=False)