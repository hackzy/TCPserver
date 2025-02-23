import src.server.server as server
import socket
from threading import Thread as 线程
import traceback
from src.regserver.regdata import RegData
class Regserver(server.Server):
    
    def __init__(self,server) -> None:
        super().__init__(server)
        self.connips = []
    def 启动服务器(self,监听ip,监听端口):
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 监听者，用于接收新的socket连接
            self.listener.bind((监听ip, 监听端口))  # 绑定ip、端口
            self.listener.listen(5)  # 最大等待数
            
        except:
            self.server.写日志('注册网关启动失败，请检查ip端口是否被占用。详细原因：\n' + traceback.format_exc())
        self.server.写日志('注册网关启动成功：{}:{}'.format(监听ip,监听端口))
        监听线程 = 线程(target=self.开始监听客户)
        监听线程.daemon = True
        监听线程.start()

    def 开始监听客户(self):
        while True:
            '''开始监听客户'''
            client, 客户IP = self.listener.accept()          #阻塞，等待客户端连接
            if self.server.is_allowed(客户IP[0]):
                self.server.写日志(f"ip：{客户IP[0]}，30 秒内连接数已达到最大值：{len(self.server.ip_connections[客户IP[0]])}，拉黑！",console=False)
                self.server.ensure_rule_exists("IP黑名单",客户IP[0])
                client.close()
                return
            if len(self.connips) > 2:
                self.Logger(f"ip：[{客户IP[0]}]，请求连接，但总连接数已达到最大值：{len(self.connips)}，已拒绝连接",console=False)
                client.close()
                return
            self.server.写日志("客户连接注册服务器 IP:{}".format(客户IP[0]))
            self.connips.append(客户IP[0])
            self.开始接受请求(client,客户IP[0])
            
    def 开始接受请求(self,user,ip):
        数据处理 = RegData(self.server,ip)
        thread = 线程(target=数据处理.请求处理线程,args=(user,))
        thread.setDaemon(True)
        thread.start()