# coding=utf-8

import pyaudio
import wave

# define stream chunk
chunk = 1024

# open a wav format music
f = wave.open(r"a.wav", "rb")
# instantiate PyAudio
p = pyaudio.PyAudio()
# open stream
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
				channels = f.getnchannels(),
				rate = f.getframerate(),
				output = True)
# read data
data = f.readframes(chunk)
print(data)

# paly stream
while len(data) != 0:
    stream.write(data)
    print(len(data))
    data = f.readframes(chunk)

print('hello')
n = input()

# stop stream
stream.stop_stream()
stream.close()

# close PyAudio
p.terminate()