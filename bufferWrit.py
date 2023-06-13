class 写封包:
    def __init__(self) -> None:
        self.data = b''

    def 写字节集(self,buffer,声明长度=False,长度类型=0,反转长度=False):
        if 声明长度 == False:
            self.data = self.data + buffer
            return
        if 长度类型 == 0:
            self.写字节型(len(buffer))
        elif 长度类型 == 1:
                self.写短整数型(len(buffer),反转长度)
        elif 长度类型 == 2:
                self.写整数型(len(buffer),反转长度)
        self.data = self.data + buffer
        return
    
    def 写文本型(self,buffer,声明长度=False,长度类型=0,反转长度=False):
         bytes()