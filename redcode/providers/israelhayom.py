from json import loads


async def init_func(conn):
    await conn.send_str('{"t":"d","d":{"r":1,"a":"s","b":{"c":{"sdk.js.8-8-1":1}}}}')
    await conn.send_str('{"t":"d","d":{"r":2,"a":"q","b":{"p":"/","h":""}}}')


def parse_func(message):
    data = loads(message)

    if "d" in data and "d" in data["d"] and "h" in data["d"]["d"] and "ts" in data["d"]["d"] and data["d"]["d"]["h"].endswith("firebasedatabase.app"):
        return {"title": "FIREBASE_HI", "alerts": []}
    elif "d" in data and "b" in data["d"] and "s" in data["d"]["b"] and data["d"]["b"]["s"] == "ok":
        return {"title": "FIREBASE_OK", "alerts": []}
    elif "d" in data and "b" in data["d"] and "d" in data["d"]["b"] and data["d"]["b"]["d"] is False:
        return {"title": "", "alerts": []}
    elif "d" in data and "b" in data["d"] and "d" in data["d"]["b"] and "items" in data["d"]["b"]["d"] and "0" in data["d"]["b"]["d"]["items"]:
        info = data["d"]["b"]["d"]
        raw_alerts = info["items"]
        title = info["title"]

        temp_alerts = {}
        for alert_key in raw_alerts.keys():
            alert = raw_alerts[alert_key]
            alert_id = "_".join(alert["pubDate"].values())
            if alert_id not in temp_alerts:
                temp_alerts[alert_id] = []
            temp_alerts[alert_id] += list(alert["title"].values())

        alerts = []
        for (alert_key, alert_cities) in temp_alerts.items():
            alerts.append({"id": alert_key, "cities": alert_cities})

        return {
            "title": title,
            "alerts": alerts,
        }
    else:
        raise ValueError()
