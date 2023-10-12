from json import loads


def parse_func(message):
    data = loads(message)

    if "areas" not in data:
        raise ValueError()

    return {"title": "אזעקה", "alerts": [{"id": data["pikudid"], "cities": data["areas"]}]}
