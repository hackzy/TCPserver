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
            self.data += bytes(sstr,'utf8')
            return
        if lenType == 0:
            self.data += len(sstr.encode()).to_bytes()
        elif lenType == 1:
            self.integer(len(sstr.encode()),2,byteorder)
        elif lenType == 2:
            self.integer(len(sstr.encode()),byteorder=byteorder)
        self.data += bytes(sstr,'utf-8')
        return
    
    def integer(self,iint:int,length = 4,byteorder='big'):
        tempLength = (iint.bit_length()+7)// 8
        if tempLength > 4:
                iint = iint.to_bytes(tempLength,byteorder)[-length:]
        else:
                iint = iint.to_bytes(length,byteorder)
        self.data += iint
        return
    
    def getLen(self):
         return len(self.data)
    
    def getBuffer(self):
         return self.data
    
    def clearBuffer(self):
         self.data = b''