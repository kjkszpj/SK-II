import socket
import threading
import wave
from time import sleep
from share.atp import ATP
from share.config import CONFIG


class CONTENT_CONTROL(threading.Thread):
    content = None
    did = None
    sk = None
    status = None

    def __init__(self, dconn, data):
        threading.Thread.__init__(self)
        self.sk = dconn

    def setup(self, package):
        self.content = wave.open('../data/%d.wav' % package.did, 'rb')
        self.did = package.did
        self.status = 'NEW'
        # construct new package
        package.head.flag = 1
        package.info = '%d %d %d\0' % (self.content.getsampwidth(), self.content.getnchannels(), self.content.getframerate())
        self.sk.sendall(package.tobyte())

    def play(self, package):
        pos = 0
        if self.status == 'PLAY':
            pos = readint(package.info)
        elif self.status == 'PAUSE':
            pass
        elif self.status == 'NEW':
            pos = 0
        elif self.status == 'STOP':
            # should arise an error
            pos = 0
        self.content.setpos(pos)
        self.status = 'PLAY'
        while self.status == 'PLAY':
            data = self.content.readframes(1024)
            if len(data) == 0:
                self.status = 'STOP'
                break
            sleep(0.1)
            print(self.status)

    def pause(self, package=None):
        self.status = 'PAUSE'

    def teardown(self, package=None):
        self.content.close()
        self.status = 'STOP'

    def run(self):
        threading.Thread.run(self)
        while self.status != 'STOP': pass


def readint(data):
    assert type(data) == bytearray
    result = 0
    for i in data:
        assert i in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ']
        if i == ' ': break
        result = result * 10 + ord(i) - ord('0')
    return result
