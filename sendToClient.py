from recBuffer import 读封包
from bufferWrit import 写封包
from itemData import 背包数据
from setting import *
import threading
from petData import petdata
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
            temp = {物品位置id:背包数据()}
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
                            if 属性标识 == b'\x01\x4f'  \
                            and T_字节型 == 1:
                                是否封印 = True
                            保存包.写字节型(T_字节型.to_bytes())
                        elif 数据类型 == 2:
                            T_短整数型 = 读.读短整数型(True)
                            写.写短整数型(T_短整数型)
                        elif 数据类型 == 3:
                            T_整数型 = 读.读整数型(True)
                            保存包.写整数型(T_整数型)
                            if 属性标识 == b'\x02\x47':
                                pass
                            if 属性标识 == b'\x00\x54':
                                temp[物品位置id].id = T_整数型
                        elif 数据类型 == 4:
                            T_文本型 = 读.读文本型()
                            保存包.写文本型(T_文本型,True)
                            if 属性标识 == b'\x00\x01':
                                temp[物品位置id].名称 = T_文本型
                        elif 数据类型 == 6:
                            T_字节型 = 读.读字节型()
                            if 属性标识 == b'\x00\xca':
                                temp[物品位置id].类型 = T_字节型
                        elif 数据类型 == 7:
                            T_短整数型 = 读.读短整数型(True)
                            保存包.写短整数型(T_短整数型,True)
                    temp[物品位置id].封包缓存 = 保存包.取数据()
            self.user.gamedata.物品数据.update(temp)

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
                elif 数据头 == '0007':
                    self.user.gamedata.最大气血 = T_整数型
                elif 数据头 == '000c':
                    self.user.gamedata.最大法力 = T_整数型
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
                    return
        except:
            #self.server.写日志(buffer.hex())
            return
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
        self.user.gamedata.上一地图 = self.user.gamedata.当前地图[1]
        self.user.gamedata.当前地图 = [地图id,地图名]
        self.user.gamedata.当前坐标[0] = 读.读短整数型(True)
        self.user.gamedata.当前坐标[1] = 读.读短整数型(True)
        if 地图名 == '天墉城':
            地图所有 = threading.Thread(target=self.假人线程,args=('所有',))
            地图所有.start()
            self.假人所有 = True
            self.假人擂台 = False
            self.假人商会 = False
            self.假人拍卖行 = False
            if self.user.gamedata.当前坐标[0] <= 355 and self.user.gamedata.当前坐标[0] >= 255 and \
                self.user.gamedata.当前坐标[1] <= 255 and self.user.gamedata.当前坐标[1] >= 155:
                地图擂台 = threading.Thread(target=self.假人线程,args=('擂台',))
                地图擂台.start()
                self.假人擂台 = True
                self.假人商会 = False
                self.假人拍卖行 = False
            elif self.user.gamedata.当前坐标[0] <= 324 and self.user.gamedata.当前坐标[0] >= 224 and \
                self.user.gamedata.当前坐标[1] <= 261 and self.user.gamedata.当前坐标[1] >= 121:
                地图商会 = threading.Thread(target=self.假人线程,args=('商会',))
                地图商会.start()
                地图活动大使 = threading.Thread(target=self.假人线程,args=('活动大使',))
                地图活动大使.start()
                self.假人擂台 = False
                self.假人商会 = True
                self.假人拍卖行 = False

            elif self.user.gamedata.当前坐标[0] <= 227 and self.user.gamedata.当前坐标[0] >= 187 and \
                self.user.gamedata.当前坐标[1] <= 120 and self.user.gamedata.当前坐标[1] >= 80:
                地图拍卖 = threading.Thread(target=self.假人线程,args=('拍卖',))
                地图拍卖.start()
                self.假人擂台 = False
                self.假人商会 = False
                self.假人拍卖行 = True
        elif 地图名 == '幽雅小居' or 地图名 == '豪華居所' \
            or 地图名 == '花園別墅' or 地图名 == '翡翠莊園':
            self.user.gamedata.屏蔽垃圾 = False
        else:
            self.user.gamedata.屏蔽垃圾 = True
            if self.user.gamedata.上一地图 == '天墉城':
                删除假人 = threading.Thread(target=self.假人删除线程)
                删除假人.start()
                '''for 假人 in self.server.假人:
                    self.server.服务器发送(假人.删除假人(),self.user)
                threading.Event().wait(1)
                if self.假人擂台:
                    for 擂台假人 in self.server.擂台假人:
                        self.server.服务器发送(擂台假人.删除假人(),self.user)
                if self.假人商会:
                    for 商会假人 in self.server.商会假人:
                        self.server.服务器发送(商会假人.删除假人(),self.user)
                    for 活动大使假人 in self.server.活动大使假人:
                        self.server.服务器发送(活动大使假人.删除假人(),self.user)
                if self.假人擂台:
                    for 拍卖行假人 in self.server.拍卖行假人:
                        self.server.服务器发送(拍卖行假人.删除假人(),self.user)
            '''
    def 假人线程(self,假人类型):
        for a in range(50):
            if 假人类型 == '所有':
                temp = self.server.假人[a*50:a*50+50]
            elif 假人类型 == '擂台':
                temp = self.server.擂台假人[a*50:a*50+50]
            elif 假人类型 == '商会':
                temp = self.server.商会假人[a*50:a*50+50]
            elif 假人类型 == '拍卖':
                temp = self.server.拍卖行假人[a*50:a*50+50]
            elif 假人类型 == '活动大使':
                temp = self.server.活动大使假人[a*50:a*50+50]
            for i in temp:
                self.server.服务器发送(i.属性封包(),self.user)
                self.server.服务器发送(i.显示(),self.user)
            #threading.Event().wait(30)

    def 假人删除线程(self):
        for 假人 in self.server.假人:
            self.server.服务器发送(假人.删除假人(),self.user)
        if self.假人擂台:
            for 擂台假人 in self.server.擂台假人:
                self.server.服务器发送(擂台假人.删除假人(),self.user)
            threading.Event().wait(2)
        if self.假人商会:
            for 商会假人 in self.server.商会假人:
                self.server.服务器发送(商会假人.删除假人(),self.user)
            threading.Event().wait(2)
            for 活动大使假人 in self.server.活动大使假人:
                self.server.服务器发送(活动大使假人.删除假人(),self.user)
            threading.Event().wait(2)
        if self.假人擂台:
            for 拍卖行假人 in self.server.拍卖行假人:
                self.server.服务器发送(拍卖行假人.删除假人(),self.user)
            threading.Event().wait(2)

    def 战斗对话(self,buffer):
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

    def 商城读取(self,buffer):
        '''00 01 00 01 00 05 00 01 04 0C E5 BE A1 E9 9D 88 E7 B3 A7 E8 A2 8B 00 28 03 00 00 23 83 01 37 04 03 E5 80 8B 00 CB 02 00 01 00 C9 04 00 09 43 30 30 30 30 30 30 30 39 00 01 00 06 00 09 02 00 00 00 64 00 00 00 00 00 00 00 00 00 00 '''
        '''00 01 00 01 00 05 00 01 04 0F E4 B8 80 E7 99 BE E4 B8 80 E8 A1 A3 00 28 03 00 00 06 13 01 37 04 03 E5 80 8B 00 CB 02 00 01 00 C9 04 33 E6 89 93 E9 96 8B E5 BE 8C E5 8F AF E4 BB A5 E7 8D B2 E5 BE 97 E8 A1 A3 E6 9C 8D E6 BB BF E5 B1 AC E6 80 A7 E8 B6 85 E7 B4 9A E9 BB 91 E6 B0 B4 E6 99 B6 09 54 30 30 30 30 30 30 31 38 00 01 00 01 00 12 01 00 00 00 01 00 00 00 00 00 00 00 00 00 00'''
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        数量 = 读.读短整数型(True)
        for a in range(数量):
            读.读短整数型()
            读.读短整数型()
            数据数量 = 读.读短整数型(True)
            for b in range(数据数量):
                数据头 = 读.读短整数型(True)
                标识 = 读.读字节型()
                if 标识 == 4:
                    文本 = 读.读文本型()
                    if 数据头 == 1:
                        道具名称 = 文本
                elif 标识 == 3:
                    读.读整数型(True)
                elif 标识 == 2:
                    读.读短整数型(True)
                elif 标识 == 1:
                    读.读字节型()
            道具id = 读.读文本型()
            读.跳过(6)
            元宝类型 = 读.读字节型()
            if 元宝类型 == 1 or 元宝类型 == 3:
                self.user.gamedata.商城数据.update({道具名称:[道具id,'gold_coin']})
            else:
                self.user.gamedata.商城数据.update({道具名称:[道具id,'silver_coin']})
            读.跳过(14)

    def NPC对话(self,buffer):
        读 = 读封包()
        写 = 写封包()
        完整包 = 写封包()
        读.置数据(buffer)
        读.跳过(10)
        写.写字节集(读.读字节集(2))
        NPCid = 读.读整数型(True)
        写.写整数型(NPCid,True)
        写.写整数型(读.读整数型(True),True)
        写.写字节集(读.读字节集(2))
        对话内容 = 读.读文本型(True,1,True)
        if self.user.fuzhu.鉴定类型 != '':
            if 对话内容.find('鑒定符') != -1:
                self.user.fuzhu.鉴定二级对话(NPCid,对话内容)
                return b''
        写.写文本型(对话内容,True,1,True)
        写.写字节集(读.读字节集(4))
        写.写文本型(读.读文本型(),True)
        写.写字节集(读.剩余数据())
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        return 完整包.取数据()

    def 宠物读取(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(14)
        位置id = 读.读字节型()
        id = 读.读整数型(True)
        self.user.gamedata.pet.update({id:petdata()})
        self.user.gamedata.pet[id].位置 = 位置id
        数量 = 读.读短整数型(True)
        for a in range(数量):
            读.读字节集(2)
            属性数量 = 读.读短整数型(True)
            for b in range(属性数量):
                数据头 = 读.读字节集(2)
                标识 = 读.读字节型()
                if 标识 == 1:
                    T_字节型 = 读.读字节型()
                elif 标识 == 2:
                    T_短整数型 = 读.读短整数型(True)
                elif 标识 == 3:
                    T_整数型 = 读.读整数型(True)
                    if 数据头.hex() == '0006':
                        self.user.gamedata.pet[id].当前气血 = T_整数型
                    elif 数据头.hex() == '000b':
                        self.user.gamedata.pet[id].当前法力 = T_整数型
                    elif 数据头.hex() == '0007':
                        self.user.gamedata.pet[id].最大气血 = T_整数型
                    elif 数据头.hex() == '000c':
                        self.user.gamedata.pet[id].最大法力 = T_整数型
                    elif 数据头.hex() == '0042':
                        self.user.gamedata.pet[id].忠诚 = T_整数型
                elif 标识 == 4:
                    T_文本型 = 读.读文本型()
                    if 数据头.hex() == '0001':
                        self.user.gamedata.pet[id].昵称 = T_文本型
                elif 标识 == 6:
                    读.读字节型()
                elif 标识 == 7:
                    读.读短整数型(True)
            
    def 宠物数据更新(self,buffer):
        '''4d5a000000000000001610ec00010400052f710001000100010042030000005b'''
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(14)
        位置 = 读.读字节型()
        id = 读.读整数型(True)
        读.读短整数型(True)
        读.读短整数型(True)
        读.读短整数型(True)
        数据头 = 读.读字节集(2)
        标识 = 读.读字节型()
        if 标识 == 1:
            读.读字节型()
        elif 标识 == 2:
            读.读短整数型(True)
        elif 标识 == 3:
            整数 = 读.读整数型(True)
            if 数据头.hex() == '0006':
                self.user.gamedata.pet[id].气血 = 整数
            elif 数据头.hex() == '000b':
                self.user.gamedata.pet[id].法力 = 整数
            elif 数据头.hex() == '0042':
                self.user.gamedata.pet[id].忠诚 = 整数
            elif 标识 == 4:
                文本 = 读.读文本型()
                if 数据头.hex() == '0001':
                    self.user.gamedata.pet[id].昵称 = 文本

    def 读当前坐标(self,buffer:bytes):
        recBuffer = 读封包()
        recBuffer.置数据(buffer)
        recBuffer.跳过(12)
        id = recBuffer.读整数型(True)
        if id == self.user.gamedata.角色id:
            self.user.gamedata.当前坐标 = [recBuffer.读短整数型(True),recBuffer.读短整数型(True)]
            if self.user.gamedata.当前地图[1] == '天墉城':
                if self.user.gamedata.当前坐标[0] <= 355 and self.user.gamedata.当前坐标[0] >= 295 and \
                    self.user.gamedata.当前坐标[1] <= 255 and self.user.gamedata.当前坐标[1] >= 190 and \
                        self.假人擂台 == False:
                    坐标擂台 = threading.Thread(target=self.假人线程,args=('擂台',))
                    坐标擂台.start()
                    self.假人擂台 = True
                    self.假人商会 = False
                    self.假人拍卖行 = False
                    for 商会假人 in self.server.商会假人:
                        self.server.服务器发送(商会假人.删除假人(),self.user)
                    for 拍卖行假人 in self.server.拍卖行假人:
                        self.server.服务器发送(拍卖行假人.删除假人(),self.user)
                elif self.user.gamedata.当前坐标[0] <= 273 and self.user.gamedata.当前坐标[0] >= 177 and \
                self.user.gamedata.当前坐标[1] <= 210 and self.user.gamedata.当前坐标[1] >= 121 and \
                    self.假人商会 == False:
                    地图商会 = threading.Thread(target=self.假人线程,args=('商会',))
                    地图商会.start()
                    地图活动大使 = threading.Thread(target=self.假人线程,args=('活动大使',))
                    地图活动大使.start()
                    self.假人擂台 = False
                    self.假人商会 = True
                    self.假人拍卖行 = False
                    for 擂台假人 in self.server.擂台假人:
                        self.server.服务器发送(擂台假人.删除假人(),self.user)
                    for 拍卖行假人 in self.server.拍卖行假人:
                        self.server.服务器发送(拍卖行假人.删除假人(),self.user)
                elif self.user.gamedata.当前坐标[0] <= 227 and self.user.gamedata.当前坐标[0] >= 187 and \
                    self.user.gamedata.当前坐标[1] <= 120 and self.user.gamedata.当前坐标[1] >= 80 and \
                        self.假人拍卖行 == False:
                    坐标拍卖 = threading.Thread(target=self.假人线程,args=('拍卖',))
                    坐标拍卖.start()
                    self.假人擂台 = False
                    self.假人商会 = False
                    self.假人拍卖行 = True
                    for 商会假人 in self.server.商会假人:
                        self.server.服务器发送(商会假人.删除假人(),self.user)
                    for 擂台假人 in self.server.擂台假人:
                        self.server.服务器发送(擂台假人.删除假人(),self.user)

