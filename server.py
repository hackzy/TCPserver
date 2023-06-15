
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
            self.server.启动客户端(client,客户IP,sid)
            



