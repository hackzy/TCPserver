import server
import socket
from threading import Thread as 线程
import traceback
from regdata import RegData
class Regserver(server.Server):
    
    def __init__(self,server) -> None:
        super().__init__(server)

    def 启动服务器(self,监听ip,监听端口):
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
            self.开始接受请求(client,客户IP[0])

    def 开始接受请求(self,user,ip):
        数据处理 = RegData(self.server,ip)
        thread = 线程(target=数据处理.请求处理线程,args=(user,))
        thread.setDaemon(True)
        thread.start()