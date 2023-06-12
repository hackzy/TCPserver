
from threading import Thread as 线程
from setting import *
from servertest import Server

class 服务器:
    def __init__(self) -> None:
        self.监听端口 = None
        self.游戏端口 = None
        self.游戏IP = None
        self.服务器 = None
        self.使用中 = False
                
    def 初始化服务器(self,serverid,游戏ip,游戏端口,监听端口):
        服务器组.append(self)
        服务器组[serverid].监听端口 = 监听端口
        服务器组[serverid].游戏IP = 游戏ip
        服务器组[serverid].游戏端口 = 游戏端口
        t = 线程(target=Server,args=(self,serverid,服务器监听地址,监听端口))
        t.setDaemon(True)
        t.start()

    def 分配空闲客户(self):
        for i in range(len(客户端组)):
            if 客户端组[i].使用中 == False:
                print("分配空闲客户",i)
                return i
        return 0
    