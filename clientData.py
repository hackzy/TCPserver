from setting import *
from data import 数据池
from threading import Thread as 线程
from recBuffer import 读封包
from bufferWrit import 写封包
class 客户端数据处理:
    '''客户端数据处理类，负责处理服务器发来的数据'''
    def __init__(self,server) -> None:
        self.未发送 = bytes()
        self.server = server
    def 接收处理线程(self,user):
        data = 数据池()
        data.置数据(self.未发送)
        self.未发送 = b''
        while data.是否还有剩余():
            buffer = data.取出数据()
            if getattr(user.客户句柄,'_closed') == False:
                中心线程 = 线程(target=self.接收处理中心,args=(buffer,user))
                中心线程.daemon = True
                中心线程.start()

    def 接收处理中心(self,buffer,user):
        包头 = buffer[10:12]
        if 包头.hex() == "3357":
            buffer = self.登录线路(buffer)
        if 包头.hex() == "4355":
            buffer = self.显示线路(buffer)
        if 包头.hex() == '20d7':
            buffer = self.切换角色(buffer)
        if len(buffer) != 0 and getattr(user.客户句柄,'_closed') == False:
            user.客户句柄.send(buffer)

    def 登录线路(self,buffer):
        封包 = buffer[0:18]
        封包 = 封包 + len(服务器监听地址).to_bytes(1) +  bytes(服务器监听地址,'UTF-8') + \
                            服务器监听端口[1].to_bytes(2)
        封包 = 封包 + buffer[33:]
        封包 = 组包包头 + len(封包).to_bytes(2) + 封包[10:] 
        return 封包
    
    def 显示线路(self,buffer):
        a = 1
        封包 = buffer[10:12] + a.to_bytes(2)+ buffer[14:15] + buffer[15:15+buffer[14:15][0]] + \
            len(服务器监听地址).to_bytes(1) + bytes(服务器监听地址,'UTF-8') + buffer[-2:]
        封包 = 组包包头 + len(封包).to_bytes(2) + 封包
        return 封包
    
    def 切换角色(self,buffer):
        读 = 读封包()
        写 = 写封包()
        完整包 = 写封包()
        读.置数据(buffer)
        读.跳过(10)
        写.写字节集(读.读字节集(4))
        data = 读.读文本型()
        stri = data.split(" ")
        data = 服务器监听地址 + ' ' + str(服务器监听端口[1]) + ' '
        for i in range(len(stri) - 2):
            data = data + stri[i + 2] + ' '
        data = data[:len(data) - 1]
        写.写文本型(data,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1,True)
        return 完整包.取数据()