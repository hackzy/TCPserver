import socket
from setting import *
from threading import Thread as 线程
from clientData import 客户端
class Client:
    def __init__(self,sid) -> None:
        self.cid = 0
        self.客户IP = 0
        self.连接id = 0
        self.服务器数组id = sid
        self.客户端id = 0
        self.使用中 = False
        self.客户数据处理 = 客户端()
        self.未请求 = bytes()
    
    def 客户端启动(self,cid,ip,端口):
        self.客户端id = socket.socket()
        self.客户端id.connect((ip,端口))
        c1 = 线程(target=self.数据到达,args=(cid,))
        c1.setDaemon(True)
        c1.start()
        return self.客户端id
    
    def 数据到达(self,cid):
        while True:
            buffer = self.客户端id.recv(50000)
            print("客户端数据",buffer.hex())
            if cid != None:
                self.客户数据处理.未发送 = buffer
                t = 线程(target=self.客户数据处理.接收处理线程,args=(cid,))
                t.setDaemon(True)
                t.start()
                
            if len(buffer) == 0:
                self.客户端id.close()
                # 删除连接
                #客户端组.remove(客户端组[cid])
                print("服务器断开")
                break

