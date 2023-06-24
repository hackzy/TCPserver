from bufferWrit import 写封包
from recBuffer import 读封包
import psutil
from setting import *
import time
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
            攻击id = self.攻击位置id[攻击位置]
            技能id = 0
            攻击类型 = 2
        else:
            try:
                攻击id = self.攻击位置id[攻击位置]
                技能id = self.user.gamedata.技能[id][技能]
                攻击类型 = 3
                if 辅助技能.find(技能) != -1:
                    攻击id = id
            except:
                攻击id = self.攻击位置id[攻击位置]
                key = self.user.gamedata.技能[id].keys()[0]
                技能id = self.user.gamedata.技能[id][key]
                攻击类型 = 3
                if 辅助技能.find(技能) != -1:
                    攻击id = id
        写包 = 写封包()
        完整包 = 写封包()
        写包.写字节集(bytes.fromhex("3202"))
        写包.写整数型(id,True)
        写包.写整数型(攻击id,True)
        写包.写整数型(攻击类型,True)
        写包.写整数型(技能id,True)
        写包.写整数型(0,True)
        完整包.写字节集(b'\x4d\x5a\x00\x00')
        完整包.写整数型(int(psutil.boot_time()),True)
        完整包.写字节集(写包.取数据(),True,1,True)
        return 完整包.取数据()

    def 开始战斗(self):
        
        self.server.客户端发送(self.战斗封包(self.user.gamedata.角色id,
                                         self.人物使用技能,self.人物攻击位置),self.user)

        self.server.客户端发送(self.战斗封包(self.user.gamedata.参战宠物id,
                                         self.宠物使用技能,self.宠物攻击位置),self.user)
        
    def 置攻击位置id(self,buffer):
        读 = 读封包()
        self.攻击位置id = {}
        读.置数据(buffer)
        读.跳过(12)
        数量 = 读.读字节型()
        for a in range(数量):
            id = 读.读整数型(True)
            读.跳过(6)
            位置 = 读.读短整数型(True)
            self.攻击位置id.update({位置:id})
            信息数量 = 读.读短整数型(True)
            for b in range(信息数量):
                读.读短整数型()
                标识 = 读.读字节型()
                if 标识 == 4:
                    读.读文本型(True)
                if 标识 == 3:
                    读.读整数型()
            读.跳过(65)

    def 删攻击id(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        删除id = 读.读整数型(True)
        for a in list(self.攻击位置id.keys()):
            if self.攻击位置id[a] == 删除id:
                del self.攻击位置id[a]

    def 补充状态(self):
        血玲珑,法玲珑 = self.user.fuzhu.血蓝位置()
        self.user.fuzhu.人物回复(血玲珑,法玲珑)
        self.user.fuzhu.宠物回复(血玲珑,法玲珑)