import requests
import time

TARGET_BUS = "2651"
WEBHOOK_URL = "https://discord.com/api/webhooks/1485962823250215004/2llIF6XkFAKSvOVZ23ZNABTAqccSXb966k2HyvRJkBI67tDXewx2Jglw-bngzhT7qBuq"

URL = "https://kyotocity.bus-navigation.jp/wgsys/wgs_kyt/updateApproachGuidance.htm"

last_seen = None

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded"
}

# ★ここ重要（最低限）
data = {
    "from": "新林公団住宅前",
    "fromType": "1",
    "locale": "ja"
}

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})
    print("通知:", msg)

while True:
    try:
        res = requests.post(URL, headers=headers, data=data, timeout=5)
        json_data = res.json()

        print("取得:", json_data)

        # ★ここは後で調整する可能性あり
        text = str(json_data)

        if TARGET_BUS in text:
            print("検出:", TARGET_BUS)

            if last_seen != text:
                send(f"🚌 {TARGET_BUS} 動いた！")
                last_seen = text

    except Exception as e:
        print("エラー:", e)

    time.sleep(20)
