import socket
from setting import *
from threading import Thread as 线程
from clientData import 客户端
class Client:
    def __init__(self,server) -> None:
        self.cid = 0
        self.客户IP = 0
        self.server = server
        self.sid = 0
        self.客户句柄 = 0
        self.服务器句柄 = 0
        self.使用中 = False
        self.客户数据处理 = 客户端(self.server)
        self.未请求 = bytes()
    
    def 客户端启动(self,ip,端口):
        self.服务器句柄 = socket.socket()
        self.服务器句柄.connect((ip,端口))
        c1 = 线程(target=self.数据到达)
        c1.setDaemon(True)
        c1.start()
        
    
    def 数据到达(self):
        while True:
            try:
                if self.服务器句柄 != -1:
                    buffer = self.服务器句柄.recv(100000)
                #print("客户端数据",buffer.hex())
                if self.cid != None:
                    self.客户数据处理.未发送 = buffer
                    
                    self.客户数据处理.接收处理线程(self.cid)
                    
                
                if len(buffer) == 0:
                
                    self.服务器句柄.close()
                    # 删除连接
                    print("断开与服务器连接",self.服务器句柄,self.cid)
                    break
            except:
                print("接收数据异常",len(buffer))
                #self.服务器句柄.close()
                # 删除连接
                #del self.server.client[self.cid]
                #客户端组.remove(客户端组[cid])