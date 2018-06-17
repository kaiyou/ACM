""" Notification objects and utils
"""

import struct


class Notification(object):

    def __init__(self, source=None):
        if source is None:
            self.data = bytearray(64)
        else:
            self.data = bytearray(source)

    @property
    def channel(self):
        return self.data[0:32]

    @channel.setter
    def channel(self, value):
        self.data[0:32] = value

    @property
    def format(self):
        return struct.unpack('<I', self.data[32:36])[0]

    @format.setter
    def format(self, value):
        self.data[32:36] = struct.pack('<I', value)

    @property
    def length(self):
        return self.data[36]

    @length.setter
    def length(self, value):
        self.data[36] = value

    @property
    def payload(self):
        return self.data[64:]

    @payload.setter
    def payload(self, value):
        print("ok")
        assert len(value) % 16 == 0 and len(value) < 4096
        del self.data[64:]
        self.length = len(value) // 16
        self.data += value


if __name__ == '__main__':
    n = Notification()
    n.format = 12
    print(n.payload)
    n.payload = b'\x01' * 32
    print(n.data)
