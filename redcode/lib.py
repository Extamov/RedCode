from datetime import datetime
from os import name, system, path
from aiohttp import ClientSession, TCPConnector, ClientTimeout, WSMsgType, ClientConnectionError, WSMessage
from threading import Thread, Timer
from tkinter import ttk, Tk
from time import sleep
from winsound import PlaySound, SND_ASYNC, SND_FILENAME
from importlib import resources
from . import assets

class AlarmWindow:
    def __init__(self):
        self.root_frame = None
        self.label_object = None
        self.texts = []
        Thread(target=self._initialize).start()
        sleep(0.3)

    def _initialize(self):
        self.root_frame = Tk()
        self.root_frame.attributes("-topmost", True)
        self.root_frame.overrideredirect(1)
        self.root_frame.withdraw()

        frm = ttk.Frame(self.root_frame, padding=20)
        frm.grid()
        self.label_object = ttk.Label(frm, text="", font=("Arial", 16))
        self.label_object.grid(column=0, row=0)

        self.root_frame.mainloop()

    def _dequeue(self):
        self.texts.pop(0)
        self.change_text("\n".join(self.texts))

    def add_alarm(self, text, is_progressive):
        if is_progressive:
            self.texts += [text]
            Timer(15, self._dequeue).start()
        else:
            self.texts = [text]
        self.change_text("\n".join(self.texts))

    def change_text(self, new_text):
        old_text = self.label_object.cget("text")
        self.label_object.config(text=new_text)
        self.root_frame.update()
        screen_width = self.root_frame.winfo_screenwidth()
        screen_height = self.root_frame.winfo_screenheight()
        r_width = self.root_frame.winfo_reqwidth()
        r_height = self.root_frame.winfo_reqheight()

        self.root_frame.geometry('%dx%d+%d+%d' % (
            r_width,
            r_height,
            screen_width - r_width - 10,
            screen_height - r_height - 50
        ))

        if old_text != "" and new_text == "":
            self.root_frame.withdraw()
        elif old_text == "" and new_text != "":
            self.root_frame.deiconify()

wind = AlarmWindow()

assets_location = resources.files(assets)

def show_notification(cities, is_progressive):
    if len(cities) > 0:
        print(f"[{datetime.now()}]: {' | '.join(cities) if type(cities) == list else cities}")

    wind.add_alarm("\n".join(cities) if type(cities) == list else cities, is_progressive)

    current_all_cities = set(("\n".join(wind.texts)).split("\n"))
    new_all_cities = set(cities if type(cities) == list else cities.split("\n"))
    if is_progressive or not new_all_cities.issubset(current_all_cities):
        PlaySound(path.join(assets_location, "alert_sound.wav"), SND_FILENAME | SND_ASYNC)

def show_error(msg):
    print(f"Error: {msg}")
    PlaySound(path.join(assets_location, "error.wav"), SND_FILENAME | SND_ASYNC)
    sleep(5)
    exit()

def createAIOSession():
    sess = ClientSession(timeout=ClientTimeout(total=20), connector=TCPConnector(ttl_dns_cache=300), headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    })
    return sess

def messageAutoCheck(message: WSMessage):
    if message.data in [b"\xd0\x00", b"\x00\x00"] or message.type in [WSMsgType.PING, WSMsgType.PONG]:
        return True
    if message.type in [WSMsgType.CLOSED, WSMsgType.ERROR]:
        raise ClientConnectionError()

def clear():
    if name == "nt":
        system("cls")
    else:
        system("clear")