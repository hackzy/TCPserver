from setting import *
from data import 数据池
from threading import Thread as 线程
class 客户端数据处理:
    '''客户端数据处理类，负责处理服务器发来的数据'''
    def __init__(self,server) -> None:
        self.未发送 = bytes()
        self.server = server
    def 接收处理线程(self,cid):
        data = 数据池()
        data.置数据(self.未发送)
        self.未发送 = b''
        while data.是否还有剩余():
            buffer = data.取出数据()
            if self.server.client[cid].使用中 == True:
                中心线程 = 线程(target=self.接收处理中心,args=(cid,buffer))
                中心线程.daemon = True
                中心线程.start()



    def 接收处理中心(self,cid,buffer):
        包头 = buffer[10:12]
        #print(包头.hex())
        #self.server.写日志(self.未发送.hex())
        if 包头.hex() == "3357":
            buffer = self.登录线路(buffer)
        if 包头.hex() == "4355":
            buffer = self.显示线路(buffer)
        if len(buffer) != 0 :
            self.server.client[cid].客户句柄.send(buffer)


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