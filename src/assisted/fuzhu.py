from src.assisted.luzhi import Luzhi
from src.assisted.autoFired import 自动战斗
from src.assisted.xiaozhushou import XiaoZhuShou
from src.basebuffer.writebuffer import WriteBuff
from .autoTreasure import AutoTreasure
from setting import *
from threading import Event
import time
class fuzhu:
    def __init__(self,server,user) -> None:
        self.luzhi = Luzhi(server,user)
        self.自动战斗 = 自动战斗(server,user)
        self.小助手 = XiaoZhuShou(server,user)
        self.autoTreasure = AutoTreasure()
        self.鉴定类型 = ''
        self.user = user
        self.server = server
        self.开始改造 = False
        self.改造类型 = ''
        self.录制保存 = {}

    def 血蓝位置(self):
        法玲珑 = self.getItemPot('法玲瓏')
        血玲珑 = self.getItemPot('血玲瓏')
        驯兽诀 = self.getItemPot('馴獸訣')
        # self.server.写日志(msg = '血玲珑位置：{}，法玲珑位置：{}，驯兽诀位置：{}，所有物品：{}'.format(血玲珑,法玲珑,驯兽诀,self.user.gamedata.物品数据),console=True)
        if 法玲珑 == 0:
            if not self.server.基础功能.商城购买道具(self.user,'特級法玲瓏'):
                time.sleep(1)
                法玲珑 = self.getItemPot('法玲瓏')
        if 血玲珑 == 0:
            if not self.server.基础功能.商城购买道具(self.user,'特級血玲瓏'):
                time.sleep(1)
                血玲珑 = self.getItemPot('血玲瓏')
        if 驯兽诀 == 0:
            if not self.server.基础功能.商城购买道具(self.user, '高級馴獸訣'):
                time.sleep(1)
                驯兽诀 = self.getItemPot('馴獸訣')
        if 法玲珑 != 0 and 血玲珑 != 0 and 驯兽诀 != 0:
            return 血玲珑,法玲珑
        else:
            法玲珑 = self.getItemPot('法玲瓏')
            血玲珑 = self.getItemPot('血玲瓏')
            驯兽诀 = self.getItemPot('馴獸訣')
            return 血玲珑,法玲珑
    def 使用物品(self,pot):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('202c'))
        write.byte(pot.to_bytes(1))
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def 使用技能(self,id):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('2032'))
        write.integer(self.user.gamedata.角色id)
        write.integer(id,3)
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def 人物回复(self,血玲珑,法玲珑):
        buffer = self.使用物品(血玲珑) + self.使用物品(法玲珑)
        for a in range(3):
            self.server.客户端发送(buffer,self.user)

    def 宠物回复(self,血玲珑,法玲珑):
        try:
            write = WriteBuff()
            allWrite = WriteBuff()
            write.byte(bytes.fromhex('204e'))
            write.byte(self.user.gamedata.pet[self.user.gamedata.参战宠物id].位置.to_bytes(1))
            write.byte(血玲珑.to_bytes(1))
            allWrite.byte(组包包头)
            allWrite.byte(write.getBuffer(),True,1)
            write = WriteBuff()
            write.byte(bytes.fromhex('204e'))
            write.byte(self.user.gamedata.pet[self.user.gamedata.参战宠物id].位置.to_bytes(1))
            write.byte(法玲珑.to_bytes(1))
            allWrite.byte(组包包头)
            allWrite.byte(write.getBuffer(),True,1)
            if self.user.gamedata.pet[self.user.gamedata.参战宠物id].忠诚 < 80:
                    write = WriteBuff()
                    write.byte(bytes.fromhex('109a'))
                    write.integer(self.user.gamedata.参战宠物id)
                    allWrite.byte(组包包头)
                    allWrite.byte(write.getBuffer(),True,1)
            for a in range(3):
                self.server.客户端发送(allWrite.getBuffer(),self.user)
        except:
            return
        
    def 一键鉴定(self):
        if len(self.user.gamedata.物品数据) == 0:
            return
        try:
            for back in self.user.gamedata.物品数据:
                if back > 100:
                    write = WriteBuff()
                    write.byte(组包包头)
                    write.byte(bytes.fromhex('0006301c'))
                    write.integer(back)
                    self.user.服务器句柄.send(write.getBuffer())
                    Event().wait(timeout=0.2)
        except:
            pass
        self.鉴定类型 = ''

    def 鉴定二级对话(self,NPCID,对话内容):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('3038'))
        write.integer(NPCID)
        if 对话内容.find('花費') != -1:
            write.string('確定',True)
        else:
            write.string(self.鉴定类型,True)
        write.byte(b'\x00')
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        self.user.服务器句柄.send(allWrite.getBuffer())
        
    def 装备改造(self):
        item = []
        write = WriteBuff()
        allWrite = WriteBuff()
        if self.改造类型 == '改造武器':
            改造道具 = '超級靈石'
        else:
            改造道具 = '超級晶石'

        for a in self.user.gamedata.物品数据:
            if self.user.gamedata.物品数据[a].名称 == 改造道具:
                item.append(a)
        if len(item) < 6:
            数量 = 6 - len(item)
            self.server.基础功能.商城购买道具(self.user,改造道具,数量=数量)
            Event().wait(0.3)
            for a in self.user.gamedata.物品数据:
                if self.user.gamedata.物品数据[a].名称 == 改造道具:
                    item.append(a)
        if len(item) < 6:
            return
        write.byte(bytes.fromhex('508A'))
        write.integer(self.user.gamedata.角色id)
        write.integer(1,2)
        write.integer(7,2)
        write.integer(101)
        for b in range(6):
            write.integer(item[b])
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()

    def 改造线程(self):
        while self.开始改造:
            self.server.客户端发送(self.装备改造(),self.user)
            Event().wait(0.3)

    def 维修装备(self):
        #4D 5A 00 00 24 BC 8E 68 00 08 20 A4 00 00 00 00 00 00 
        write = WriteBuff()
        write.byte(bytes.fromhex('4D5A000024BC8E68000820A40000000000'))
        buffer = write.getBuffer()
        self.server.客户端发送(buffer,self.user)
        time.sleep(0.3)
        write = WriteBuff()
        write.byte(bytes.fromhex('4D 5A 00 00 24 BC 9A 8D 00 0B 20 EE 06 E4 BF AE E7 90 86 01 30 '))
        buffer = write.getBuffer()
        self.server.客户端发送(buffer,self.user)
        
    def getItemPot(self,item:str,vague = True):
        for key in self.user.gamedata.物品数据:
            if vague:
                if self.user.gamedata.物品数据[key].名称.find(item) != -1:
                    return key
            else:
                if self.user.gamedata.物品数据[key].名称 == item:
                    return key
        return 0