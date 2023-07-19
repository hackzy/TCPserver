from writebuffer import WriteBuff
from readBuffer import ReadBuffer
import psutil
from setting import *
class 自动战斗:
    def __init__(self,server,user) -> None:
        self.人物使用技能 = ""
        self.宠物使用技能 = ""
        self.攻击位置id = {}
        self.人物攻击位置 = 0
        self.宠物攻击位置 = 0
        self.开关 = False
        self.server = server
        self.user = user

    def 战斗封包(self,id,技能,攻击位置):
        if 攻击位置 not in self.攻击位置id:
            for b in self.攻击位置id.keys():
                攻击位置 = b
                break
        if 技能 == '':
            return
        if len(self.攻击位置id) == 0:
            return
        if 技能 == "防御":
            攻击id = id
            技能id = 0
            攻击类型 = 1
        elif 技能 == "普通攻擊":
            攻击id = self.攻击位置id[攻击位置]['id']
            技能id = 0
            攻击类型 = 2
        else:
            try:
                攻击id = self.攻击位置id[攻击位置]['id']
                技能id = self.user.gamedata.技能[id][技能]
                攻击类型 = 3
                if 辅助技能.find(技能) != -1:
                    攻击id = id
            except:
                self.server.基础功能.中心提示('自動戰斗配置錯誤，請重新配置！')
                return b''
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex("3202"))
        write.integer(id)
        write.integer(攻击id)
        write.integer(攻击类型)
        write.integer(技能id)
        write.integer(0)
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()

    def 开始战斗(self):
        
        self.server.客户端发送(self.战斗封包(self.user.gamedata.角色id,
                                         self.人物使用技能,self.人物攻击位置),self.user)

        self.server.客户端发送(self.战斗封包(self.user.gamedata.参战宠物id,
                                         self.宠物使用技能,self.宠物攻击位置),self.user)
        
    def 置攻击位置id(self,buffer):
        read = ReadBuffer()
        self.攻击位置id = {}
        read.setBuffer(buffer)
        read.skip(12)
        数量 = int.from_bytes(read.byte(1))
        for a in range(数量):
            id = read.integer()
            read.skip(6)
            位置 = read.integer()
            self.攻击位置id.update({位置:{'id':id}})
            信息数量 = read.integer(2)
            for b in range(信息数量):
                类型 = read.integer(2)
                标识 = int.from_bytes(read.byte(1))
                if 标识 == 4:
                    文本 = read.string()
                    if 类型 == 1:
                        self.攻击位置id.update({位置:{'名称':文本}})
                if 标识 == 3:
                    read.integer()
            read.skip(65)

    def 删攻击id(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        删除id = read.integer()
        for a in list(self.攻击位置id.keys()):
            try:
                if self.攻击位置id[a]['id'] == 删除id:
                    del self.攻击位置id[a]
            except:
                continue
    def 捕捉(self,名称):
        write = WriteBuff()
        allWrite = WriteBuff()
        for 位置 in self.攻击位置id:
            if self.攻击位置id[位置]['名称'] == 名称:
                break
        write.byte(bytes.fromhex('1208'))
        write.integer(self.user.gamedata.角色id)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def 补充状态(self):
        血玲珑,法玲珑 = self.user.fuzhu.血蓝位置()
        self.user.fuzhu.人物回复(血玲珑,法玲珑)
        self.user.fuzhu.宠物回复(血玲珑,法玲珑)