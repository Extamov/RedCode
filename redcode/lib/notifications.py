from datetime import datetime
from .gui import AlarmWindow
from .audio import play_audio, get_audio_data
from importlib import resources
from os import path
from time import sleep
from redcode import assets

assets_location = resources.files(assets)
wind = AlarmWindow()
alarm_audio_data = get_audio_data(path.join(assets_location, "alert_sound.wav"))
error_audio_data = get_audio_data(path.join(assets_location, "error.wav"))

def show_notification(cities, is_progressive):
    current_all_cities = set(("\n".join(wind.texts)).split("\n"))
    new_all_cities = set(cities if isinstance(cities, list) else cities.split("\n"))

    wind.add_alarm("\n".join(cities) if isinstance(cities, list) else cities, is_progressive)

    if (is_progressive or not new_all_cities.issubset(current_all_cities)) and len(cities) > 0:
        print(f"[{datetime.now()}]: {' | '.join(cities) if isinstance(cities, list) else cities}")
        play_audio(alarm_audio_data)

def show_error(msg):
    print(f"Error: {msg}")
    play_audio(error_audio_data)
    sleep(5)
    exit()
