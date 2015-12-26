import socket
import threading
import wave
from time import sleep
from share.atp import ATP
from share.config import CONFIG
from server.content_control import CONTENT_CONTROL

class CLIENT_HANDLE(threading.Thread):
    sk = None
    data = None
    content = None

    def __init__(self, dconn):
        threading.Thread.__init__(self)
        self.sk = dconn

    def run(self):
        # todo, where to put init of content_control?
        self.content = CONTENT_CONTROL(self.sk, None)
        self.content.start()
        while True:
            raw_data = self.sk.recv(CONFIG.buffersize)
            p = ATP(raw_data)
            func = None
            if not p.verify():
                print('---ERROR, package format wrong')
                pass
                break
            if p.head.type == 0:
                if p.head.func == 0:      func = self.content.setup
                elif p.head.func == 1:    func = self.content.play
                elif p.head.func == 2:    func = self.content.pause
                elif p.head.func == 3:    func = self.content.teardown
            elif p.head.type == 1:
                if p.head.func == 0:      pass
            func(p)
