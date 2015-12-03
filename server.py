import socket

server_addr = '127.0.0.1'
port = 2333
root_sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
root_sk.bind((server_addr, port))
root_sk.listen(5)
conn, caddr = root_sk.accept()
while 1:
	data = conn.recv(1024)
	if not data: break
	conn.send(data)
conn.close()
