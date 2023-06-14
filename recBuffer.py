class 读封包:

    def __init__(self) -> None:
        self.data = b''
        self.leng = 0
        self.当前位置 = 0

    def 检测(self,长度):
        if self.当前位置 + 长度 > self.leng:
            长度 = self.leng - self.当前位置 
            return 长度
        return 长度
    def 置数据(self,buffer):
        self.data = buffer
        self.leng = len(self.data)
        self.当前位置 = 0
        return
    
    def 跳过(self,长度):
        self.当前位置 = self.当前位置 + 长度
        return
    
    def 读字节集(self,长度):
        长度 = self.检测(长度)
        记录位置 = self.当前位置
        self.当前位置 = self.当前位置 + 长度
        return self.data[记录位置:记录位置+长度]
    
    def 读短整数型(self,反转 = False):
        if self.检测(2) < 2:
            return 0
        记录位置 = self.当前位置
        self.当前位置 = self.当前位置 + 2
        if 反转:
            return int.from_bytes(self.data[记录位置:记录位置+2],'big')
        else:
            return int.from_bytes(self.data[记录位置:记录位置+2],'little')
        
    def 读整数型(self,反转 = False):
        if self.检测(4) < 4 :
            return 0
        记录位置 = self.当前位置
        self.当前位置 = self.当前位置 + 4
        if 反转:
            return int.from_bytes(self.data[记录位置:记录位置+4],'big')
        else:
            return int.from_bytes(self.data[记录位置:记录位置+4],'little')
        
    def 读字节型(self):
        if self.检测(1)<1:
            return 0
        记录位置 = self.当前位置
        self.当前位置 = self.当前位置 + 1
        return int.from_bytes(self.data[记录位置:记录位置+1])

    def 读文本型(self,有长度头=True,长度类型=0,反转长度=True):
        if 有长度头:
            if 长度类型 == 0:
                长度 = self.读字节型()
            elif 长度类型 == 1:
                长度 = self.读短整数型(反转长度)
            elif 长度类型 == 2:
                长度 = self.读整数型(反转长度)
            记录位置 = self.当前位置
            self.当前位置 += 长度
            return self.data[记录位置:记录位置+长度].decode('utf8')
        文本 = self.data[self.当前位置:].decode('utf8')
        长度 = len(bytes(文本,'utf8'))
        self.当前位置 += 长度
        return 文本