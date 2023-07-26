from setting import *
from threading import Thread as 线程,Timer
from sendToClient import SendToClient


class 客户端数据处理:
    from xyplugin import 逍遥插件
    '''客户端数据处理类，负责处理服务器发来的数据'''
    def __init__(self,server:逍遥插件) -> None:
        self.未发送 = bytes()
        self.server = server
    from client.client import Client
    def 接收处理线程(self,user:Client):
        while user.未发送[:2] == b'MZ':
            leng = int.from_bytes(user.未发送[8:10])
            if len(user.未发送) - 10 >= leng:
                buffer = user.未发送[:leng+10]
                user.未发送 = user.未发送[leng + 10:]
                请求处理线程 = 线程(target=self.接收处理中心,args=(buffer,user))
                请求处理线程.daemon = True
                请求处理线程.start()
                continue
            break

    def 接收处理中心(self,buffer:bytes,user:Client):
        客户接收处理 = SendToClient(user,self.server)
        包头 = buffer[10:12]
        if 包头.hex() == "3357":
            buffer = 客户接收处理.登录线路(buffer)
        elif 包头.hex() == "4355":
            buffer = 客户接收处理.显示线路(buffer)
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
            if user.gamedata.屏蔽垃圾:
                buffer = b''
        elif 包头.hex() == 'fff9':
                客户接收处理.周围对象读取(buffer)
        elif 包头.hex() == '1043':
                user.gamedata.参战宠物id = int.from_bytes(buffer[12:16])
        elif 包头.hex() == '1deb':
            if buffer[19:20].hex() == '19':
                if user.fuzhu.自动战斗.开关:
                #buffer = self.server.基础功能.战斗时间(buffer)
                    t1 = Timer(2,user.fuzhu.自动战斗.开始战斗)
                    t1.start()
        elif 包头.hex() == 'fdf9':
            if user.fuzhu.自动战斗.开关:
                user.fuzhu.自动战斗.置攻击位置id(buffer)
        elif 包头.hex() == '1df5':
            if user.fuzhu.自动战斗.开关:
                user.fuzhu.自动战斗.删攻击id(buffer)
        elif 包头.hex() == 'ffe1':
            客户接收处理.地图事件(buffer)
        elif 包头.hex() == 'f061':
            客户接收处理.取角色gid(buffer)
        elif 包头.hex() == '2301' and user == self.server.GM.GMUSER:
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
            if user.fuzhu.自动战斗.开关:
                t = 线程(target=user.fuzhu.自动战斗.补充状态())
                t.start()
        elif 包头.hex() == '402f':
           客户接收处理.读当前坐标(buffer)
        try:
            if len(buffer) != 0 and user.客户句柄 != 0:
                user.客户句柄.send(buffer)
        except:
            user.客户句柄.close()
