import requests
import re
import time

TARGET_BUS = "2651"
WEBHOOK_URL = "https://discord.com/api/webhooks/1485962823250215004/2llIF6XkFAKSvOVZ23ZNABTAqccSXb966k2HyvRJkBI67tDXewx2Jglw-bngzhT7qBuq"

URL = "https://kyotocity.bus-navigation.jp/wgsys/wgs_kyt/search.htm"

last_seen = None

headers = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://kyotocity.bus-navigation.jp/"
}

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})
    print("通知:", msg)

def get_buses():
    try:
        res = requests.get(URL, headers=headers, timeout=5)
        text = res.text

        # ★ここが核心
        match = re.findall(r'(\d{4}:\d+:\d+)', text)

        print("取得:", match)
        return match

    except Exception as e:
        print("エラー:", e)
        return []

while True:
    buses = get_buses()

    for bus in buses:
        if TARGET_BUS in bus:
            print("検出:", bus)

            if last_seen != bus:
                send(f"🚌 {TARGET_BUS} 動いた → {bus}")
                last_seen = bus

    time.sleep(20)
