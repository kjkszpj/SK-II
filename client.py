import socket

server_addr = '127.0.0.1'
port = 2333
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server_addr, port))
s.send('fuck socket')
data = s.recv(1024)
s.close()
print(data)
