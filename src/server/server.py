import socket
import traceback
from threading import Thread as 线程
from setting import *
from src.server.ServerData import 服务器数据处理
class Server:
    """
    服务端，为每个线路启动一个服务端对象
    """
    def __init__(self,server):
        '''初始化并启动服务端'''
        self.server = server
        self.server.写日志("服务器启动中，请稍候...")
   
    def 启动服务器(self,游戏ip,游戏端口,监听ip,监听端口):
        self.游戏ip = 游戏ip
        self.游戏端口 = 游戏端口
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 监听者，用于接收新的socket连接
            self.listener.bind((监听ip, 监听端口))  # 绑定ip、端口
            self.listener.listen(5)  # 最大等待数
            
        except:
            self.server.写日志('服务器启动失败，请检查ip端口是否被占用。详细原因：\n' + traceback.format_exc())
        self.server.写日志('服务器启动成功：{}:{}'.format(监听ip,监听端口))
        监听线程 = 线程(target=self.开始监听客户)
        监听线程.daemon = True
        监听线程.start()

    def 开始监听客户(self):
        while True:
            '''开始监听客户'''
            client, 客户IP = self.listener.accept()          #阻塞，等待客户端连接
            self.server.客户连接(client,客户IP[0],self)

    def 开始接受请求(self,user):
        数据处理 = 服务器数据处理(self.server)
        线程(target=数据处理.请求处理线程,args=(user,),daemon=True).start()
        线程(target=数据处理.buffer_processing_queue,args=(user,),daemon=True).start()

