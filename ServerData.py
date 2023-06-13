
from threading import Thread as 线程
from setting import *
from server import Server
import traceback
class 服务器:
    def __init__(self,server) -> None:
        self.监听端口 = None
        self.游戏端口 = None
        self.游戏IP = "127.0.0.1"
        self.客户句柄 = 0
        self.sid = 0
        self.server = server
                
    def 初始化服务器(self,serverid,游戏ip,游戏端口,监听端口):
        self.监听端口 = 监听端口
        self.游戏IP = 游戏ip
        self.游戏端口 = 游戏端口
        self.sid = serverid
        t = 线程(target=Server,args=(self.server,serverid,服务器监听地址,监听端口))
        t.setDaemon(True)
        t.start()

    def 开始接受请求(self,cid):
        thread = 线程(target=self.请求处理线程,args=(cid,))
        thread.setDaemon(True)
        thread.start()

    def 请求处理线程(self,cid):
        # 接收数据
        try:
            while True:
                if self.server.client[cid].客户句柄 != 0:
                    bytes = self.server.client[cid].客户句柄.recv(1000)  # 我们这里只做一个简单的服务端框架，不去做分包处理。所以每个数据包不要大于2048
                if len(bytes) == 0:
                    self.server.client[cid].客户句柄.close()
                    del self.server.client[cid]
                    print("客户断开")
                    break
                # 处理数据
                self.deal_data(bytes,cid)
        except:
            if type(self.server.client[cid].客户句柄) != 0:
                self.server.client[cid].客户句柄.close()
            self.server.write_log('有用户接收数据异常，已强制下线，详细原因：\n' + traceback.format_exc())

    def deal_data(self,bytes,cid):
        """
        处理服务端发送的数据
        :param bytes:
        :return:
        """
        #客户端组[cid].未请求 = 客户端组[cid].未请求 + bytes
        if self.server.client[cid].服务器句柄 != -1:
            self.server.client[cid].服务器句柄.send(bytes)
            #print('\n客户端消息：',bytes.hex())
            #print("当前cid",self.cid)
