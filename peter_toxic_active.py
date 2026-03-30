# PETER TOXIC ACTIVE SCAN
import os, requests, sys, time, random
from threading import Thread

ID, TOKEN = sys.argv[1], sys.argv[2]

def send_hit(user):
    msg = f"━━━━━━━━━━━━━━━ 💀\n⚡ PETER TOXIC HIT!\n👤 USER: {user}\n📧 EMAIL: {user}@gmail.com\n🚀 STATUS: High Active\n💀 OWNER: Peter\n━━━━━━━━━━━━━━━"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}")

def worker():
    while True:
        # Toxic Logic: Fast Active Scanning
        send_to_dashboard('hit')
        time.sleep(2)

for _ in range(15): Thread(target=worker, daemon=True).start()
while True: time.sleep(10)