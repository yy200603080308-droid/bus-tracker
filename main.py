import requests
import re
import time

URL = "https://kyotocity.bus-navigation.jp/wgsys/wgs_kyt/vehiclePosition.htm?tabName=vehiclePosition&selectedLandmarkCatCd=&from=%E6%96%B0%E6%9E%97%E5%85%AC%E5%9B%A3%E4%BD%8F%E5%AE%85%E5%89%8D&fromType=1&to=&toType=&locale=ja&fromlat=34.966261&fromlng=135.670186&tolat=&tolng=&fromSignpoleKey=&routeLayoutCd=&bsid=1&fromBusStopCd=&toBusStopCd=&mapFlag=true&existYn=&routeKey=&nextDiagramFlag=&diaRevisedDate=&timeTableDirevtionCd=&searchDate=&searchTime=&fromBusStopKey=&toBusStopKey=&lineSelected=&targetTabName=mapSearchTab&informationTextId=&busStopName=%E6%96%B0%E6%9E%97%E5%85%AC%E5%9B%A3%E4%BD%8F%E5%AE%85%E5%89%8D&search_map_from=&search_map_to=&routeKeys=9834_9849_9856%2C9857_10094%2C10119_10098%2C10097_10130_9833_9851_9859%2C9858_10095&fromDisplayPassNo=28_6_5%2C5_6%2C16_7%2C7_6_2_32_27%2C28_11&toDisplayPassNo=&routeKeynum=10&busCode=&formerApproachLat=&formerApproachLng=&formerApproachGuidance=3637%3A5%3A1%402973%3A3%3A1%401746%3A4%3A1&informationFromTextId=&informationToTextId=&informationRouteId=&busstopCdnum=&autoRefreshTime=&vehicleScrollPosition=&destinationCd=023020003%2C029010001%2C033033T01%2CW01W05001%2CW02010002%2CW08020002%2C023010001%2C029020003%2C033033T06%2CW01020001&fromSignpoleStringKey=29690_29690_29690%2C29690_29690%2C29690_29690%2C29690_29690_29691_29691_29691%2C29691_29691&routeSelectNo=0"

TARGET_BUS = "2973"
WEBHOOK_URL = "https://discord.com/api/webhooks/1485962823250215004/2llIF6XkFAKSvOVZ23ZNABTAqccSXb966k2HyvRJkBI67tDXewx2Jglw-bngzhT7qBuq"

last_seen = None

def send(msg):
    requests.post(WEBHOOK_URL, json={"content": msg})
    print("通知:", msg)

def get_buses():
    try:
        res = requests.get(URL, timeout=5)
        text = res.text

        # ★ここがポイント
        match = re.search(r'formerApproachGuidance=([^"&]+)', text)

        if match:
            raw = match.group(1)
            buses = raw.split("@")
            return buses

        return []

    except Exception as e:
        print("取得エラー:", e)
        return []

while True:
    buses = get_buses()

    print("取得:", buses)

    for bus in buses:
        if TARGET_BUS in bus:
            print("検出:", bus)

            if last_seen != bus:
                send(f"🚌 {TARGET_BUS} 動いた → {bus}")
                last_seen = bus

    time.sleep(20)
