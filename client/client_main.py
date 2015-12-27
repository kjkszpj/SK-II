import pyaudio
import socket
import random
from share.atp import *
from share.config import CONFIG


class PLAYER:
    pos = None
    player = None
    stream = None
    sk = None
    uid = None
    data_list = None
    did = None
    player_info = None

    def __init__(self, dsk):
        self.sk = dsk
        pass

    # send & player control logic
    def setup(self, did=random.randint(0, 233)):
        # update player on ack package for setup
        msg = ATP()
        msg.head.type = 0
        msg.head.func = 0
        msg.head.uid = self.uid
        msg.head.did = did
        msg.info = 'SETUP'
        socket.socket.sendall(self.sk, msg.tobyte())

    def play(self, pos=0):
        msg = ATP()
        msg.head.type = 0
        msg.head.func = 1
        msg.head.uid = self.uid
        msg.head.did = self.did
        msg.info = tobyte(pos)
        socket.socket.sendall(self.sk, msg.tobyte())
        self.pos = pos
        self.stream = self.player.open(format=self.player.get_format_from_width(self.player_info[0]),
                                       channels=self.player_info[1], rate=self.player_info[2], output=True)

    def pause(self):
        msg = ATP()
        msg.head.type = 0
        msg.head.func = 2
        msg.head.uid = self.uid
        msg.head.did = self.did
        msg.info = 'PAUSE'
        socket.socket.sendall(self.sk, msg.tobyte())
        self.stream.stop_stream()

    def teardown(self):
        msg = ATP()
        msg.head.type = 0
        msg.head.func = 2
        msg.head.uid = self.uid
        msg.head.did = self.did
        msg.info = 'PAUSE'
        socket.socket.sendall(self.sk, msg.tobyte())
        self.stream.stop_stream()
        self.stream.close()

    def login(self, uid=random.randint(0, 233)):
        msg = ATP()
        msg.head.type = 1
        msg.head.func = 0
        self.uid = msg.head.uid = uid
        msg.info = 'LOGIN'
        socket.socket.sendall(self.sk, msg.tobyte())

    def logout(self):
        msg = ATP()
        msg.head.type = 1
        msg.head.type = 1
        msg.head.uid = self.uid
        msg.info = 'LOGOUT'
        socket.socket.sendall(self.sk, msg.tobyte())

    # thread like?
    def run(self):
        while True:
            content = socket.socket.recv(self.sk, CONFIG.head_size)
            temp = HEAD(content)
            if temp.verify():
                if temp.flag == 0:
                    # for now, it is no use
                    pass
                    continue
                elif temp.type == 0:
                    if temp.func == 0:
                        self.shou_setup()
                    elif temp.func == 1:
                        self.shou_play()
                    elif temp.func == 2:
                        self.shou_pause()
                    elif temp.func == 3:
                        self.shou_teardown()
                elif temp.type == 1:
                    if temp.func == 0:
                        self.shou_login()
                    elif temp.func == 1:
                        self.shou_logout()
            else:
                print('Invalid head encounter.')
            pass

    # receive logic
    def shou_setup(self):
        content = read_file(self.sk)
        content = content.encode('utf-8')
        content = content.split(' ')
        self.player = pyaudio.PyAudio()
        self.player_info = (int(content[0]), int(content[1]), int(content[2]))

    def shou_play(self):
        data_len = read_int(self.sk)
        pos = read_int(self.sk)
        content = read_len(self.sk, data_len)
        if pos == self.pos:
            self.stream.write(content)
            self.pos += data_len

    def shou_pause(self):
        pass

    def shou_teardown(self):
        pass

    def shou_login(self):
        content = read_file(self.sk)
        content = content.encode('utf-8')
        self.data_list = content.split(' ')

    def shou_logout(self):
        pass


def init():
    # global sk
    pass


def read_file(sk):
    result = socket.socket.recv(sk, 1)
    while result[-1] != b'\0':
        result = socket.socket.recv(sk, 1)
    return result[:-1]


def read_len(sk, len=1):
    return socket.socket.recv(sk, len)


def read_int(sk):
    result = '0'
    ch = socket.socket.recv(sk, 1).encode('utf-8')
    while ch in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        result = result * 10 + ord(ch) - ord('0')
        ch = socket.socket.recv(sk, 1).encode('utf-8')
    return result


if __name__ == '__main__':
    sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    while True:
        try:
            sk.connect((CONFIG.server_addr, CONFIG.server_port))
        except:
            print('can not connect to server.')
        else:
            break
    p = PLAYER(sk)
