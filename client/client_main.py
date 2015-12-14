import socket
from share.config import CONFIG

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_UDP)
    s.connect((CONFIG.server_addr, CONFIG.server_port))
    pass
