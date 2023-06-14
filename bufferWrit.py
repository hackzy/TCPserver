class 写封包:
    def __init__(self) -> None:
        self.data = b''

    def 写字节集(self,buffer:bytes,声明长度=False,长度类型=0,反转长度=True):
        if 声明长度 == False:
            self.data = self.data + buffer
            return
        if 长度类型 == 0:
            self.写字节型(len(buffer).to_bytes())
        elif 长度类型 == 1:
                self.写短整数型(len(buffer),反转长度)
        elif 长度类型 == 2:
                self.写整数型(len(buffer),反转长度)
        self.data = self.data + buffer
        return
    
    def 写文本型(self,buffer:str,声明长度=False,长度类型=0,反转长度=False):
        if 声明长度 == False:
            self.data = self.data + bytes(buffer,'utf8')
            return
        if 长度类型 == 0:
            self.写字节型(len(buffer).to_bytes())
        elif 长度类型 == 1:
            self.写短整数型(len(buffer),反转长度)
        elif 长度类型 == 2:
            self.写整数型(len(buffer),反转长度)
        self.data = self.data + bytes(buffer,'utf-8')
        return
    
    def 写字节型(self,buffer:bytes):
         self.data += buffer
         return
    
    def 写短整数型(self,buffer,反转=False):
        if 反转:
            self.data += buffer.to_bytes(2,'big')
        else:
            self.data += buffer.to_bytes(2,'little')
        return
    
    def 写整数型(self,buffer,反转=False):
        if 反转:
            self.data += buffer.to_bytes(4,'big')
        else:
            self.data += buffer.to_bytes(4,'little')
        return
    
    def 取长度(self):
         return len(self.data)
    
    def 取数据(self):
         return self.data
    
    def 清数据(self):
         self.data = b''