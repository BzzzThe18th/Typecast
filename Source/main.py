import wave
import time
import pyaudio
import keyboard
from contextlib import closing
from urllib.parse import quote
from urllib.request import urlopen

rawInput = ""
deviceId = 0

with open('deviceid.txt') as f:
    deviceId = int(f.readlines()[0])

while True:
    player = None
    def playwav(path_or_file):
        global player
        if player is None:
            player = pyaudio.PyAudio()
        with closing(wave.open(path_or_file, 'rb')) as wavfile, \
            closing(player.open(
                format=player.get_format_from_width(wavfile.getsampwidth()),
                channels=wavfile.getnchannels(),
                rate=wavfile.getframerate(),
                output=True,
                output_device_index=deviceId)) as stream:
            while True:
                data = wavfile.readframes(1024)
                if not data:
                    break
                stream.write(data)
    
    key = keyboard.read_key()
    
    if (keyboard.is_pressed('alt') and keyboard.is_pressed('shift')):
        if (key != ('alt' or 'shift')):
            if (key == 'space'):
                key = " "
            if (key == 'shift' or key == 'alt'):
                key = ""
            if (key == 'backspace'):
                key = ""
                rawInput = rawInput[:-1]
            if (key == 'enter'):
                key = ""
                text = quote(rawInput, safe='/', encoding=None, errors=None)
                playwav(urlopen('http://localhost:5500/api/tts?voice=espeak%3Aen&text={text}&vocoder=high&denoiserStrength=0.03&cache=false'
                            ''.format(**vars())))
                rawInput = ""
            if (key != ""):
                rawInput += key.lower()
                print (rawInput)
                time.sleep(0.16)