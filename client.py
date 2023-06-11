import socket
import setting
from threading import Thread as 线程
class Client:
    def __init__(self,sid) -> None:
        self.cid = 0
        self.客户IP = 0
        self.连接id = 0
        self.服务器数组id = sid
        self.客户端id = 0
        self.未发送 = 0
        self.未请求 = bytes()
    
    def 客户端启动(self,cid,ip,端口):
        self.客户端id = socket.socket()
        self.客户端id.connect((ip,端口))
        return cid
    
    def 数据到达(self,cid):
        buffer = self.客户端id.recv()
        print("客户端数据",buffer)
        if cid != 0:
            self.未发送 = self.未发送 + buffer
            t = 线程(target=self.接收处理线程,args=(cid,))
            self.连接id.send(buffer)

    def 接收处理线程(self,cid):
        pass