from json import loads


def parse_func(message):
    data = loads(message)

    if ("id" not in data) or ("data" not in data):
        raise ValueError()

    if len(data["data"]) == 0:
        return {"title": "", "alerts": []}

    return {"title": data["title"], "alerts": [{"id": data["id"], "cities": data["data"]}]}
