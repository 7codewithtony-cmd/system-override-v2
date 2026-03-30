# PETER DEEP PERMA SCANNER
import os, requests, sys, time, random
from threading import Thread

ID, TOKEN = sys.argv[1], sys.argv[2]

def send_hit(user):
    msg = f"━━━━━━━━━━━━━━━ 🌌\n🌀 PETER DEEP PERMA!\n👤 USER: {user}\n📅 YEAR: 2012 Deep\n📧 EMAIL: {user}@gmail.com\n💀 OWNER: Peter\n━━━━━━━━━━━━━━━"
    requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={ID}&text={msg}")

# Deep UID Scanning logic...
for _ in range(10): Thread(target=lambda: print("Deep Scan Running..."), daemon=True).start()
while True: time.sleep(10)