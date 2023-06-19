from setting import *
from ServerData import 服务器数据处理
import datetime
from client import Client
import datetime
import logging
from otherKing import 基础功能
class 逍遥插件:
    '''全局管理类，负责保存分配客户与服务端信息'''
    def __init__(self) -> None:
      self.server = []
      self.client = []
      self.sid = 0
      self.user = {}
      self.基础功能 = 基础功能()
    
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
        print(s+"\n")

    def 分配空闲客户(self):
        for a in range(len(self.user)+1):
            if a not in self.user.keys():
                return a

    def 启动客户端(self,client,ip,sid):
        cid = self.分配空闲客户()
        self.user.update({cid:Client(self)})
        self.user[cid].初始化客户信息(client,ip[0],sid)  #保存客户属性
        self.user[cid].客户端启动(self.server[sid].游戏IP,self.server[sid].游戏端口) #客户连接，启动连接服务端
        self.server[sid].开始接受请求(self.user[cid])           #服务器启动接受客户发来的数据
        self.写日志('有客户进入，当前客户数：{}，IP：{}'.format(len(self.client),ip[0]))

    def 服务器发送(self,buffer):
        self.user.客户句柄.send(buffer)

    def 客户端发送(self,buffer):
        self.user.服务器句柄.send(buffer)

if __name__== '__main__':
    '服务器启动'
    server = 逍遥插件() #创建全局对象
    for id in range(len(服务器监听端口)):           #根据线路数量创建服务端，一个线路一个服务端
        server.server.append(服务器数据处理(server))  #创建服务器管理对象
        server.server[id].启动服务器(id,游戏IP,游戏端口[id],服务器监听端口[id]) #初始化并创建服务端

    m = input()