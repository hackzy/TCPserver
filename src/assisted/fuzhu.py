from src.assisted.luzhi import Luzhi
from src.assisted.autoFired import 自动战斗
from src.assisted.xiaozhushou import XiaoZhuShou
from src.basebuffer.writebuffer import WriteBuff
from .autoTreasure import AutoTreasure
from setting import *
from threading import Event
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
        法玲珑 = self.server.基础功能.getItemPot('法玲珑')
        血玲珑 = self.server.基础功能.getItemPot('血玲珑')
        驯兽诀 = self.server.基础功能.getItemPot('驯兽诀')
        if 法玲珑 == 0:
            self.server.基础功能.商城购买道具(self.user,'特级法玲珑')
        if 血玲珑 == 0:
            self.server.基础功能.商城购买道具(self.user,'特级血玲珑')
        if 驯兽诀 == 0:
            self.server.基础功能.商城购买道具(user = self.user,道具 = '高级驯兽诀')
        if 法玲珑 != 0 and 血玲珑 != 0 and 驯兽诀 != 0:
            return 血玲珑,法玲珑
        else:
            return self.血蓝位置()
        
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
        if 对话内容.find('花费') != -1:
            write.string('确定',True)
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
            改造道具 = '超级灵石'
        else:
            改造道具 = '超级晶石'

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

