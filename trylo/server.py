import wave
import socket

chunk = 1024
f = wave.open(r"../a.wav", "rb")

server_addr = '127.0.0.1'
port = 2333
root_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
root_sk.bind((server_addr, port))
root_sk.listen(5)
conn, caddr = root_sk.accept()

data = conn.recv(1024)
print(data)
print(type(data))
if data:
	data = f.readframes(chunk)
	print(data)
	# paly stream
	while len(data) != 0:
		print(len(data))
		conn.send(data)
		data = f.readframes(chunk)
conn.close()
