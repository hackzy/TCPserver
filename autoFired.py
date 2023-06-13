from bufferWrit import 写封包
import psutil
class 自动战斗:
    def __init__(self) -> None:
        self.技能名称 = []
        self.技能id = []
        self.人物使用技能 = ""
        self.宠物使用技能 = ""
        self.攻击id = []
        self.攻击位置 = []
        self.人物攻击位置 = 0
        self.宠物攻击位置 = 0

    def 置技能(self,技能名称,技能id):
        self.技能名称.append(技能名称)
        self.技能id.append(技能id)
    
    def 取技能id(self,技能名称):
        i = 0
        for 名称 in self.技能名称:
            if 名称 == 技能名称:
                return self.技能id[i]
            i += 1
        return 0
    def 战斗封包(self,id,技能,攻击位置):
        if 技能 == "防御":
            攻击id = id
            技能id = 0
            攻击类型 = 1
        elif 技能 == "普通攻擊":
            攻击id = self.取攻击位置id(攻击位置)
            技能id = 0
            攻击类型 = 2
        else:
            攻击id = self.取攻击位置id(攻击位置)
            技能id = self.取技能id(技能)
            攻击类型 = 3
            if 辅助技能.find(技能) != -1:
                攻击id = id
        写包 = 写封包()
        完整包 = 写封包()
        写包.写字节集(bytes.fromhex("3202"))
        写包.写整数型(id,True)
        写包.写整数型(攻击id,True)
        写包.写整数型(攻击类型,True)
        写包.写整数型(0,True)
        完整包.写字节集(b'\x79\x90\x00\x00')
        完整包.写整数型(psutil.boot_time(),True)
        完整包.写字节集(写包.取数据(),True,1,True)
        return 完整包.取数据()
