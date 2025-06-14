import os
import sys
from aiohttp import WSMsgType, ClientConnectionError, WSMessage

def message_ping_check(message: WSMessage):
    if (message.data in [b"\xd0\x00", b"\x00\x00", b""] and message.type == WSMsgType.BINARY) or message.type in [WSMsgType.PING, WSMsgType.PONG]:
        return True
    if message.type in [WSMsgType.CLOSED, WSMsgType.ERROR]:
        raise ClientConnectionError()

def clear_terminal():
    if sys.platform in ["win32", "cygwin", "msys"]:
        os.system("cls")
    else:
        os.system("clear")

def set_terminal_title(text: str):
    if sys.platform in ["win32", "cygwin", "msys"]:
        os.system(f"title {text}")
    else:
        sys.stdout.write(f"\x1b]2;{text}\x07")