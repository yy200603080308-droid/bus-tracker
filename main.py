import requests
import re
import time

TARGET_BUS = "2973"  # ←あとで変えてOK
WEBHOOK_URL = "https://discord.com/api/webhooks/1485962823250215004/2llIF6XkFAKSvOVZ23ZNABTAqccSXb966k2HyvRJkBI67tDXewx2Jglw-bngzhT7qBuq"

BASE_URL = "https://kyotocity.bus-navigation.jp/wgsys/wgs_kyt/vehiclePosition.htm"

last_seen = None

def send(msg):
    try:
        requests.post(WEBHOOK_URL, json={"content": msg}, timeout=5)
        print("通知送信:", msg)
    except Exception as e:
        print("送信エラー:", e)

def get_data():
    buses = []

    coords = [
        ("34.95", "135.70"),
        ("35.00", "135.75"),
        ("35.05", "135.80"),
    ]

    for lat, lng in coords:
        try:
            params = {
                "from": "auto",
                "fromType": "1",
                "locale": "ja",
                "fromlat": lat,
                "fromlng": lng,
                "mapFlag": "true"
            }

            res = requests.get(BASE_URL, params=params, timeout=5)
            found = re.findall(r'(\d{4}:\d+:\d+)', res.text)

            print(f"{lat},{lng} → {found}")
            buses += found

        except Exception as e:
            print("取得エラー:", e)

    return list(set(buses))

while True:
    data = get_data()

    print("まとめ:", data)

    for item in data:
        if TARGET_BUS in item:
            print("検出:", item)

            if last_seen != item:
                send(f"🚌 {TARGET_BUS} 動いた → {item}")
                last_seen = item

    time.sleep(20)
