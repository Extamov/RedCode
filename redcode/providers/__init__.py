from . import cumta, israelhayom, mako, oref, tzofar, walla, ynet

PROVIDERS = [
    {
        "name": "Cumta",
        "type": "Websocket",
        "displayUrl": "cumta.morhaviv.com",
        "connUrl": "ws://ws.cumta.morhaviv.com:25565/ws",
        "optionalHeaders": {},
        "parseFunc": cumta.parse_func,
        "is_progressive": True,
    },
    {
        "name": "Tzofar",
        "type": "Websocket",
        "displayUrl": "www.tzevaadom.co.il",
        "connUrl": "wss://ws.tzevaadom.co.il:8443/socket?platform=WEB",
        "optionalHeaders": {"Origin": "https://www.tzevaadom.co.il"},
        "parseFunc": tzofar.parse_func,
        "is_progressive": True,
    },
    {
        "name": "Israel Hayom",
        "type": "Firebase Websocket",
        "displayUrl": "www.israelhayom.co.il",
        "connUrl": "wss://redalerts-new-default-rtdb.europe-west1.firebasedatabase.app/.ws?v=5&ns=redalerts-new-default-rtdb",
        "optionalHeaders": {},
        "initFunc": israelhayom.init_func,
        "parseFunc": israelhayom.parse_func,
        "is_progressive": True,
    },
    {
        "name": "Walla",
        "type": "Firebase Websocket",
        "displayUrl": "www.walla.co.il",
        "connUrl": "wss://pikud-a0b24.firebaseio.com/.ws?v=5&ns=pikud-a0b24",
        "optionalHeaders": {},
        "initFunc": walla.init_func,
        "parseFunc": walla.parse_func,
        "is_progressive": False,
    },
    {
        "name": "Ynet",
        "type": "Polling",
        "displayUrl": "www.ynet.co.il",
        "connUrl": "https://alerts.ynet.co.il/alertsRss/YnetPicodeHaorefAlertFiles.js",
        "optionalHeaders": {},
        "parseFunc": ynet.parse_func,
        "is_progressive": True,
    },
    {
        "name": "Oref",
        "type": "Polling",
        "displayUrl": "www.oref.org.il",
        "connUrl": "https://www.oref.org.il/WarningMessages/alert/alerts.json",
        "optionalHeaders": {"Referer": "https://www.oref.org.il/", "X-Requested-With": "XMLHttpRequest"},
        "parseFunc": oref.parse_func,
        "is_progressive": False,
    },
    {
        "name": "Mako",
        "type": "Polling",
        "displayUrl": "www.mako.co.il",
        "connUrl": "https://www.mako.co.il/Collab/amudanan/alerts.json",
        "optionalHeaders": {},
        "parseFunc": mako.parse_func,
        "is_progressive": False,
    },
]