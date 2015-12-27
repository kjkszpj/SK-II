import socket
import threading
import wave
from time import sleep
from share.atp import *
from share.config import CONFIG


class CONTENT_CONTROL(threading.Thread):
    content = None
    uid = None
    did = None
    sk = None
    status = None
    pos = None

    def __init__(self, dconn):
        threading.Thread.__init__(self)
        self.sk = dconn

    def setup(self, package):
        if not self.content is None: self.content.close()
        try:
            self.content = wave.open('data/%d.wav' % package.head.did, 'rb')
        except:
            msg = ATP()
            msg.head.type = 2
            msg.head.flag = 1
            msg.info = 'data/%d.wav' % package.head.did
            self.sk.sendall(msg.tobyte())
            return
        else:
            pass
        self.uid = package.head.uid
        self.did = package.head.did
        self.pos = 0
        self.status = 'NEW'
        # construct new package
        package.head.flag = 1
        package.info = '%d %d %d' % (self.content.getsampwidth(),
                                       self.content.getnchannels(),
                                       self.content.getframerate())
        self.sk.sendall(package.tobyte())

    def play(self, package=None):
        if not package is None:
            self.pos = int(package.info.decode('utf-8')[:-1])
        if self.content is None:
            package.head.type = 2
            package.head.flag = 1
            package.info = 'open it before play'
            self.sk.sendall(package.tobyte())
            return
        # self.content.setpos(self.pos * CONFIG.cnt_frames)
        # print(self.content.tell())
        self.status = 'PLAY'
        data = self.content.readframes(CONFIG.cnt_frames)
        # construct new package
        package = ATP()
        package.head.type = 0
        package.head.func = 1
        package.head.flag = 1
        package.head.uid = self.uid
        package.head.did = self.did
        package.info = bytearray(tobyte('%d %d ' % (len(data), self.pos)) + bytearray(data))
        self.sk.sendall(package.tobyte(False))
        if len(data) == 0:
            print('End of play')
            self.status = 'STOP'
        # sleep(0.1)
        self.pos += 1
        print(len(data))
        print(self.status)
        # input('.')

    def pause(self, package=None):
        self.status = 'PAUSE'

    def teardown(self, package=None):
        self.content.close()
        self.content = None
        self.status = 'STOP'

    def run(self):
        while self.status != 'STOP':
            if self.status == 'PLAY':
                self.play()
            sleep(0.01)
            pass
