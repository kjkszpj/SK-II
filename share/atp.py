# -*- coding:utf-8 -*-

###
#   support feature:
#   1.  player control
#       a.  setup
#       b.  play
#       c.  pause
#       d.  teardown
#       e.  other option
#   2.  control flow?
#       a.  ack
#       b.  retransmit
#       c.  quit
#   3.  user feature
#   4.  version control?
#   5.  recorder
#   6.  other
#
#   design of header
#   1byte:  magic number, 110 & version(0 for now)
#   1byte:  type of package
#   1byte:  function selection
#   1byte:  flag
#   2byte:  uid
#   2byte:  did
###


class HEAD(object):
    #   1B
    version = 0
    #   1B
    type = 0
    #   1B
    func = 0
    #   1b
    flag = 0
    #   2B
    uid = 0
    #   2B
    did = 0

    def __init__(self, data=bytearray(8)):
        self.version = int(data[0])
        self.version = 0b01101111
        self.type = int(data[1])
        self.func = int(data[2])
        self.flag = int(data[3])
        self.uid = int((data[4] << 8) + data[5])
        self.did = int((data[6] << 8) + data[7])

    def tobyte(self):
        try:
            self.check_format()
        except:
            print('header format is wrong')
            return bytearray(8)
        else:
            return bytearray((self.version, self.type, self.func, self.flag)) + tobyte(self.uid, 2) + tobyte(self.did, 2)

    def check_format(self):
        assert self.version in range(0, 0x100)
        assert self.type in range(0, 0x100)
        assert self.func in range(0, 0x100)
        assert self.flag in range(0, 0x100)
        assert self.uid in range(0, 0x10000)
        assert self.did in range(0, 0x10000)

    def verify(self):
        return self.version & 0xF0 == 0b01100000


class ATP(object):
    head = HEAD()
    info = bytearray(800)
    #   security information?

    def __init__(self, data=bytearray(800 + 8)):
        assert type(data) == bytearray
        assert len(data) >= 8
        self.head = HEAD(data[:8])
        self.info = data[8:]

    def tobyte(self, display=True):
        # assert type(self.info) == bytearray
        if display: print((self.head.tobyte() + tobyte(self.info) + tobyte('\0'))[:32])
        return self.head.tobyte() + tobyte(self.info) + tobyte('\0')

    def verify(self):
        return self.head.verify()


def tobyte(data, len=0):
    if type(data) == int:
        result = bytearray([data & 0xFF])
        data >>= 8
        while data != 0 or len > 1:
            result = bytearray([data & 0xFF]) + result
            data >>= 8
            len -= 1
        return result
    elif type(data) == bytearray:
        return data
    elif type(data) == str:
        return str.encode(data, 'utf-8')
    elif type(data) == bytes:
        return bytearray(data)


def readint(data):
    assert type(data) == bytearray
    result = 0
    for i in data:
        assert chr(i) in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ' ', '\0']
        if i == ' ' or i == '\0': break
        result = result * 10 + i - ord('0')
    return result


if __name__ == '__main__':
    a = ATP()
    print(a.tobyte())
