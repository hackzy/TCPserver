
import socket
import traceback
from setting import *
from threading import Thread
from client import Client
class Server:
    """
    服务端主类
    """
    __user_cls = None

    @staticmethod


    def __init__(self,server,sid,ip, port):
        self.server = server
        self.connections = []  # 所有客户端连接
        self.server.write_log('服务器启动中，请稍候...')
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 监听者，用于接收新的socket连接
            self.listener.bind((ip, port))  # 绑定ip、端口
            self.listener.listen(5)  # 最大等待数
            
        except:
            self.server.write_log('服务器启动失败，请检查ip端口是否被占用。详细原因：\n' + traceback.format_exc())

        if self.__user_cls is None:
            self.server.write_log('服务器启动失败，未注册用户自定义类')
            return

        self.server.write_log('服务器启动成功：{}:{}'.format(ip,port))
        while True:
            client, 客户端IP = self.listener.accept()  # 阻塞，等待客户端连接
            self.server.client.append(Client(self.server))
            cid = self.server.分配空闲客户()
            self.server.client[cid].cid = cid
            self.server.client[cid].客户句柄 = client
            self.server.client[cid].客户IP = 客户端IP
            self.server.client[cid].sid = sid
            self.server.client[cid].客户端启动(self.server.server[sid].游戏IP,self.server.server[sid].游戏端口)
            print(self.server.server[sid].游戏IP,self.server.server[sid].游戏端口,len(self.server.client))
            
            #user = self.__user_cls(self.server, self.connections,cid)
            #self.connections.append(user)
            
            self.server.write_log('有新连接进入，当前连接数：{}'.format(len(self.connections)))





    @classmethod
    def register_cls(cls, sub_cls):
        """
        注册玩家的自定义类
        """
        if not issubclass(sub_cls, Connection):
            cls.write_log('注册用户自定义类失败，类型不匹配')
            return

        cls.__user_cls = sub_cls


class Connection:
    """
    连接类，每个socket连接都是一个connection
    """

    def __init__(self,server, connections,cid):
        self.connections = connections
        self.data_handler()
        self.cid = cid
        self.server = server
    def data_handler(self):
        # 给每个连接创建一个独立的线程进行管理
        thread = Thread(target=self.recv_data)
        thread.setDaemon(True)
        thread.start()

    def recv_data(self):
        # 接收数据
        try:
            while True:
                bytes = self.server.client[self.cid].客户句柄.recv(50000)  # 我们这里只做一个简单的服务端框架，不去做分包处理。所以每个数据包不要大于2048
                if len(bytes) == 0:
                    del self.server.client[self.cid]
                    print("客户断开")
                    self.connections.remove(self)
                    break
                # 处理数据
                self.deal_data(bytes)
        except:
            self.connections.remove(self)
            Server.write_log('有用户接收数据异常，已强制下线，详细原因：\n' + traceback.format_exc())

    def deal_data(self,bytes):
        """
        处理客户端的数据，需要子类实现
        """
        raise NotImplementedError


@Server.register_cls
class Player(Connection):
    """
    玩家类，我们的游戏中，每个连接都是一个Player对象
    """

    def __init__(self, *args):
        super().__init__(*args)

    def deal_data(self,bytes):
        """
        处理服务端发送的数据
        :param bytes:
        :return:
        """
        #客户端组[cid].未请求 = 客户端组[cid].未请求 + bytes
        if self.server.client[self.cid].服务器句柄 != -1:
            self.server.client[self.cid].服务器句柄.send(bytes)
            #print('\n客户端消息：',bytes.hex())
            #print("当前cid",self.cid)


