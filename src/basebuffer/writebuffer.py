class WriteBuff:
    def __init__(self) -> None:
        self.data = b''

    def byte(self,byte:bytes,bLen=False,lenType=0,byteorder='big'):
        if bLen == False:
            self.data += byte
            return
        if lenType == 0:
            self.data += len(byte).to_bytes()
        elif lenType == 1:
                self.integer(len(byte),2,byteorder)
        elif lenType == 2:
                self.integer(len(byte),byteorder=byteorder)
        self.data = self.data + byte
        return
    
    def string(self,sstr:str,bLen=True,lenType=0,byteorder='big'):
        if bLen == False:
            self.data += bytes(sstr,'gbk')
            return
        if lenType == 0:
            self.data += len(sstr.encode('gbk')).to_bytes()
        elif lenType == 1:
            self.integer(len(sstr.encode('gbk','utf8')),2,byteorder)
        elif lenType == 2:
            self.integer(len(sstr.encode('gbk')),byteorder=byteorder)
        self.data += bytes(sstr,'gbk')
        return
    
    def integer(self,iint:int,length = 4,byteorder='big'):
        self.data += iint.to_bytes(length,byteorder)
        return
    
    def getLen(self):
         return len(self.data)
    
    def getBuffer(self):
         return self.data
    
    def clearBuffer(self):
         self.data = b''