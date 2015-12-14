import pyaudio
import wave

import socket


p = pyaudio.PyAudio()
f = wave.open(r"../a.wav", "rb")
stream = p.open(format = p.get_format_from_width(f.getsampwidth()),
				channels = f.getnchannels(),
				rate = f.getframerate(),
				output = True)

server_addr = '127.0.0.1'
port = 2333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_addr, port))
s.send(b'fuck socket')
data = s.recv(1024)
while len(data) != 0:
    # print(len(data))
    data = s.recv(1024)
    stream.write(data)
print(data)
s.close()
