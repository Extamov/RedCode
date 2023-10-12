from json import loads


def parse_func(message):
    if message == b"\xef\xbb\xbf\r\n" or message == b"":
        return {"title": "", "alerts": []}

    data = loads(message)

    if ("id" not in data) or ("title" not in data) or ("data" not in data):
        raise ValueError()

    return {"title": data["title"], "alerts": [{"id": data["id"], "cities": data["data"]}]}
