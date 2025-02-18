import socket
from setting import *
from threading import Timer,Thread as 线程

import traceback
from src.game.GameData import GameData
from src.assisted.fuzhu import fuzhu
from .sendToClient import SendToClient


class Client:
    '''客户对象类，每个客户连接插件服务端就创建一个客户对象连接游戏的服务器'''
    def __init__(self,server) -> None:
        '''初始化客户属性'''
        self.server = server
        self.未请求 = b''
        self.gamedata = GameData()
        self.fuzhu = fuzhu(server,self)
        self.账号 = ''
        self.在线中 = False
        self.未发送 = b''
        self.time = 0
    def 客户端启动(self,ip,端口):
        '''启动连接服务器'''
        self.port = 端口
        try:
            self.服务器句柄 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.服务器句柄.connect((ip,端口))
            c1 = 线程(target=self.数据到达)
            c1.setDaemon(True)
            c1.start()
        except:
            self.server.写日志("连接服务器失败，请检查服务器是否开启，详细错误：{}".format(traceback.format_exc()))

    def 初始化客户信息(self,客户句柄:socket.socket,客户IP:str,cid:int):
        '''初始化客户连接属性'''
        self.客户句柄 = 客户句柄
        self.客户IP = 客户IP
        self.cid = cid
        self.在线中 = True

    def 数据到达(self):
        '''开始接收服务器发来的数据'''
        while self.在线中:
            try:
                buffer = self.服务器句柄.recv(20000)
                if buffer == b'' :
                    if self.gamedata.角色名 != '':
                        if self.账号 == GM账号 and self.port == 游戏端口[1]:
                            self.server.写日志('GM号已掉线,所有功能已失效,2秒后自动上线。。。')
                            self.server.GM.挂载 = False
                            self.server.GM.GMUSER.在线中 = False
                    return
                else:
                    self.未发送 += buffer
                    self.接收处理线程()
            except:
                return

    def 接收处理线程(self):
        while self.未发送[:2] == b'MZ':
            leng = int.from_bytes(self.未发送[8:10])
            if len(self.未发送) - 10 >= leng:
                buffer = self.未发送[:leng+10]
                self.未发送 = self.未发送[leng + 10:]
                请求处理线程 = 线程(target=self.接收处理中心,args=(buffer,))
                请求处理线程.daemon = True
                请求处理线程.start()
                continue
            break

    def 接收处理中心(self,buffer:bytes):
        客户接收处理 = SendToClient(self,self.server)
        包头 = buffer[10:12]
        #self.server.写日志(buffer.hex())
        if 包头.hex() == "3357":
            buffer = 客户接收处理.登录线路(buffer)
            if self.账号 == GM账号:
                self.server.GM.GM_login_line()
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_3357())
                return
        elif 包头.hex() == "4355":
            buffer = 客户接收处理.显示线路(buffer)
            if self.账号 == GM账号:
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_4355())
                return
        elif 包头.hex() == '20d7':
            buffer = 客户接收处理.切换角色(buffer)
        elif 包头.hex() == 'fff5':
            客户接收处理.背包读取(buffer)
        elif 包头.hex() == 'fff7':
            客户接收处理.人物属性读取(buffer)
        elif 包头.hex() == '7feb':
            客户接收处理.技能读取(buffer)
        elif 包头.hex() == 'fff1':
            #屏蔽垃圾
            if self.gamedata.屏蔽垃圾:
                buffer = b''
        elif 包头.hex() == 'fff9':
                客户接收处理.周围对象读取(buffer)
        elif 包头.hex() == '1043':
                self.gamedata.参战宠物id = int.from_bytes(buffer[12:16])
        elif 包头.hex() == '1deb':
            if buffer[19:20].hex() == '19':
                if self.fuzhu.自动战斗.开关:
                #buffer = self.server.基础功能.战斗时间(buffer)
                    t1 = Timer(2,self.fuzhu.自动战斗.开始战斗)
                    t1.start()
        elif 包头.hex() == 'fdf9':
            if self.fuzhu.自动战斗.开关:
                self.fuzhu.自动战斗.置攻击位置id(buffer)
        elif 包头.hex() == '1df5':
            if self.fuzhu.自动战斗.开关:
                self.fuzhu.自动战斗.删攻击id(buffer)
        elif 包头.hex() == 'ffe1':
            客户接收处理.地图事件(buffer)
        elif 包头.hex() == 'f061':
            客户接收处理.取角色gid(buffer)
            if self.账号 == GM账号:
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1060())
                return
        elif 包头.hex() == '2301' and self == self.server.GM.GMUSER:
            self.server.GM.元宝寄售(buffer)
        elif 包头.hex() == 'fdd1':
            客户接收处理.战斗对话(buffer)
        elif 包头.hex() == 'ffdb':
            客户接收处理.商城读取(buffer)
        elif 包头.hex() == '2037':
            buffer = 客户接收处理.NPC对话(buffer)
        elif 包头.hex() == '10ec':
            客户接收处理.宠物数据更新(buffer)
        elif 包头.hex() == 'ffe3':
            客户接收处理.宠物读取(buffer)
        elif 包头.hex() == '0dfd':
            if self.fuzhu.自动战斗.开关:
                t = 线程(target=self.fuzhu.自动战斗.补充状态())
                t.start()
        elif 包头.hex() == '402f':
            客户接收处理.读当前坐标(buffer)
        elif 包头.hex() == 'f0dd':
            客户接收处理.读自身显示属性(buffer)
        elif 包头.hex() == 'f071':
            客户接收处理.任务读取(buffer)
        elif 包头.hex() == '10b3' and self.账号 == GM账号 and self.server.GM.挂载:
            self.server.GM.setsHeartbeatd(buffer)
        elif 包头.hex() == '1003':
            客户接收处理.角色登录(buffer)
            if self.账号 == GM账号:
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_10d1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1003())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1003_2())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_1())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_1b01_2())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_success())
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_10b1_3())
                self.server.GM.挂载 = True
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_heartbeatd())
                self.server.GM.tGMHeartbeatd()
                self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_10b1_4())
        elif 包头.hex() == '5351' and self.账号 == GM账号:
            self.server.GM.login_check = buffer[16:20]
            self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_5351())
            return
        elif 包头.hex() == '10b2' and self.账号 == GM账号:
            self.server.GM.GMUSER.服务器句柄.send(self.server.GM.login_acc_10b2())
        try:
            if len(buffer) != 0 and self.账号 != GM账号:
                self.客户句柄.send(buffer)
        except:
            self.客户句柄.close()
