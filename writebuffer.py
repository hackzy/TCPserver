class WriteBuff:
    def __init__(self) -> None:
        self.data = b''

    def writeBytes(self,byte:bytes,bLen=False,lenType=0,byteorder='big'):
        if bLen == False:
            self.data += byte
            return
        if lenType == 0:
            self.data += len(byte).to_bytes()
        elif lenType == 1:
                self.writeInteger(len(byte),2,byteorder)
        elif lenType == 2:
                self.writeInteger(len(byte),byteorder=byteorder)
        self.data = self.data + byte
        return
    
    def writeStr(self,sstr:str,bLen=False,lenType=0,byteorder='big'):
        if bLen == False:
            self.data += bytes(sstr,'utf8')
            return
        if lenType == 0:
            self.data += len(sstr.encode()).to_bytes()
        elif lenType == 1:
            self.writeInteger(len(sstr.encode()),2,byteorder)
        elif lenType == 2:
            self.writeInteger(len(sstr.encode()),byteorder=byteorder)
        self.data += bytes(sstr,'utf-8')
        return
    
    def writeInteger(self,iint:int,length = 4,byteorder='big'):
        self.data += iint.to_bytes(length,byteorder)
        return
    
    def getLen(self):
         return len(self.data)
    
    def getBuffer(self):
         return self.data
    
    def clearBuffer(self):
         self.data = b''