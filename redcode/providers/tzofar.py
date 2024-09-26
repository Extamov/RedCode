from json import loads


def parse_func(message):
    data = loads(message)

    if "type" in data and data["type"] in ["ANDROID_KEEPALIVE", "LATENCY_TEST_WS"]:
        return {"title": "", "alerts": []}

    if "data" not in data or "cities" not in data["data"] or "notificationId" not in data["data"]:
        raise ValueError()

    return {"title": "אזעקה", "alerts": [{"id": data["data"]["notificationId"], "cities": data["data"]["cities"]}]}
