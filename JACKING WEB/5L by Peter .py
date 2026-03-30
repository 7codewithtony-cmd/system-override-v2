import random
import sys
import time
import requests
from colorama import Fore, init
from time import sleep
from datetime import datetime
from threading import Thread

init(autoreset=True)

# ================= FIXED DASHBOARD SYNC LOGIC =================
def send_to_dashboard(stat_type):
    try:
        # 127.0.0.1 Render par kaam nahi karta, isliye Live URL use kar rahe hain
        url = 'https://system-override-v2.onrender.com/update_stats'
        requests.post(url, json={'type': stat_type}, timeout=5) # Timeout 5s rakha hai
    except:
        pass
# =============================================================

# ID & Token Setup (Dashboard Friendly)
if len(sys.argv) > 2:
    id_tg = sys.argv[1]
    token_tg = sys.argv[2]
else:
    id_tg = input("\033[1;36mEnter Telegram ID: ")
    token_tg = input("\033[1;36mEnter Bot Token: ")

def combo(s):
    for ASU in s + '\n':
        sys.stdout.write(ASU)
        sys.stdout.flush()
        sleep(0.005)

# Colors
n = '\033[1;35m'; j = '\033[1;36m'; o = '\033[1;31m'
Z = '\033[1;31m'; X = '\033[1;33m'; F = '\033[2;32m'
C = '\033[2;35m'; W = "\033[1;37m"

banner = j + """ 
████████╗███████╗░█████╗░███╗░░░███╗  
╚══██╔══╝██╔════╝██╔══██╗████╗░████║  
░░░██║░░░█████╗░░███████║██╔████╔██║  
░░░██║░░░██╔══╝░░██╔══██║██║╚██╔╝██║  
░░░██║░░░███████╗██║░░██║██║░╚═╝░██║  
░░░╚═╝░░░╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚═╝  
           5L USERNAME CHECKER - PETER
 """
combo(banner)

insta_chars = "1234567890qwertyuiopasdfghjklzxcvbnm"
all_chars = "qwertyuiopasdfghjkzxcvbnm"

def instaa(user):
    headers = {
        'Host': 'www.instagram.com',
        'x-ig-app-id': '936619743392459',
        'x-ig-www-claim': '0',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'x-requested-with': 'XMLHttpRequest',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'x-csrftoken': 'jzhjt4G11O37lW1aDFyFmy1K0yIEN9Qv',
        'origin': 'https://www.instagram.com',
        'referer': 'https://www.instagram.com/accounts/emailsignup/',
        'cookie': 'csrftoken=jzhjt4G11O37lW1aDFyFmy1K0yIEN9Qv; mid=YtsQ1gABAAEszHB5wT9VqccwQIUL;'
    }
    
    data = f'email={user}test%40gmail.com&username={user}&first_name=&opt_into_one_tap=false'
    
    try:
        url = requests.post('https://www.instagram.com/accounts/web_create_ajax/attempt/', headers=headers, data=data)
        
        if 'feedback_required' in url.text:
            print(W + f" [+] {Z} RATE LIMIT : {X}{user} ")
        elif '"errors": {"username":' in url.text or '"code": "username_is_taken"' in url.text:
            print(W + f" [+] {Z} TAKEN : {X}{user} ")
            send_to_dashboard('bad') 
        else:
            print(W + f" [+] {F} AVAILABLE : {C}{user} ")
            send_to_dashboard('hit') 
            hit_msg = f"━━━━━━━━━━━━━━━\n🚀 5L HIT FOUND!\n👤 USERNAME: {user}\n💀 OWNER: Peter\n━━━━━━━━━━━━━━━"
            requests.post(f'https://api.telegram.org/bot{token_tg}/sendMessage?chat_id={id_tg}&text={hit_msg}')
    except:
        pass

def generate_and_check():
    while True:
        v1 = random.choice(insta_chars)
        v2 = random.choice(insta_chars)
        v3 = random.choice(insta_chars)
        v4 = random.choice(insta_chars)
        v5 = random.choice(all_chars)
        user = v5 + v1 + v2 + v3 + v4
        instaa(user)

if __name__ == "__main__":
    # Render resource limit ke liye 5 threads best hain
    for i in range(5):
        Thread(target=generate_and_check, daemon=True).start()
    
    while True:
        time.sleep(10)
