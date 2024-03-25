import wave
import numpy
import sounddevice

def play_audio(file_name: str):
    with wave.open(file_name, "rb") as wf:
        buffer = wf.readframes(wf.getnframes())
        interleaved = numpy.frombuffer(buffer, dtype=f'int{wf.getsampwidth()*8}')
        data = numpy.reshape(interleaved, (-1, wf.getnchannels()))
        sounddevice.play(data, wf.getframerate(), blocking=False)
