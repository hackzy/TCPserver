from src.basebuffer.readBuffer import ReadBuffer
from src.basebuffer.writebuffer import WriteBuff
from src.game.itemData import itemAttrib
from setting import *
import threading
from src.game.petData import petdata
class SendToClient:
    def __init__(self,user,server) -> None:
        self.user = user
        self.server = server

    def 登录线路(self,buffer):
        #4d5a000000000000003433570000000103e80f3131312e3137332e3131362e313333177bebf42c6315e58581e8a8b1e8a9b2e5b8b3e8999fe799bbe585a5
        write = WriteBuff()
        read = ReadBuffer()
        allWrite = WriteBuff()
        read.setBuffer(buffer)
        read.skip(10)
        write.byte(read.byte(8))
        read.string()
        port = read.integer(2)
        for p in range(len(游戏端口)):
            if 游戏端口[p] == port:
                监听端口 = 服务器监听端口[p]
        write.string(服务器外网地址,True)
        write.integer(监听端口,2)
        write.byte(read.residBuffer())
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def 显示线路(self,buffer):
        #4D 5A 00 00 00 00 00 00 00 23 43 55 00 01 06 E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C E4 B8 80 E7 B7 9A 09 31 32 37 2E 30 2E 30 2E 31 00 02 
        write = WriteBuff()
        read = ReadBuffer()
        allWrite = WriteBuff()
        read.setBuffer(buffer)
        read.skip(10)
        write.byte(read.byte(2))
        number = read.integer(2)
        write.integer(number,2)
        for n in range(number):
            write.string(read.string(),True)
            read.string()
            write.string(服务器外网地址,True)
        write.byte(read.residBuffer())
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def 切换角色(self,buffer):
        read = ReadBuffer()
        write = WriteBuff()
        allWrite = WriteBuff()
        read.setBuffer(buffer)
        read.skip(10)
        write.byte(read.byte(4))
        data = read.string()
        stri = data.split(" ")
        data = 服务器外网地址 + ' ' + str(服务器监听端口[1]) + ' '
        for i in range(len(stri) - 2):
            data = data + stri[i + 2] + ' '
        data = data[:len(data) - 1]
        write.string(data,True)
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()

    def 背包读取(self,buffer):
        write = WriteBuff()
        read = ReadBuffer()
        saveBuff = WriteBuff()
        read.setBuffer(buffer)
        read.skip(10)
        write.byte(read.byte(2))
        物品总数 = read.integer(2)
        write.integer(物品总数,2)
        for i in range(物品总数):
            物品位置id = int.from_bytes(read.byte(1))
            if 物品位置id == 32:
                物品位置id = 55
            temp = {物品位置id:itemAttrib()}
            write.byte(物品位置id.to_bytes(1))
            物品数据总数 = read.integer(2)
            if 物品数据总数 == 0:
                write.integer(物品数据总数,2)
            saveBuff.clearBuffer()
            saveBuff.integer(物品数据总数,2)
            for a in range(物品数据总数):
                物品属性类别 = read.integer(2)
                saveBuff.integer(物品属性类别,2)
                物品属性数量 = read.integer(2)
                if 物品位置id == 33 or 物品位置id == 31:
                    saveBuff.integer(物品属性数量 + 1,2)
                    saveBuff.byte(bytes.fromhex('038e0101'))
                    saveBuff.integer(物品属性数量,2)
                else:
                    for b in range(物品属性数量):
                        属性标识 = read.byte(2)
                        数据类型 = int.from_bytes(read.byte(1))
                        saveBuff.byte(属性标识)
                        saveBuff.byte(数据类型.to_bytes())
                        if 数据类型 == 1:
                            T_字节型 = int.from_bytes(read.byte(1))
                            if 属性标识 == b'\x01\x4f'  \
                            and T_字节型 == 1:
                                是否封印 = True
                            saveBuff.byte(T_字节型.to_bytes())
                        elif 数据类型 == 2:
                            T_短整数型 = read.integer(2)
                            write.integer(T_短整数型,2)
                        elif 数据类型 == 3:
                            T_整数型 = read.integer()
                            saveBuff.integer(T_整数型)
                            if 属性标识 == b'\x02\x47':
                                pass
                            if 属性标识 == b'\x00\x54':
                                temp[物品位置id].id = T_整数型
                        elif 数据类型 == 4:
                            T_文本型 = read.string()
                            saveBuff.string(T_文本型,True)
                            if 属性标识 == b'\x00\x01':
                                temp[物品位置id].名称 = T_文本型
                        elif 数据类型 == 6:
                            T_字节型 = int.from_bytes(read.byte(1))
                            if 属性标识 == b'\x00\xca':
                                temp[物品位置id].类型 = T_字节型
                        elif 数据类型 == 7:
                            T_短整数型 = read.integer(2)
                            saveBuff.integer(T_短整数型,2)
                    temp[物品位置id].封包缓存 = saveBuff.getBuffer()
            self.user.gamedata.物品数据.update(temp)

    def 人物属性读取(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(10)
        read.byte(2)
        self.user.gamedata.角色id = read.integer()
        数量 = read.integer(2)
        for a in range(数量):
            数据头 = read.byte(2).hex()
            标识 = int.from_bytes(read.byte(1))
            if 标识 == 1:
                read.byte(1)
            elif 标识 == 2:
                T_短整数型 = read.integer(2)
                if 数据头 == '002c':
                    self.user.gamedata.五行 = T_短整数型
                elif 数据头 == '001f':
                    self.user.gamedata.等级 = T_短整数型
            elif 标识 == 3:
                T_整数型 = read.integer()
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
                T_文本型 = read.string()
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
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        对象id = read.integer()
        数量 = read.integer(2)
        try:
            for a in range(数量):
                技能id = read.integer(2)
                read.skip(2)
                标识 = read.byte(2).hex()
                技能名称 = read.string()
                read.skip(2)
                技能等级 = read.integer(2)
                read.skip(39)
                read.string()
                read.byte(1)
                t数量 = read.integer(2)
                for b in range(t数量):
                    read.string()
                    read.integer()
                read.byte(5)
                if 标识 == '0092' or 标识 == '008a':
                    if 对象id not in self.user.gamedata.技能:
                        self.user.gamedata.技能.update({对象id:{技能名称:技能id}})
                    else:
                        self.user.gamedata.技能[对象id].update({技能名称:技能id})
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
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        对象id = read.integer()
        x = read.integer(2)
        y = read.integer(2)
        朝向 = read.integer(2)
        武器 = read.integer()
        NPC类型 = read.integer()
        read.skip(20)
        坐骑 = read.integer()
        read.skip(8)
        对象昵称 = read.string()
        read.skip(6)
        read.string()
        read.string()
        read.string()
        read.string()
        read.skip(10)
        对象职业 = read.integer()
        read.skip(12)
        飞行法宝ID = int.from_bytes(read.byte(1))
        read.skip(19)
        名牌 = read.string()
        #print(buffer.hex())
        #self.server.写日志('对象id:'+str(对象id)+'|'+'对象昵称:'+对象昵称+'|'+'武器:'+str(武器)+'|'\
        #                +'NPC类型:'+str(NPC类型)+'|'+'坐骑:'+str(坐骑)+'|'+'对象职业:'+str(对象职业)+'|'+\
        #                    '飞行法宝:'+str(飞行法宝ID)+'|'+'铭牌:'+名牌+'|'+'X:'+str(x)+'|'+'Y:'+str(y)+'|')
        '''[13:21:58.965960]对象id:379088|对象昵称:窦小鑫|对象类型:11962|NPC类型:1|坐骑:31501|对象职业:4001|飞
行法宝:0|铭牌:|X:61|Y:29|'''

    def 取角色gid(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        角色数量 = read.integer(2)
        for i in range(角色数量):
            数据数量 = read.integer(2)
            for b in range(数据数量):
                数据头 = read.byte(2)
                标识 = int.from_bytes(read.byte(1))
                if 标识 == 1:
                    read.byte(1)
                elif 标识 == 2:
                    read.integer(2)
                elif 标识 == 3:
                    read.integer()
                elif 标识 == 4:
                    文本 = read.string()
                    if 数据头 == b'\x00\x01':
                        self.user.gamedata.所有角色[str(i)].update({'名称':文本})
                    elif 数据头 == b'\x01\x31':
                        self.user.gamedata.所有角色[str(i)].update({'GID':int.from_bytes(bytes.fromhex(文本))})


    def 地图事件(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        地图id = read.integer()
        read.integer()
        地图名 = read.string()
        self.user.gamedata.上一地图 = self.user.gamedata.当前地图[1]
        self.user.gamedata.当前地图 = [地图id,地图名]
        self.user.gamedata.当前坐标[0] = read.integer(2)
        self.user.gamedata.当前坐标[1] = read.integer(2)
        self.user.gamedata.屏蔽垃圾 = True
        if 地图名 == '天墉城':
            刷新假人 = threading.Thread(target=self.server.假人.地图假人刷新,args=(self.server,self.user,'坐标'))
            刷新假人.daemon = True
            刷新假人.start()
        elif 地图名 == '幽雅小居' or 地图名 == '豪华居所' \
            or 地图名 == '花园别墅' or 地图名 == '翡翠庄园':
            self.user.gamedata.屏蔽垃圾 = False
        else:
            if self.user.gamedata.上一地图 == '天墉城' and \
                self.user.gamedata.上一地图 != self.user.gamedata.当前地图[1]:
                删除假人 = threading.Thread(target=self.server.假人.假人删除线程,args=(self.server,self.user,'地图'))
                删除假人.daemon = True
                删除假人.start()

    def 战斗对话(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        read.integer()
        read.integer()
        NPC = read.string()
        read.skip(7)
        内容 = read.string()
        if NPC == '财神' and 内容 == '感谢你们帮我的忙，这些是给你们的奖励！':
            evn = threading.Event()
            evn.wait(2)
            self.财神奖励(self.user)



    def 财神奖励(self,user):
        #GM_SEND(self,玩家昵称,角色id,命令,值):
        现金 = user.gamedata.金币 + 20000000
        if 现金 > 2000000000:
            self.server.基础功能.中心提示('你的金钱已满，无法继续获得金钱。')
            self.server.GM.GM_SEND(user.gamedata.角色名,user.gamedata.角色id,'cash',2000000000)
        else:
            self.server.GM.GM_SEND(user.gamedata.角色名,user.gamedata.角色id,'cash',现金)
            bf = self.server.基础功能.奖励_上升提示(20000000,'cash') + \
            self.server.基础功能.中心提示('你得到了#Y20,000,000#n文钱。') + \
            self.server.基础功能.左下角提示('你得到了#Y20,000,000#n文钱。')
            self.server.服务器发送(bf,user)

    def 商城读取(self,buffer):
        '''00 01 00 01 00 05 00 01 04 0C E5 BE A1 E9 9D 88 E7 B3 A7 E8 A2 8B 00 28 03 00 00 23 83 01 37 04 03 E5 80 8B 00 CB 02 00 01 00 C9 04 00 09 43 30 30 30 30 30 30 30 39 00 01 00 06 00 09 02 00 00 00 64 00 00 00 00 00 00 00 00 00 00 '''
        '''00 01 00 01 00 05 00 01 04 0F E4 B8 80 E7 99 BE E4 B8 80 E8 A1 A3 00 28 03 00 00 06 13 01 37 04 03 E5 80 8B 00 CB 02 00 01 00 C9 04 33 E6 89 93 E9 96 8B E5 BE 8C E5 8F AF E4 BB A5 E7 8D B2 E5 BE 97 E8 A1 A3 E6 9C 8D E6 BB BF E5 B1 AC E6 80 A7 E8 B6 85 E7 B4 9A E9 BB 91 E6 B0 B4 E6 99 B6 09 54 30 30 30 30 30 30 31 38 00 01 00 01 00 12 01 00 00 00 01 00 00 00 00 00 00 00 00 00 00'''
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        数量 = read.integer(2)
        for a in range(数量):
            read.integer(2)
            read.integer(2)
            数据数量 = read.integer(2)
            for b in range(数据数量):
                数据头 = read.integer(2)
                标识 = int.from_bytes(read.byte(1))
                if 标识 == 4:
                    文本 = read.string()
                    if 数据头 == 1:
                        道具名称 = 文本
                elif 标识 == 3:
                    read.integer()
                elif 标识 == 2 or 标识 == 7:
                    read.integer(2)
                elif 标识 == 1 or 标识 == 6:
                    read.byte(1)
            道具id = read.string()
            read.skip(6)
            元宝类型 = int.from_bytes(read.byte(1))
            if 元宝类型 == 1 or 元宝类型 == 3:
                self.user.gamedata.商城数据.update({道具名称:[道具id,'gold_coin']})
            else:
                self.user.gamedata.商城数据.update({道具名称:[道具id,'silver_coin']})
            read.skip(6)
    def NPC对话(self,buffer):
        read = ReadBuffer()
        write = WriteBuff()
        allWrite = WriteBuff()
        read.setBuffer(buffer)
        read.skip(10)
        write.byte(read.byte(2))
        NPCid = read.integer()
        write.integer(NPCid)
        write.integer(read.integer())
        write.byte(read.byte(2))
        对话内容 = read.string(lenType=1)
        if self.user.fuzhu.鉴定类型 != '':
            if 对话内容.find('鉴定符') != -1:
                self.user.fuzhu.鉴定二级对话(NPCid,对话内容)
                return b''
        write.string(对话内容,True,1)
        write.byte(read.byte(4))
        write.string(read.string(),True)
        write.byte(read.residBuffer())
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()

    def 宠物读取(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(14)
        位置id = int.from_bytes(read.byte(1))
        id = read.integer()
        self.user.gamedata.pet.update({id:petdata()})
        self.user.gamedata.pet[id].位置 = 位置id
        数量 = read.integer(2)
        for a in range(数量):
            read.byte(2)
            属性数量 = read.integer(2)
            for b in range(属性数量):
                数据头 = read.byte(2)
                标识 = int.from_bytes(read.byte(1))
                if 标识 == 1:
                    T_字节型 = int.from_bytes(read.byte(1))
                elif 标识 == 2:
                    T_短整数型 = read.integer(2)
                elif 标识 == 3:
                    T_整数型 = read.integer()
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
                    T_文本型 = read.string()
                    if 数据头.hex() == '0001':
                        self.user.gamedata.pet[id].昵称 = T_文本型
                elif 标识 == 6:
                    read.byte(1)
                elif 标识 == 7:
                    read.integer(2)
            
    def 宠物数据更新(self,buffer):
        '''4d5a000000000000001610ec00010400052f710001000100010042030000005b'''
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(14)
        位置 = int.from_bytes(read.byte(1))
        id = read.integer()
        read.integer(2)
        read.integer(2)
        read.integer(2)
        数据头 = read.byte(2)
        标识 = int.from_bytes(read.byte(1))
        if id not in self.user.gamedata.pet:
            return
        if 标识 == 1:
            read.byte(1)
        elif 标识 == 2:
            read.integer(2)
        elif 标识 == 3:
            整数 = read.integer()
            if 数据头.hex() == '0006':
                self.user.gamedata.pet[id].气血 = 整数
            elif 数据头.hex() == '000b':
                self.user.gamedata.pet[id].法力 = 整数
            elif 数据头.hex() == '0042':
                self.user.gamedata.pet[id].忠诚 = 整数
            elif 标识 == 4:
                文本 = read.string()
                if 数据头.hex() == '0001':
                    self.user.gamedata.pet[id].昵称 = 文本

    def 读当前坐标(self,buffer:bytes):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        id = read.integer()
        if id == self.user.gamedata.角色id:
            self.user.gamedata.当前坐标 = [read.integer(2),read.integer(2)]
            if self.user.gamedata.当前地图[1] == '天墉城':
                假人刷新 = threading.Thread(target=self.server.假人.地图假人刷新,args=(self.server,self.user,'坐标'))
                假人刷新.daemon = True
                假人刷新.start()

    def 读自身显示属性(self,buffer:bytes):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        read.integer()#人物id
        read.integer(2)#人物x坐标
        read.integer(2)#人物y坐标
        read.integer(2)#人物朝向
        read.integer()#人物武器
        read.integer()
        for a in range(3):# 8
            read.integer()
        read.integer()#基础形象
        read.integer()
        read.integer()#坐骑
        read.integer()
        read.integer()
        read.string()#名字
        read.integer()
        read.integer(2)#等级
        read.string()#称谓
        read.string()#称谓类型
        read.string() #门派
        read.string()#帮派
        read.integer()
        read.integer(2) #仙魔
        read.integer()
        read.integer()#基础形象
        read.integer() #套装形象
        read.integer() #显示形象
        read.integer() #坐骑形象
        read.integer(2)    #特效 套装底盘效果
        read.integer(2) #形象类型
        read.integer(2) #飞行法宝类型
        read.integer()
        self.user.gamedata.是否飞行 = read.integer(2)#是否飞行

    def 任务读取(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(14)
        任务名称 = read.string()
        read.string(lenType=1) #任务介绍
        任务内容 = read.string(lenType=1)
        read.skip(8)
        read.string()#建议人数
        read.string()#建议等级r
        read.string(lenType=1)#任务奖励
        self.user.gamedata.任务.update({任务名称:任务内容})