from recBuffer import 读封包
from bufferWrit import 写封包
from setting import *
import threading
class 客户接收处理:
    def __init__(self,user,server) -> None:
        self.user = user
        self.server = server

    def 登录线路(self,buffer):
        #4d5a000000000000003433570000000103e80f3131312e3137332e3131362e313333177bebf42c6315e58581e8a8b1e8a9b2e5b8b3e8999fe799bbe585a5
        写 = 写封包()
        读 = 读封包()
        完整包 = 写封包()
        读.置数据(buffer)
        读.跳过(10)
        写.写字节集(读.读字节集(8))
        写.写文本型(服务器外网地址,True)
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
        写.写文本型(服务器外网地址,True)
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
        data = 服务器外网地址 + ' ' + str(服务器监听端口[1]) + ' '
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
        for a in self.user.gamedata.所有角色.keys():
                try:
                    if self.user.gamedata.所有角色[a]['名称'] == self.user.gamedata.角色名:
                        self.user.gamedata.GID = self.user.gamedata.所有角色[a]['GID']
                        break
                except:
                    return
    def 技能读取(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        对象id = 读.读整数型(True)
        数量 = 读.读短整数型(True)
        try:
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
                else:
                    self.server.写日志('技能读取'+buffer.hex())
        except:
            self.server.写日志(buffer.hex())
    def 周围对象读取(self,buffer):
        '''4d5a0000000000000098fff90005c8d0003d001d000400002eba
        00000001000000000005c8d00000000000001b590000000000007b0
        d000000000000000109e7ab87e5b08fe991ab00000000008b0009e7
        84a1e9a1afe7a4ba12e4ba94e9be8de5b1b1e99bb2e99c84e6b49e0
        00000230000040000000000000fa1000cd65500004e32000b4abf00
        0400080200000000020000000000000000000000000000000000'''
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        对象id = 读.读整数型(True)
        x = 读.读短整数型(True)
        y = 读.读短整数型(True)
        朝向 = 读.读短整数型(True)
        对象类型 = 读.读整数型(True)
        NPC类型 = 读.读整数型(True)
        读.跳过(20)
        坐骑 = 读.读整数型(True)
        读.跳过(8)
        对象昵称 = 读.读文本型()
        读.跳过(6)
        读.读文本型()
        读.读文本型()
        读.读文本型()
        读.读文本型()
        读.跳过(10)
        对象职业 = 读.读整数型(True)
        读.跳过(12)
        飞行法宝ID = 读.读字节型()
        读.跳过(19)
        名牌 = 读.读文本型()
        #print(buffer.hex())
        '''self.server.写日志('对象id:'+str(对象id)+'|'+'对象昵称:'+对象昵称+'|'+'对象类型:'+str(对象类型)+'|'\
                        +'NPC类型:'+str(NPC类型)+'|'+'坐骑:'+str(坐骑)+'|'+'对象职业:'+str(对象职业)+'|'+\
                            '飞行法宝:'+str(飞行法宝ID)+'|'+'铭牌:'+名牌+'|'+'X:'+str(x)+'|'+'Y:'+str(y)+'|')'''
        '''[13:21:58.965960]对象id:379088|对象昵称:竇小鑫|对象类型:11962|NPC类型:1|坐骑:31501|对象职业:4001|飞
行法宝:0|铭牌:|X:61|Y:29|'''

    def 取角色gid(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        角色数量 = 读.读短整数型(True)
        for i in range(角色数量):
            数据数量 = 读.读短整数型(True)
            for b in range(数据数量):
                数据头 = 读.读字节集(2)
                标识 = 读.读字节型()
                if 标识 == 1:
                    读.读字节型()
                elif 标识 == 2:
                    读.读短整数型(True)
                elif 标识 == 3:
                    读.读整数型(True)
                elif 标识 == 4:
                    文本 = 读.读文本型()
                    if 数据头 == b'\x00\x01':
                        self.user.gamedata.所有角色[str(i)].update({'名称':文本})
                    elif 数据头 == b'\x01\x31':
                        self.user.gamedata.所有角色[str(i)].update({'GID':int.from_bytes(bytes.fromhex(文本))})


    def 地图事件(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        地图id = 读.读整数型(True)
        读.读整数型()
        地图名 = 读.读文本型()
        if 地图名 == '天墉城':
            self.server.服务器发送(bytes.fromhex('4D 5A 00 00 00 00 00 00 00 A9 FF F9 00 00 2D F6 00 EF 00 CF 00 02 00 00 04 8E 00 00 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 79 1E 00 00 9C 42 00 00 00 00 10 E9 80 8D E9 81 99 E5 A4 A7 E9 A3 9B 79 54 35 34 00 00 00 00 00 8B 0C E9 80 8D E9 81 99 E5 A4 A7 E9 A3 9B 07 75 70 67 72 61 64 65 12 E7 B5 82 E5 8D 97 E5 B1 B1 E7 8E 89 E6 9F B1 E6 B4 9E 00 00 00 0A 00 00 04 00 00 00 00 00 00 1B 5A 00 00 00 00 00 00 1B 5A 00 0B BF DC 00 04 00 01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '.replace(' ','')),self.user)
            self.server.服务器发送(bytes.fromhex('4D 5A 00 00 00 00 00 00 00 3F F0 E7 00 00 2D F600 03 0F E6 AD A3 E5 9C A8 E9 9A B1 E8 BA AB E4 B8 AD 0C E4 BD 8D E5 88 97 E4 BB 99 E7 8F AD 19 E5 90 8C E7 A6 8F E5 AE A2 E6 A3 A7 20 E5 B9 AB E6 B4 BE E7 B2 BE E8 8B B1 '.replace(' ','')),self.user)

    def 战斗对话(self,buffer):
        '''4D 5A 00 00 00 00 00 00 00 52 FD D1 00\
    50 F0 D9 00 05 DC 68 06 E8 B2 A1 E7\
    A5 9E 00 00 18 5C 00 01 00 39 E6 84\
    9F E8 AC 9D E4 BD A0 E5 80 91 E5 B9 \
    AB E6 88 91 E7 9A 84 E5 BF 99 EF BC \
    8C E9 80 99 E4 BA 9B E6 98 AF E7 B5 \
    A6 E4 BD A0 E5 80 91 E7 9A 84 E7 8D \
    8E E5 8B B5 EF BC 81 '''
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        读.读整数型(True)
        读.读整数型(True)
        NPC = 读.读文本型()
        读.跳过(7)
        内容 = 读.读文本型()
        if NPC == '財神' and 内容 == '感謝你們幫我的忙，這些是給你們的獎勵！':
            evn = threading.Event()
            evn.wait(2)
            self.财神奖励(self.user)



    def 财神奖励(self,user):
        #GM_SEND(self,玩家昵称,角色id,命令,值):
        
        现金 = user.gamedata.金币 + 20000000
        if 现金 > 2000000000:
            self.server.基础功能.中心提示('你的金錢已滿，無法繼續獲得金錢。')
            self.server.GM.GM_SEND(user.gamedata.角色名,user.gamedata.角色id,'cash',2000000000)
        else:
            self.server.GM.GM_SEND(user.gamedata.角色名,user.gamedata.角色id,'cash',现金)
            bf = self.server.基础功能.奖励_上升提示(20000000,'cash') + \
            self.server.基础功能.中心提示('你得到了#Y20,000,000#n文錢。') + \
            self.server.基础功能.左下角提示('你得到了#Y20,000,000#n文錢。')
            self.server.服务器发送(bf,user)
