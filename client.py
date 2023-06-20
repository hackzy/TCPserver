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
        self.客户IP = ''
        self.server = server
        self.sid = 0
        self.客户句柄 = None
        self.服务器句柄 = None
        self.客户数据处理 = 客户端数据处理(self,server)
        self.未请求 = b''
        self.gamedata = GameData()
        self.fuzhu = fuzhu(server,self)
        self.cid = 0
        self.账号 = ''
        
    
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
    def 初始化客户信息(self,客户句柄,客户IP,sid,cid):
        '''初始化客户连接属性'''
        self.客户句柄 = 客户句柄
        self.客户IP = 客户IP
        self.sid = sid
        self.cid = cid
    def 数据到达(self):
        '''开始接收服务器发来的数据'''
        while True:
            try:
                if getattr(self.服务器句柄,'_closed') == False:
                    buffer = self.服务器句柄.recv(20000)
                    if buffer == b'' or getattr(self.服务器句柄,
                                                   '_closed') == True:
                        # 删除连接
                        if self.gamedata.角色名 != '':
                            存档.存储账号信息(self)
                            self.server.写日志('玩家: '+self.gamedata.角色名+' 下线 Ip:'+self.客户IP+'  当前在线人数:'+str(len(self.server.user)))
                            if self.账号 == GM账号:
                                self.server.写日志('GM号已掉线,所有功能已失效')
                                self.server.GM.GMUSER = None

                        #print("断开与服务器连接1")
                        del self
                        return
                    self.客户数据处理.未发送 += buffer
                    self.客户数据处理.接收处理线程(self)
                else:
                        # 删除连接
                    self.server.user.pop(self.cid)
                    print("断开与服务器连接2",self.服务器句柄)
                    return
            except:
                print("接收数据异常",len(buffer),traceback.format_exc())
                return
