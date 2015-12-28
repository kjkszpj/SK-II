import socket
import threading
import wave
from time import sleep
from share.atp import *
from share.config import CONFIG
from server.content_control import CONTENT_CONTROL


class CLIENT_HANDLE(threading.Thread):
    sk = None
    data = None
    content = None
    uid = None
    retf = None

    def __init__(self, dconn, retf):
        threading.Thread.__init__(self)
        self.sk = dconn
        self.retf = retf

    def run(self):
        # todo, where to put init of content_control?
        self.content = CONTENT_CONTROL(self.sk)
        self.content.start()
        while True:
            raw_data = self.sk.recv(CONFIG.buffersize)
            if raw_data == b'':
                break
            print(raw_data[:22])
            p = ATP(bytearray(raw_data))
            func = None
            if not p.verify():
                print('---ERROR, package format wrong')
                break
            if p.head.type == 0:
                if p.head.func == 0:      func = self.content.setup
                elif p.head.func == 1:    func = self.content.play
                elif p.head.func == 2:    func = self.content.pause
                elif p.head.func == 3:    func = self.content.teardown
            elif p.head.type == 1:
                if p.head.func == 0:      func = self.login
                if p.head.func == 1:      func = self.logout
            if func(p): break
        print('bye~')
        self.retf()

    def login(self, p):
        self.uid = p.head.uid
        # todo, not done yet, send data list to user
        pass

    def logout(self, p):
        p.head.flag = 1
        self.sk.send(p.tobyte())
        self.uid = None
        return True
