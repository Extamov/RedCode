import wave
import numpy
import sounddevice

sounddevice.default.latency = 0.05
sounddevice.default.blocksize = 1

def get_audio_data(file_name: str) -> tuple[numpy.ndarray, int]:
    with wave.open(file_name, "rb") as wf:
        buffer = wf.readframes(wf.getnframes())
        interleaved = numpy.frombuffer(buffer, dtype=f'int{wf.getsampwidth()*8}')
        data = numpy.reshape(interleaved, (-1, wf.getnchannels()))
        return (data, wf.getframerate())

def play_audio(audio_data: tuple[numpy.ndarray, int]):
    sounddevice.play(audio_data[0], audio_data[1], blocking=False)
