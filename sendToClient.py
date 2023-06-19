from recBuffer import 读封包
from bufferWrit import 写封包
from setting import *
class 客户接收处理:
    def __init__(self,user) -> None:
        self.user = user

    def 登录线路(self,buffer):
        #4d5a000000000000003433570000000103e80f3131312e3137332e3131362e313333177bebf42c6315e58581e8a8b1e8a9b2e5b8b3e8999fe799bbe585a5
        写 = 写封包()
        读 = 读封包()
        完整包 = 写封包()
        读.置数据(buffer)
        读.跳过(10)
        写.写字节集(读.读字节集(8))
        写.写文本型(服务器监听地址,True)
        写.写短整数型(服务器监听端口[1],True)
        读.读文本型()
        读.读字节集(2)
        写.写字节集(读.剩余数据())
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        return 完整包.取数据()
    
    def 显示线路(self,buffer):
        #4D 5A 00 00 00 00 00 00 00 23 43 55 00 01 06 E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C E4 B8 80 E7 B7 9A 09 31 32 37 2E 30 2E 30 2E 31 00 02 
        写 = 写封包()
        读 = 读封包()
        完整包 = 写封包()
        读.置数据(buffer)
        读.跳过(10)
        写.写字节集(读.读字节集(4))
        写.写文本型(读.读文本型(),True)
        写.写文本型(服务器监听地址,True)
        写.写短整数型(2,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        return 完整包.取数据()
    
    def 切换角色(self,buffer):
        读 = 读封包()
        写 = 写封包()
        完整包 = 写封包()
        读.置数据(buffer)
        读.跳过(10)
        写.写字节集(读.读字节集(4))
        data = 读.读文本型()
        stri = data.split(" ")
        data = 服务器监听地址 + ' ' + str(服务器监听端口[1]) + ' '
        for i in range(len(stri) - 2):
            data = data + stri[i + 2] + ' '
        data = data[:len(data) - 1]
        写.写文本型(data,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1,True)
        return 完整包.取数据()

    def 背包读取(self,buffer):
        写 = 写封包()
        读 = 读封包()
        保存包 = 写封包()
        读.置数据(buffer)
        读.跳过(10)
        写.写字节集(读.读字节集(2))
        物品总数 = 读.读短整数型(True)
        写.写短整数型(物品总数,True)
        for i in range(物品总数):
            物品位置id = 读.读字节型()
            if 物品位置id == 32:
                物品位置id = 55
            写.写字节型(物品位置id.to_bytes(1))
            物品数据总数 = 读.读短整数型(True)
            if 物品数据总数 == 0:
                写.写短整数型(物品数据总数,True)
            保存包.清数据()
            保存包.写短整数型(物品数据总数,True)
            for a in range(物品数据总数):
                物品属性类别 = 读.读短整数型(True)
                保存包.写短整数型(物品属性类别,True)
                物品属性数量 = 读.读短整数型(True)
                if 物品位置id == 33 or 物品位置id == 31:
                    保存包.写短整数型(物品属性数量 + 1,True)
                    保存包.写字节集(bytes.fromhex('038e0101'))
                    保存包.写短整数型(物品属性数量,True)
                else:
                    for b in range(物品属性数量):
                        属性标识 = 读.读字节集(2)
                        数据类型 = 读.读字节型()
                        保存包.写字节集(属性标识)
                        保存包.写字节型(数据类型.to_bytes())
                        if 数据类型 == 1:
                            T_字节型 = 读.读字节型()
                            if 属性标识 == b'\x01\x79' and 是否封印 == False \
                            and T_字节型 == 1:
                                是否封印 = True
                            保存包.写字节型(T_字节型.to_bytes())
                        elif 数据类型 == 2:
                            T_短整数型 = 读.读短整数型(True)
                            写.写短整数型(T_短整数型)
                        elif 数据类型 == 3:
                            T_整数型 = 读.读整数型(True)
                            保存包.写整数型(T_整数型)
                            if 属性标识 == b'\x02\x71':
                                pass
                            if 属性标识 == b'\x00\x84':
                                self.user.gamedata.物品数据.物品列表[物品位置id]\
                                = {'物品id':T_整数型}
                        elif 数据类型 == 4:
                            T_文本型 = 读.读文本型()
                            保存包.写文本型(T_文本型,True)
                            if 属性标识 == b'\x00\x01':
                                self.user.gamedata.物品数据.物品列表[物品位置id]\
                                = {'物品名称':T_文本型}
                        elif 数据类型 == 6:
                            T_字节型 = 读.读字节型()
                            if 属性标识 == b'\x00\x202':
                                self.user.gamedata.物品数据.物品列表[物品位置id]\
                                = {'物品类型':T_字节型}
                        elif 数据类型 == 7:
                            T_短整数型 = 读.读短整数型(True)
                            保存包.写短整数型(T_短整数型,True)
                    self.user.gamedata.物品数据.物品列表[物品位置id]\
                    = {'封包缓存':保存包.取数据()}
        
    def 人物属性读取(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(10)
        读.读字节集(2)
        self.user.gamedata.角色id = 读.读整数型(True)
        数量 = 读.读短整数型(True)
        for a in range(数量):
            数据头 = 读.读字节集(2).hex()
            标识 = 读.读字节型()
            if 标识 == 1:
                读.读字节型()
            elif 标识 == 2:
                T_短整数型 = 读.读短整数型(True)
                if 数据头 == '002c':
                    self.user.gamedata.五行 = T_短整数型
                elif 数据头 == '001f':
                    self.user.gamedata.等级 = T_短整数型
            elif 标识 == 3:
                T_整数型 = 读.读整数型(True)
                if 数据头 == '001b':
                    self.user.gamedata.金币 = T_整数型
                elif 数据头 == '013e':
                    self.user.gamedata.代金券 = T_整数型
                elif 数据头 == '0077':
                    self.user.gamedata.银元宝 = T_整数型
                elif 数据头 == '0078':
                    self.user.gamedata.金元宝 = T_整数型
                elif 数据头 == '0056':
                    self.user.gamedata.形象id = T_整数型
                elif 数据头 == '001a':
                    self.user.gamedata.潜能 = T_整数型
                elif 数据头 == '0014':
                    self.user.gamedata.道行 = T_整数型
                elif 数据头 == '0019':
                    self.user.gamedata.经验 = T_整数型
                elif 数据头 == '0006':
                    self.user.gamedata.当前气血 = T_整数型
                elif 数据头 == '000b':
                    self.user.gamedata.当前法力 = T_整数型
                elif 数据头 == '004b':
                    self.user.gamedata.战绩 = T_整数型
                elif 数据头 == '0079':
                    self.user.gamedata.血池 = T_整数型
                elif 数据头 == '007a':
                    self.user.gamedata.灵池 = T_整数型
            elif 标识 == 4:
                T_文本型 = 读.读文本型()
                if 数据头 == '0051':
                    self.user.gamedata.门派 = T_文本型
                elif 数据头 == '001e':
                    self.user.gamedata.师尊 = T_文本型
                elif 数据头 == '0001':
                    self.user.gamedata.角色名 = T_文本型

    def 技能读取(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        对象id = 读.读整数型(True)
        数量 = 读.读短整数型(True)
        for a in range(数量):
            技能id = 读.读短整数型(True)
            读.跳过(4)
            技能名称 = 读.读文本型(True)
            读.跳过(2)
            技能等级 = 读.读短整数型(True)
            读.跳过(29)
            标识 = 读.读字节集(2).hex()
            if 标识 == '0104':
                读.跳过(13)
            elif 标识 == '0106':
                读.跳过(15)
            elif 标识 == '0203':
                读.跳过(23)
                if 对象id not in self.user.gamedata.技能:
                    self.user.gamedata.技能.update({对象id:{技能名称:技能id}})
                else:
                    self.user.gamedata.技能[对象id].update({技能名称:技能id})

    def 周围对象显示(self):
        读 = 读封包()
