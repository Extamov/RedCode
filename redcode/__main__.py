import asyncio
from json import JSONDecodeError
from aiohttp import ClientConnectionError, WSServerHandshakeError, ClientSession, ClientTimeout, TCPConnector
import sys
from .lib.notifications import show_error, show_notification
from .lib.general import clear_terminal, message_ping_check, set_terminal_title
from .providers import PROVIDERS

def create_session():
    sess = ClientSession(timeout=ClientTimeout(total=20), connector=TCPConnector(ttl_dns_cache=300), headers={
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    })
    return sess

async def polling_thread(provider):
    last_alert_ids = []
    session = create_session()
    while True:
        try:
            async with session.get(provider["connUrl"], headers=provider["optionalHeaders"]) as res:
                message = await res.read()
                if res.status != 200:
                    show_error(f"invalid status code ({res.status}), message is '{message}'")

                try:
                    data = provider["parseFunc"](message)
                except JSONDecodeError:
                    show_error(f"failed to parse json, got '{message}'")
                except ValueError:
                    show_error(f"got unexpected data, got '{message}'")

                for alert in data["alerts"]:
                    if alert["id"] not in last_alert_ids:
                        last_alert_ids.append(alert["id"])
                        last_alert_ids = last_alert_ids[-30:]
                        show_notification(alert["cities"], provider["is_progressive"])
                if len(data["alerts"]) == 0 and not provider["is_progressive"]:
                    show_notification([], provider["is_progressive"])
                await asyncio.sleep(0.5)
        except (ClientConnectionError, TimeoutError):
            print("Connection failed, retrying...")
            await asyncio.sleep(1)


async def websocket_thread(provider):
    last_alert_ids = []
    session = create_session()
    while True:
        try:
            async with session.ws_connect(provider["connUrl"], headers=provider["optionalHeaders"], heartbeat=60) as websocket:
                if "initFunc" in provider:
                    await provider["initFunc"](websocket)
                async for message in websocket:
                    if message_ping_check(message):
                        continue

                    try:
                        data = provider["parseFunc"](message.data)
                    except JSONDecodeError:
                        show_error(f"failed to parse json, got '{message}'")
                    except ValueError:
                        show_error(f"got unexpected data, got '{message}'")

                    for alert in data["alerts"]:
                        if alert["id"] not in last_alert_ids:
                            last_alert_ids.append(alert["id"])
                            last_alert_ids = last_alert_ids[-30:]
                            show_notification(alert["cities"], provider["is_progressive"])
                    if len(data["alerts"]) == 0 and not provider["is_progressive"]:
                        show_notification([], provider["is_progressive"])
        except (ClientConnectionError, TimeoutError, WSServerHandshakeError):
            print("Connection failed/forciblly closed, retrying...")
            await asyncio.sleep(1)


async def main():
    ans = ""
    while len(ans) > 3 or not ans.isnumeric() or int(ans) < 0 or int(ans) >= len(PROVIDERS):
        print("Redcode")
        print("=======")
        for index, provider in enumerate(PROVIDERS):
            print(f"[{index}] {provider['name']} [{provider['type']}] [{provider['displayUrl']}]")
        ans = input("Please select provider:")
        clear_terminal()
    provider = PROVIDERS[int(ans)]
    title = f"{provider['name']} [{provider['type']}] [{provider['displayUrl']}]"
    set_terminal_title(title)
    print(title)
    print("=" * len(title))
    if "polling" in provider["type"].lower():
        await polling_thread(provider)
    elif "websocket" in provider["type"].lower():
        await websocket_thread(provider)

def entrypoint():
    # Uses the same event loop policy as unix in windows
    if sys.platform in ["win32", "cygwin", "msys"]:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

if __name__ == "__main__":
    entrypoint()
