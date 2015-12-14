# -*- coding:utf-8 -*-

###
#   support feature:
#   1.  player control
#       a.  setup
#       b.  play
#       c.  pause
#       d.  teardown
#       e.  other option
#   2.  control flow
#       a.  ack
#       b.  retransmit
#       c.  quit
#   3.  user love feature
#       a.  login
#       b.  record of user
#       c.  share among friend
#   4.  version control?
#   5.  recorder
#   6.  other
#
#   design of header
#   todo, src/dst?
#   1byte:  magic number & version
#   1byte:  type of package
#   1byte:  function selection
#   3byte:  other option
#   2byte:  checksum
###


class HEAD(object):
    #   1B
    #   1B
    #   1B
    #   3B
    #   2B
    version = 0
    type = 0
    func = 0
    option = 0
    cs = 0

    def __init__(self, data=bytearray(8)):
        self.version = int(data[0])
        self.type = int(data[1])
        self.func = int(data[2])
        self.option = int((data[3] << 16) + (data[4] << 8) + data[5])
        self.cs = int((data[6] << 8) + data[7])

    def tobyte(self):
        try:
            self.check_format()
        except:
            print('header format is wrong')
            return bytearray(8)
        else:
            return tobyte(self.version) + tobyte(self.type) + tobyte(self.func) + tobyte(self.option) + tobyte(self.cs)

    def check_format(self):
        assert self.version in range(0, 0x100)
        assert self.type in range(0, 0x100)
        assert self.func in range(0, 0x100)
        assert self.option in range(0, 0x1000000)
        assert self.cs in range(0, 0x10000)

    def verify(self):
        return self.version & 0xF0 == 0b1010


class ATP(object):
    head = HEAD()
    info = bytearray(1000)
    #   security information?

    def __init__(self, data=bytearray(1000 + 8)):
        assert type(data) == bytearray
        assert len(data) >= 8
        self.head = HEAD(data[:8])
        self.info = data[8:]

    def tobyte(self):
        return self.head.tobyte() + self.info

    def verify(self):
        return self.head.verify()


def tobyte(data):
    if type(data) == int:
        result = bytearray([data & 0xFF])
        data >>= 8
        while data != 0:
            result = bytearray([data & 0xFF]) + result
            data >>= 8
        return result
    pass


if __name__ == '__main__':
    a = ATP()
    print(a.tobyte())