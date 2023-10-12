from json import loads


def parse_func(message):
    if message == b'jsonCallback({"alerts": {"items": ]}});':
        return {"title": "", "alerts": []}

    data = loads(message[13:-2])

    if "alerts" not in data or "items" not in data["alerts"]:
        raise ValueError()

    alerts = []

    for alert in data["alerts"]["items"]:
        if "item" not in alert or "guid" not in alert["item"] or "title" not in alert["item"]:
            raise ValueError()
        alerts.append({"id": alert["item"]["guid"], "cities": alert["item"]["title"]})

    return {"title": "אזעקה" if len(alerts) > 0 else "", "alerts": alerts}
