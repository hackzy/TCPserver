import socket
from setting import *
from threading import Thread as 线程
from clientData import 客户端数据处理
import traceback
from GameData import GameData
from fuzhu import fuzhu
from saveData import 存档

class Client:
    '''客户对象类，每个客户连接插件服务端就创建一个客户对象连接游戏的服务器'''
    def __init__(self,server) -> None:
        '''初始化客户属性'''
        self.server = server
        self.客户数据处理 = 客户端数据处理(self,server)
        self.未请求 = b''
        self.gamedata = GameData()
        self.fuzhu = fuzhu(server,self)
        self.账号 = ''
        self.在线中 = False
        
    def 客户端启动(self,ip,端口):
        '''启动连接服务器'''
        try:
            self.服务器句柄 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.服务器句柄.connect((ip,端口))
            c1 = 线程(target=self.数据到达)
            c1.setDaemon(True)
            c1.start()
        except:
            self.server.写日志("连接服务器失败，请检查服务器是否开启，详细错误：{}".format(traceback.format_exc()))

    def 初始化客户信息(self,客户句柄,客户IP,cid):
        '''初始化客户连接属性'''
        self.客户句柄 = 客户句柄
        self.客户IP = 客户IP
        self.cid = cid
        self.在线中 = True

    def 数据到达(self):
        '''开始接收服务器发来的数据'''
        while True:
            try:
                buffer = self.服务器句柄.recv(20000)
                if buffer == b'' :
                        # 删除连接
                    if self.gamedata.角色名 != '':
                        存档.存储账号信息(self)
                        if self.账号 == GM账号:
                            self.server.写日志('GM号已掉线,所有功能已失效')
                            self.server.GM.GMUSER = None
                    self.server.删除客户(self)
                    break
                else:
                    self.客户数据处理.未发送 += buffer
                    self.客户数据处理.接收处理线程(self)
            except:
                self.server.删除客户(self)
                return
