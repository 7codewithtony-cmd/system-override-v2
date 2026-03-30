import os, requests, sys, time, re, json, string, random
from threading import Thread, Lock
from user_agent import generate_user_agent as gg

# --- DASHBOARD SYNC ---
def send_to_dashboard(stat_type):
    try: requests.post('https://system-override-v2.onrender.com/update_stats', json={'type': stat_type}, timeout=3)
    except: pass

if len(sys.argv) > 2: ID, TOKEN = sys.argv[1], sys.argv[2]
else: ID = input("ID: "); TOKEN = input("Token: ")

stats_lock = Lock()
hits = 0

def send_hit(user, year="2012-14"):
    msg = f"━━━━━━━━━━━━━━━ 🚀\n🌠 PETER PERMA HIT!\n🛰 USER: {user}\n📅 YEAR: {year}\n📧 EMAIL: {user}@gmail.com\n💀 OWNER: Peter (Team TX)\n━━━━━━━━━━━━━━━"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}")

def worker():
    while True:
        try:
            # Zakir/Cipher Logic: Old UID Ranges
            lsd = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            uid = random.randrange(1000000, 500000000) 
            res = requests.post('https://www.instagram.com/api/graphql', data={'lsd':lsd, 'variables':json.dumps({'id':str(uid)})}, headers={'X-FB-LSD':lsd}).json()
            user = res.get('data',{}).get('user',{}).get('username')
            if user:
                # Gmail check logic here...
                send_hit(user)
                send_to_dashboard('hit')
            else: send_to_dashboard('bad')
        except: time.sleep(1)

for _ in range(15): Thread(target=worker, daemon=True).start()
while True: time.sleep(10)