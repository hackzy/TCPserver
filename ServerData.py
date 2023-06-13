
from threading import Thread as 线程
from setting import *
from server import Server
import traceback
from sendToServer import 客户请求处理
class 服务器数据处理:
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
                    buffer = self.server.client[cid].客户句柄.recv(1000)  # 我们这里只做一个简单的服务端框架，不去做分包处理。所以每个数据包不要大于2048
                if len(buffer) == 0 or len(buffer) > 1000:
                    self.server.client[cid].客户句柄.close()
                    del self.server.client[cid]
                    buffer = b''
                    print("客户断开")
                    break
                # 处理数据
                self.处理数据(buffer,cid)
        except:
            if self.server.client[cid].客户句柄 != 0:
                self.server.client[cid].客户句柄.close()

            self.server.write_log('有用户接收数据异常，已强制下线，详细原因：\n' + traceback.format_exc())

    def 处理数据(self,buffer,cid):
        """
        处理准备发给服务器的数据
        """
        flag = True
        self.server.client[cid].未请求 = self.server.client[cid].未请求 + buffer
        while flag:
            if self.server.client[cid].未请求[:2] != b'MZ':
                break
            leng = int.from_bytes(self.server.client[cid].未请求[8:10])
            if len(self.server.client[cid].未请求) - 10 >= leng:
                buffer = self.server.client[cid].未请求[:leng+10]
                self.server.client[cid].未请求 = self.server.client[cid].未请求[:len(self.server.client[cid].未请求) - leng -10]
                buffer = self.请求处理中心(cid,buffer)
                if buffer != b'':
                    self.server.client[cid].服务器句柄.send(buffer)

    def 请求处理中心(cid,buffer):
        包头 = buffer[10:12]

        if 包头.hex() == '4062':
            return 客户请求处理.喊话(cid.buffer)
        