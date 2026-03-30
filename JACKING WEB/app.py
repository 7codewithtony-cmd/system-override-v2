from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import os

app = Flask(__name__)

# Base directory jahan app.py hai
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

stats = {
    "hits": 0,
    "bad": 0,
    "active_script": "None"
}

active_processes = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/update_stats', methods=['POST'])
def update_stats():
    global stats
    data = request.json
    if not data: return jsonify({"status": "error"})
    
    stat_type = data.get('type')
    if stat_type == 'hit': stats['hits'] += 1
    elif stat_type == 'bad': stats['bad'] += 1
    return jsonify({"status": "updated", "hits": stats['hits'], "bad": stats['bad']})

@app.route('/get_stats')
def get_stats():
    return jsonify(stats)

@app.route('/start', methods=['POST'])
def start_script():
    global stats, active_processes
    data = request.json
    script_id = data.get('script')
    user_id = data.get('id')
    user_token = data.get('token')

    if not user_id or not user_token:
        return jsonify({"status": "error", "message": "ID/Token Required!"})

    # GitHub par jo file names hain, unse exact match kiya gaya hai
    file_map = {
        "legacy": "peter_legacy_perma.py",
        "meta": "peter_meta_bizz.py",
        "toxic": "peter_toxic_active.py",
        "deep": "peter_deep_perma.py",
        "btn1": "high followers 😍 by peter (2).py",
        "btn3": "high followers file  by team tx.py",
        "btn_2k14": "2k14 to 2k15 file.py",
        "btn_5l": "5L by Peter .py",
        "btn_2k13": "2k13 to 2k15 by peter.py.py"
    }
    
    file_name = file_map.get(script_id)
    
    if file_name:
        # File check: Direct root folder mein check karega
        script_path = os.path.join(BASE_DIR, file_name)

        if not os.path.exists(script_path):
             return jsonify({"status": "error", "message": f"File '{file_name}' nahi mili!"})

        stats["active_script"] = file_name
        
        def run_proc():
            try:
                # Python command se file run hogi
                proc = subprocess.Popen(['python3', script_path, user_id, user_token])
                active_processes.append(proc)
                proc.wait() 
            except Exception as e:
                print(f"Error: {str(e)}")

        threading.Thread(target=run_proc, daemon=True).start()
        return jsonify({"status": "started", "message": f"{file_name} Started!"})
    
    return jsonify({"status": "error", "message": "Script mapping missing!"})

@app.route('/stop', methods=['POST'])
def stop_scripts():
    global active_processes, stats
    count = 0
    for proc in active_processes:
        if proc.poll() is None:
            proc.terminate()
            count += 1
    active_processes = []
    stats["active_script"] = "None"
    return jsonify({"status": "stopped", "message": f"Stopped {count} exploits!"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
