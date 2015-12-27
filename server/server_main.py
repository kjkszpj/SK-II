import os
import sys
sys.path.append(os.path.abspath(sys.argv[0])[:-21])

import socket
from share.config import CONFIG
from server.client_handle import CLIENT_HANDLE


# todo, delete issue?
class SERVER_HANDLE:
    config = CONFIG()
    sk = None

    def __init__(self):
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.sk.bind((self.config.server_addr, self.config.server_port))
        self.sk.listen(10)


if __name__ == '__main__':
    server_sk = SERVER_HANDLE()
    cnt = 0
    while True:
        client_sk, _ = server_sk.sk.accept()
        client_th = CLIENT_HANDLE(client_sk)
        client_th.start()
        cnt += 1
        print('Server load: %d' % cnt)