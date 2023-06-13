from setting import *


class 数据池 :
    def __init__(self) -> None:
        self.data = []
        self.now = 0

    def 置数据(self,buffer):
        self.data = buffer.split(组包包头)
        self.now = 0

    def 取出数据(self):
        if self.now > len(self.data):
            self.now += 1
            return 组包包头 + self.data[0]
        if self.data[self.now] == b"":
            self.now += 1
        len = int.from_bytes(self.data[self.now][:2],'little')
        if len(self.data[self.now]) - 2 == len:
            buffer = 组包包头 + self.data[self.now]
            self.now += 1
            return buffer
        buffer = 组包包头 + self.data[self.now]
        self.now += 1
        return buffer
    
    def 是否还有剩余(self):
        if self.now <= len(self.data):
            return True
        return False