
import socket
import traceback
from setting import *
from threading import Thread
from client import Client
class Server:
    """
    服务端主类
    """


    #@staticmethod


    def __init__(self,server,sid,ip, port):
        self.server = server
        self.connections = []  # 所有客户端连接
        self.server.write_log("服务器启动中，请稍候...")
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 监听者，用于接收新的socket连接
            self.listener.bind((ip, port))  # 绑定ip、端口
            self.listener.listen(5)  # 最大等待数
            
        except:
            self.server.write_log('服务器启动失败，请检查ip端口是否被占用。详细原因：\n' + traceback.format_exc())


        self.server.write_log('服务器启动成功：{}:{}'.format(ip,port))
        while True:
            client, 客户端IP = self.listener.accept()  # 阻塞，等待客户端连接
            self.server.client.append(Client(self.server))
            cid = self.server.分配空闲客户()
            self.server.client[cid].cid = cid
            self.server.client[cid].客户句柄 = client
            self.server.client[cid].客户IP = 客户端IP[0]
            self.server.client[cid].sid = sid
            self.server.client[cid].客户端启动(self.server.server[sid].游戏IP,self.server.server[sid].游戏端口)
            print(self.server.server[sid].游戏IP,self.server.server[sid].游戏端口,len(self.server.client))
            self.server.server[sid].开始接受请求(cid)
            #user = self.__user_cls(self.server, self.connections,cid)
            #self.connections.append(user)
            
            self.server.write_log('有客户进入，当前连接数：{}，IP：{}'.format(len(self.server.client),客户端IP[0]))
            



