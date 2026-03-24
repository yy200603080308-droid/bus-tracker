def get_data():
    buses = []

    coords = [
        ("34.95", "135.70"),
        ("35.00", "135.75"),
        ("35.05", "135.80"),
    ]

    for lat, lng in coords:
        params = {
            "from": "auto",
            "fromType": "1",
            "locale": "ja",
            "fromlat": lat,
            "fromlng": lng,
            "mapFlag": "true"
        }

        res = requests.get(BASE_URL, params=params)
        buses += re.findall(r'(\d{4}:\d+:\d+)', res.text)

    return list(set(buses))
