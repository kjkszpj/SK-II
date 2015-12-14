import socket
from share.config import CONFIG

class SERVER:
    addr = CONFIG.server_addr
    port = CONFIG.server_port

    def __init__(self):
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_UDP)
        self.sk.bind((self.addr, self.port))
        self.sk.listen(2)
        pass


class CLIENT:
    def __init__(self, dconn=None, daddr=None):
        self.conn = dconn
        self.addr = daddr


if __name__ == '__main__':
    server = SERVER()
    while True:
        client = CLIENT(server.sk.accept())
        # todo, move to other THREAD