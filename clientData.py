from setting import *
from threading import Thread as 线程,Timer
from sendToClient import 客户接收处理
from recBuffer import 读封包
from bufferWrit import 写封包
class 客户端数据处理:
    '''客户端数据处理类，负责处理服务器发来的数据'''
    def __init__(self,user,server) -> None:
        self.未发送 = bytes()
        self.user = user
        self.server = server
        self.客户接收处理 = 客户接收处理(user,server)

    def 接收处理线程(self,user):
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

    def 接收处理中心(self,buffer):
        包头 = buffer[10:12]
        if 包头.hex() == "3357":
            buffer = self.客户接收处理.登录线路(buffer)
        elif 包头.hex() == "4355":
            buffer = self.客户接收处理.显示线路(buffer)
        elif 包头.hex() == '20d7':
            buffer = self.客户接收处理.切换角色(buffer)
        elif 包头.hex() == 'fff5':
            self.客户接收处理.背包读取(buffer)
        elif 包头.hex() == 'fff7':
            self.客户接收处理.人物属性读取(buffer)
        elif 包头.hex() == '7feb':
            self.客户接收处理.技能读取(buffer)
        elif 包头.hex() == 'fff1':
            #屏蔽垃圾
            buffer = b''
        elif 包头.hex() == 'fff9':
                self.客户接收处理.周围对象读取(buffer)
        elif 包头.hex() == '1043':
            self.user.gamedata.参战宠物id = int.from_bytes(buffer[12:16])
        elif 包头.hex() == '1deb':
            if self.user.fuzhu.自动战斗.开关:
                #buffer = self.server.基础功能.战斗时间(buffer)
                t1 = Timer(3,self.user.fuzhu.自动战斗.开始战斗)
                t1.start()
        elif 包头.hex() == 'fdf9':
            self.user.fuzhu.自动战斗.置攻击位置id(buffer)
        elif 包头.hex() == '1df5':
            self.user.fuzhu.自动战斗.删攻击id(buffer)
        elif 包头.hex() == 'ffe1':
            self.客户接收处理.地图事件(buffer)
        elif 包头.hex() == 'f061':
            self.客户接收处理.取角色gid(buffer)
        elif 包头.hex() == '2301' and self.user == self.server.GM.GMUSER:
            self.server.GM.元宝寄售(buffer)
        elif 包头.hex() == 'fdd1':
            self.客户接收处理.战斗对话(buffer)
        try:
            if len(buffer) != 0 and self.user.客户句柄 != 0:
                self.user.客户句柄.send(buffer)
        except:
            self.user.客户句柄 = 0
