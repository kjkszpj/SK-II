import os
import sys
sys.path.append(os.path.abspath(sys.argv[0])[:-21])

import pyaudio
import socket
import random
import threading
from time import sleep
from share.atp import *
from share.config import CONFIG


class PLAYER(threading.Thread):
    pos = None
    player = None
    stream = None
    sk = None
    uid = None
    data_list = None
    did = None
    player_info = None

    def __init__(self, dsk):
        threading.Thread.__init__(self)
        self.sk = dsk
        pass

    # send & player control logic
    def setup(self, did=1):
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
        msg.info = str(pos)
        socket.socket.sendall(self.sk, msg.tobyte())
        self.pos = pos
        self.stream = self.player.open(format=self.player.get_format_from_width(self.player_info[0]),
                                       channels=self.player_info[1], rate=self.player_info[2], output=True)
        self.stream.start_stream()

    def pause(self):
        msg = ATP()
        msg.head.type = 0
        msg.head.func = 2
        msg.head.uid = self.uid
        msg.head.did = self.did
        msg.info = 'PAUSE'
        socket.socket.sendall(self.sk, msg.tobyte())
        self.stream.stop_stream()
        self.stream.is_active()
        self.stream.is_stopped()

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
            print('ready to listen')
            content = socket.socket.recv(self.sk, CONFIG.head_size)
            print(content)
            if len(content) != CONFIG.head_size:
                print('maybe /0? Ignored.')
                continue
            temp = HEAD(bytearray(content))
            print(temp.type, temp.func)
            if temp.verify():
                if temp.flag == 0:
                    # for now, it is no use
                    print('Ignored.')
                    continue
                elif temp.type == 0:
                    if temp.func == 0:
                        self.shou_setup(temp)
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
                elif temp.type == 2:
                    self.shou_error()
            else:
                print('Invalid head encounter.')
            sleep(0.01)
            # input('.')

    # receive logic
    def shou_setup(self, head):
        print('receive setup')
        content = read_file(self.sk)
        content = content.decode('utf-8')
        content = content.split(' ')
        self.pos = 0
        self.did = head.did
        self.player = pyaudio.PyAudio()
        self.player_info = (int(content[0]), int(content[1]), int(content[2]))

    def shou_play(self):
        print('receive play')
        data_len = read_int(self.sk)
        pos = read_int(self.sk)
        print(data_len, pos)
        content = read_len(self.sk, data_len)
        if pos == self.pos:
            if self.stream.is_active():
                self.stream.write(bytes(content))
            else:
                print('already stop!')
            self.pos += 1

    def shou_pause(self):
        print('receive pause')
        pass

    def shou_teardown(self):
        print('receive teardown')
        pass

    def shou_login(self):
        print('receive login')
        content = read_file(self.sk)
        content = content.decode('utf-8')
        self.data_list = content.split(' ')

    def shou_logout(self):
        print('receive logout')
        pass

    def shou_error(self):
        print('receive error')
        content = read_file(self.sk)
        print(content)


def init():
    # global sk
    pass


def read_file(sk):
    result = socket.socket.recv(sk, 1)
    while int(result[-1]) != 0:
        result += socket.socket.recv(sk, 1)
    result = bytearray(result)
    return result[:-1]


def read_len(sk, len=1):
    return bytearray(socket.socket.recv(sk, len+1))[:-1]


def read_int(sk):
    result = 0
    ch = socket.socket.recv(sk, 1).decode('utf-8')
    while ch in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        result = result * 10 + ord(ch) - ord('0')
        ch = socket.socket.recv(sk, 1).decode('utf-8')
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
    p.start()
    print('ready to send')
    p.login()
    sleep(1)
    p.setup()
    sleep(1)
    p.play()
    sleep(1)
    p.pause()
    input('.')
    p.play(p.pos)
    # while True:
    #     order = input('>>>new order\n')
    #     order = int(order)
    #     if order == 0: p.setup()
    #     if order == 1: p.play()
    #     if order == 2: p.pause()
    #     if order == 3: p.teardown()
    #     if order == 10: p.login()
    #     if order == 11: p.logout()
