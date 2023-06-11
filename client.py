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
        self.未发送 = bytes()
        self.未请求 = bytes()
    
    def 客户端启动(self,cid,ip,端口):
        self.客户端id = socket.socket()
        self.客户端id.connect((ip,端口))
        c1 = 线程(target=self.数据到达,args=(cid,))
        c1.setDaemon(True)
        c1.start()
        return cid
    
    def 数据到达(self,cid):
        while True:
            buffer = self.客户端id.recv(50000)
            print("客户端数据",buffer.hex())
            if cid != None:
                self.未发送 = self.未发送 + buffer
                t = 线程(target=self.接收处理线程,args=(cid,))
                t.setDaemon(True)
                t.start()
                setting.服务器[setting.客户端[cid].服务器数组id].服务器.send(buffer)
            if len(buffer) == 0:
                    self.客户端id.close()
                    # 删除连接
                    print("服务器断开")
                    break

    def 接收处理线程(self,cid):
        pass