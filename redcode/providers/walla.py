from json import loads

async def init_func(conn):
    await conn.send_str('{"t":"d","d":{"r":1,"a":"s","b":{"c":{"sdk.js.9-23-0":1}}}}')
    await conn.send_str('{"t":"d","d":{"r":2,"a":"q","b":{"p":"/alerts","h":""}}}')


def parse_func(message):
    data = loads(message)

    if "d" in data and "d" in data["d"] and "h" in data["d"]["d"] and "ts" in data["d"]["d"] and data["d"]["d"]["h"].endswith("firebaseio.com"):
        return {"title": "FIREBASE_HI", "alerts": []}
    elif "d" in data and "b" in data["d"] and "s" in data["d"]["b"] and data["d"]["b"]["s"] == "ok":
        return {"title": "FIREBASE_OK", "alerts": []}
    elif "d" in data and "b" in data["d"] and "d" in data["d"]["b"] and data["d"]["b"]["d"] is None:
        return {"title": "", "alerts": []}
    elif "d" in data and "b" in data["d"] and "d" in data["d"]["b"] and "p" in data["d"]["b"] and data["d"]["b"]["p"].startswith("alerts"):
        raw_alerts = data["d"]["b"]["d"]
        alerts = []
        titles = set()

        if data["d"]["b"]["p"].startswith("alerts/"):
            raw_alerts = {data["d"]["b"]["p"].replace("alerts/", ""): raw_alerts}

        for (alert_id, alert_data) in raw_alerts.items():
            alerts.append({
                "id": alert_id,
                "cities": [city["polygonName"] for city in alert_data["alerts"]]
            })
            titles.add(alert_data["title"])

        return {"title": ", ".join(titles), "alerts": alerts}
    else:
        raise ValueError()
