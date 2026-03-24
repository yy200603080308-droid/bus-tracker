import requests
import re
import time

TARGET_BUS = "3043"
WEBHOOK_URL = "https://discord.com/api/webhooks/1485962823250215004/2llIF6XkFAKSvOVZ23ZNABTAqccSXb966k2HyvRJkBI67tDXewx2Jglw-bngzhT7qBuq"

BASE_URL = "https://kyotocity.bus-navigation.jp/wgsys/wgs_kyt/vehiclePosition.htm"

last_seen = None

def send(msg):
    try:
        requests.post(WEBHOOK_URL, json={"content": msg})
    except:
        print("送信失敗")

def get_data():
    try:
        params = {
            "from": "auto",
            "fromType": "1",
            "locale": "ja",
            "fromlat": "35.0",
            "fromlng": "135.75",
            "mapFlag": "true"
        }

        res = requests.get(BASE_URL, params=params)
        data = re.findall(r'(\d{4}:\d+:\d+)', res.text)
        return data
    except:
        print("取得失敗")
        return []

while True:
    data = get_data()

    print("取得データ:", data)

    for item in data:
        print("チェック:", item)

        if TARGET_BUS in item:
            print("一致:", item)

            if last_seen != item:
                print("通知発火")
                send(f"🚌 {TARGET_BUS} 動いた → {item}")
                last_seen = item

    time.sleep(20)
