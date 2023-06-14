
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

    def 开始接受请求(self,user):
        thread = 线程(target=self.请求处理线程,args=(user,))
        thread.setDaemon(True)
        thread.start()

    def 请求处理线程(self,user):
        # 接收数据
        try:
            while True:
                if getattr(user.客户句柄,'_closed') == False:
                    buffer = user.客户句柄.recv(1000)  # 我们这里只做一个简单的服务端框架，不去做分包处理。所以每个数据包不要大于2048
                    if len(buffer) > 1000:
                        user.客户句柄.close()
                        buffer = b''
                        print("客户数据过大")
                        self.server.client.remove(user)
                        return
                else:
                    self.server.写日志('用户断开e')
                    self.server.client.remove(user)
                    return
                # 处理数据
                if buffer == b'':
                    self.server.client.remove(user)
                    del user
                    self.server.写日志('用户断开b')
                    return
                user.未请求 += buffer
                self.处理数据(user)
                
        except:
            #getattr(self.服务器句柄,'_closed')
            self.server.写日志('有用户接收数据异常，已强制下线，详细原因：\n' + traceback.format_exc())

    def 处理数据(self,user):
        """
        处理准备发给服务器的数据
        """
        while user.未请求[:2] == b'MZ':
            leng = int.from_bytes(user.未请求[8:10])
            if len(user.未请求) - 10 >= leng:
                buffer = user.未请求[:leng+10]
                user.未请求 = user.未请求[leng + 10:]
                请求处理线程 = 线程(target=self.请求处理中心,args=(buffer,user))
                请求处理线程.daemon = True
                请求处理线程.start()
                continue
            break
    def 请求处理中心(self,buffer,user):
        包头 = buffer[10:12]
        #self.server.写日志(包头.hex()+buffer.hex())
        请求处理 = 客户请求处理(self.server)
        if 包头.hex() == '4062':
            buffer = 请求处理.喊话(buffer)

        if buffer != b'' and getattr(user.服务器句柄,'_closed') == False:
            #print(buffer)
            user.服务器句柄.send(buffer)
