from json import loads


def parse_func(message):
    data = loads(message)

    if "type" in data and data["type"] in ["ANDROID_KEEPALIVE", "LATENCY_TEST_WS", "TEST_LATANCY_WS"]:
        return {"title": "", "alerts": []}

    if "type" in data and data["type"] == "SYSTEM_MESSAGE":
        return {"title": data["data"]["titleHe"], "alerts": [{"id": f"{data["data"]["id"]}_{data["data"]["time"]}", "cities": [data["data"]["bodyHe"]]}]}

    if "data" not in data or "cities" not in data["data"] or "notificationId" not in data["data"]:
        raise ValueError()

    return {"title": "אזעקה", "alerts": [{"id": data["data"]["notificationId"], "cities": data["data"]["cities"]}]}
