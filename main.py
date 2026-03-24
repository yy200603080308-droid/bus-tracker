import requests
import time

TARGET_BUS = "2973"
WEBHOOK_URL = "https://discord.com/api/webhooks/1485962823250215004/2llIF6XkFAKSvOVZ23ZNABTAqccSXb966k2HyvRJkBI67tDXewx2Jglw-bngzhT7qBuq"

URL = "https://kyotocity.bus-navigation.jp/wgsys/wgs_kyt/updateApproachGuidance.htm"

last_seen = None

headers = {
    "User-Agent": "Mozilla/5.0",
    "X-Requested-With": "XMLHttpRequest",
    "Content-Type": "application/x-www-form-urlencoded"
}

data = {
    "language": "ja",
    "from": "新林公団住宅前",
    "to": "",
    "fromType": "1",
    "toType": "",
    "routeKeys": "10094,10119_10098,10097_10104,10106_10130_9851_9859,9858_10099_10124,10117,10118,10121_10131",
    "fromDisplayPassNo": "6,16_7,7_18,18_6_32_27,28_11_11,11,11,11_18",
    "toDisplayPassNo": "",
    "formerApproachGuidance": "2664:1:1",
    "informationFromTextId": "",
    "informationToTextId": "",
    "routeInfoMessage": "0:false:0:::19700101090000000@0:false:0:::19700101090000000@0:false:0:::19700101090000000@0:false:0:::19700101090000000@0:false:0:::19700101090000000@0:false:0:::19700101090000000@0:false:0:::19700101090000000@0:false:0:::19700101090000000@0:false:0:::19700101090000000@",
    "destinationCd": "W01W05001,W02010002,W03T10012,W08020002,029020003,033033T06,W02020001,W05020011,W08010002",
    "fromSignpoleStringKey": "29690,29690_29690,29690_29690,29690_29690_29691_29691,29691_29691_29691,29691,29691,29691_29691",
    "stopInfoMessage": ""
}

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})
    print("通知:", msg)

while True:
    try:
        res = requests.post(URL, headers=headers, data=data, timeout=5)
        json_data = res.json()

        print("取得:", json_data)

        # JSON全体から検索（まずはこれでOK）
        text = str(json_data)

        if TARGET_BUS in text:
            print("検出:", TARGET_BUS)

            if last_seen != text:
                send(f"🚌 {TARGET_BUS} が接近中！")
                last_seen = text

    except Exception as e:
        print("エラー:", e)

    time.sleep(20)
