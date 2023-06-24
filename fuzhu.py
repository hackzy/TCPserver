from luzhi import Luzhi
from autoFired import 自动战斗
from xiaozhushou import XiaoZhuShou
from bufferWrit import 写封包
from setting import *
class fuzhu:
    def __init__(self,server,user) -> None:
        self.luzhi = Luzhi(server,user)
        self.自动战斗 = 自动战斗(server,user)
        self.小助手 = XiaoZhuShou(server,user)
        self.鉴定类型 = ''
        self.user = user
        self.server = server

    def 血蓝位置(self):
        for a in self.user.gamedata.物品数据:
            if a.名称.find('法玲瓏') != -1:
                法玲珑 = a.位置id
            if a.名称.find('血玲瓏') != -1:
                血玲珑 = a.位置id
            if a.名称.find('馴獸訣') != -1:
                驯兽诀 = True
        if 法玲珑 == 0:
            self.server.基础功能.商城购买道具(self.user,'特級法玲瓏')
            for a in self.user.gamedata.物品数据:
                if a.名称.find('法玲瓏') != -1:
                    法玲珑 = a.位置id
        if 血玲珑 == 0:
            self.server.基础功能.商城购买道具(self.user,'特級血玲瓏')
            for a in self.user.gamedata.物品数据:
                if a.名称.find('血玲瓏') != -1:
                    血玲珑 = a.位置id
        if 驯兽诀 == False:
            self.server.基础功能.商城购买道具(self.user,'高級馴獸訣')
        return 血玲珑,法玲珑
    
    def 人物回复(self):
        写 = 写封包()
        完整包 = 写封包()
        血玲珑,法玲珑 = self.血蓝位置()
        写.写字节集(bytes.fromhex('202c'))
        写.写字节型(法玲珑.to_bytes(1))
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        写 = 写封包()
        写.写字节集(bytes.fromhex('202c'))
        写.写字节型(血玲珑.to_bytes(1))
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        for a in range(3):
            self.server.客户端发送(完整包.取数据(),self.user)
            #print(self.user.gamedata.最大气血,self.user.gamedata.最大法力)
    def 宠物回复(self):
        try:
            写 = 写封包()
            完整包 = 写封包()
            血玲珑,法玲珑 = self.血蓝位置()
            写.写字节集(bytes.fromhex('204e'))
            写.写字节型(self.user.gamedata.pet[self.user.gamedata.参战宠物id].位置.to_bytes(1))
            写.写字节型(血玲珑.to_bytes(1))
            完整包.写字节集(组包包头)
            完整包.写字节集(写.取数据(),True,1)
            写 = 写封包()
            写.写字节集(bytes.fromhex('204e'))
            写.写字节型(self.user.gamedata.pet[self.user.gamedata.参战宠物id].位置.to_bytes(1))
            写.写字节型(法玲珑.to_bytes(1))
            完整包.写字节集(组包包头)
            完整包.写字节集(写.取数据(),True,1)
            if self.user.gamedata.pet[self.user.gamedata.参战宠物id].忠诚 < 80:
                    写 = 写封包()
                    写.写字节集(bytes.fromhex('109a'))
                    写.写整数型(self.user.gamedata.参战宠物id,True)
                    完整包.写字节集(组包包头)
                    完整包.写字节集(写.取数据(),True,1)
            for a in range(3):
                self.server.客户端发送(完整包.取数据(),self.user)
        except:
            return