import datetime
import logging
from otherKing import 基础功能
from gm import GM
from setting import *
import os
from server import Server
from regserver import Regserver
from persion import 逍遥假人
import threading
import random

class 逍遥插件:
    '''全局管理类，负责保存分配客户与服务端信息'''
    def __init__(self) -> None:
        self.server = []
        self.sid = 0
        self.user = {}
        self.基础功能 = 基础功能()
        self.GM = GM(self)
        self.测试 = 0
        self.regserver = None
        self.假人 = []
        self.擂台假人 = []
        self.商会假人 = []
        self.拍卖行假人 = []
        self.活动大使假人 = []
        for i in range(400):
            self.假人.append(逍遥假人(self,'所有'))
        for i in range(50):
            self.擂台假人.append(逍遥假人(self,'擂台'))
        for i in range(50):
            self.商会假人.append(逍遥假人(self,'商会'))
        for i in range(50):
            self.拍卖行假人.append(逍遥假人(self,'拍卖'))
        for i in range(50):
            self.活动大使假人.append(逍遥假人(self,'活动大使'))
        移动线程 = threading.Thread(target=self.假人移动线程)
        移动线程.daemon = True
        移动线程.start()
    
    def 写日志(self,msg):
        cur_time = datetime.datetime.now()
        filename = str(cur_time.year) + "年" + str(cur_time.month) + '月' + str(cur_time.day) + '日'
        s = "[" + str(cur_time.time()) + "]" + str(msg)
        logger = logging.getLogger(__name__)
        logger.setLevel(level = logging.INFO)
        handler = logging.FileHandler('./log/' + filename + '.log',encoding='utf-8')   #log.txt是文件的名字，可以任意修改
        handler.setLevel(logging.INFO)
        if not logger.handlers:
            logger.addHandler(handler)
        logger.info(s)
        logger.removeHandler(handler)
        handler.close()
        os.system('ECHO %s' % (s))

    def 删除客户(self,user):
        try:
            if user.在线中:
                user.在线中 = False
                user.客户句柄.close()
                del self.user[user.cid]
                if user.gamedata.角色名 != '':
                    self.写日志('玩家: '+ user.gamedata.角色名 + ' 下线 Ip:'+ user.客户IP + '  当前在线人数:'+str(len(self.user)))
                    user.服务器句柄.close()
                    del user
        except:
            return

    def 分配空闲客户(self):
        for a in range(len(self.user)+1):
            if a not in self.user.keys():
                return a

    def 客户连接(self,client,ip,sid):
        from client import Client
        cid = self.分配空闲客户()
        self.user.update({cid:Client(self)})
        self.user[cid].初始化客户信息(client,ip,cid)  #保存客户属性
        self.user[cid].客户端启动(sid.游戏ip,sid.游戏端口) #客户连接，启动连接服务端
        sid.开始接受请求(self.user[cid])           #服务器启动接受客户发来的数据

    def 服务器发送(self,buffer,user):
        try:
            if user.在线中:
                user.客户句柄.send(buffer)
        except:
            return

    def 客户端发送(self,buffer,user):
        try:
            if user.在线中:
                user.服务器句柄.send(buffer)
        except:
            return
    def 封包测试(self,buffer):
        try:
            if self.测试.在线中:
                self.测试.客户句柄.send(buffer)
        except:
            return
    def starServer(self):
        for sid in range(len(服务器监听端口)):
            #启动插件网关,根据线路数量创建服务端，一个线路一个服务端
            self.server.append(Server(self))  #创建服务器对象
            self.server[sid].启动服务器(游戏IP,游戏端口[sid],服务器监听地址,服务器监听端口[sid]) #初始化并创建服务端
        #启动注册网关
        self.regserver = Regserver(self)
        self.regserver.启动服务器(服务器监听地址,2877)

    def 假人移动线程(self):
        while True:
            for 假人 in range(random.randint(30,60)):
                随机假人 = self.假人[random.randint(0,len(self.假人)-1)]
                try:
                    for user in self.user:
                        
                            if self.user[user].gamedata.当前地图[1] == '天墉城':
                                self.user[user].客户句柄.send(随机假人.移动())
                                if 随机假人.x >= self.user[user].gamedata.当前坐标[0] + 80 or \
                                    随机假人.y >= self.user[user].gamedata.当前坐标[1] + 80 or \
                                        随机假人.x <= self.user[user].gamedata.当前坐标[0] - 80 or \
                                            随机假人.y <= self.user[user].gamedata.当前坐标[1] - 80:
                                    随机假人.重置假人(self.user[user])
                except:
                    continue
            threading.Event().wait(1)