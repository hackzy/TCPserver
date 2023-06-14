
import socket
import traceback
from setting import *
from client import Client
class Server:
    """
    服务端，为每个线路启动一个服务端对象
    """
    def __init__(self,server,sid,ip, port):
        '''初始化并启动服务端'''
        self.server = server
        self.connections = []  # 所有客户端连接
        self.server.写日志("服务器启动中，请稍候...")
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 监听者，用于接收新的socket连接
            self.listener.bind((ip, port))  # 绑定ip、端口
            self.listener.listen(5)  # 最大等待数
            
        except:
            self.server.写日志('服务器启动失败，请检查ip端口是否被占用。详细原因：\n' + traceback.format_exc())
        self.server.写日志('服务器启动成功：{}:{}'.format(ip,port))
        while True:
            '''开始监听客户'''
            client, 客户IP = self.listener.accept()          #阻塞，等待客户端连接
            #self.server.client.append(Client(self.server))  #客户连接，创建客户对象，加入客户列表
            #cid = self.server.分配空闲客户()                  #分配客户列表索引cid
            user = Client(self.server)
            user.初始化客户信息(client,客户IP[0],sid)  #保存客户属性
            user.客户端启动(self.server.server[sid].游戏IP,self.server.server[sid].游戏端口) #客户连接，启动连接服务端
            self.server.client.append(user)
            self.server.server[sid].开始接受请求(user)           #服务器启动接受客户发来的数据
            self.server.写日志('有客户进入，当前客户数：{}，IP：{}'.format(len(self.server.client),客户IP[0]))
            



