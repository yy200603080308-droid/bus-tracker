import requests
import re
import time

TARGET_BUS = "3347"
WEBHOOK_URL = "ここにDiscordのWebhook"

BASE_URL = "https://kyotocity.bus-navigation.jp/wgsys/wgs_kyt/vehiclePosition.htm"

last_seen = None

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})

def get_data():
    params = {
        "from": "auto",
        "fromType": "1",
        "locale": "ja",
        "fromlat": "34.98",
        "fromlng": "135.75",
        "mapFlag": "true"
    }

    res = requests.get(BASE_URL, params=params)
    return re.findall(r'(\d{4}:\d+:\d+)', res.text)

while True:
    data = get_data()

    for item in data:
        if item.startswith(TARGET_BUS):
            global last_seen
            if last_seen != item:
                send(f"🚌 {TARGET_BUS} 動いた → {item}")
                last_seen = item

    time.sleep(20)
