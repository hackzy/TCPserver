class ReadBuffer:

    def __init__(self) -> None:
        self.data = b''
        self.leng = 0
        self.now = 0

    def check(self,length:int):
        if self.now + length > self.leng:
            length = self.leng - self.now 
            return length
        return length
    def setBuffer(self,buffer:bytes):
        self.data = buffer
        self.leng = len(self.data)
        self.now = 0
        return
    
    def skip(self,length = 1):
        self.now += length
        return
    
    def byte(self,length):
        length = self.check(length)
        recLocation = self.now
        self.now += length
        return self.data[recLocation:recLocation+length]
    
    def integer(self,length = 4,byteorder = 'big'):
        if self.check(length) < length:
            return 0
        recLocation = self.now
        self.now += length
        return int.from_bytes(self.data[recLocation:recLocation + length],byteorder)

    def string(self,blen=True,lenType=0,byteorder='big'):
        try:
            if blen:
                if lenType == 0:
                    length = int.from_bytes(self.byte(1))
                elif lenType == 1:
                    length = self.integer(2,byteorder)
                elif lenType == 2:
                    length = self.integer(4,byteorder)
                recLocation = self.now
                self.now += length
                return self.data[recLocation:recLocation+length].decode('gbk')
            string = self.data[self.now:].decode(encoding='gbk')
            length = len(bytes(string,'gbk'))
            self.now += length
            return string
        except:
            return ''
    
    def getResidLen(self):
        return self.leng - self.now + 1
    
    def residBuffer(self):
        return self.byte(self.getResidLen())