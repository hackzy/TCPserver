from bufferWrit import 写封包
import random
from setting import *
import threading
class 逍遥假人:
    def __init__(self,server,假人类型) -> None:
        self.server = server
        #套装形象公式 = 假人是否坐骑+假人性别+假人套装等级+假人相性
        #坐骑形象公式 = 假人是否坐骑+假人性别+假人坐姿+假人相性
        if 假人类型 == '所有':
            self.假人id = len(self.server.假人) + 1000
            self.x = random.randint(50,390)
            self.y = random.randint(10,300)
        elif 假人类型 == '擂台':
            self.假人id = len(self.server.擂台假人) + 2000
            self.x = random.randint(326,356)
            self.y = random.randint(192,222)
        elif 假人类型 == '商会':
            self.假人id = len(self.server.商会假人) + 3000
            self.x = random.randint(260,280)
            self.y = random.randint(136,156)
        elif 假人类型 == '拍卖':
            self.假人id = len(self.server.拍卖行假人) + 4000
            self.x = random.randint(196,216)
            self.y = random.randint(91,111)
        elif 假人类型 == '活动大使':
            self.假人id = len(self.server.活动大使假人) + 5000
            self.x = random.randint(217,277)
            self.y = random.randint(163,213)
        self.称谓 = random.choice(假人称谓)
        self.名称 = ''.join(random.sample(假人名字,random.randint(3,6)))
        self.等级 = random.randint(70,159)
        self.相性 = random.choice(假人相性)
        self.门派 = 假人门派[int(self.相性)-1]
        self.性别 = random.choice(假人性别)
        self.基础形象 = self.性别 + '00' +self.相性
        self.是否坐骑 = random.choice(假人是否坐骑) # 7是坐骑 8是无
        self.形象类型1 = 3
        self.形象类型2 = 3
        self.是否飞行 = random.choice([2,0])
        self.仙魔 = random.randint(3,4)
        是否变身 = random.choice([True,False])
        变身卡 = random.choice(假人变身)
        
        if self.等级 < 131 :
            self.仙魔 = 0
        if self.等级 < 80:
            装备等级 = 假人装备等级[7]
        elif self.等级 > 79 and self.等级 < 90:
            装备等级 = 假人装备等级[8]
        elif self.等级 > 89 and self.等级 < 100:
            装备等级 = 假人装备等级[9]
        elif self.等级 > 99 and self.等级 < 110:
            装备等级 = 假人装备等级[10]
        elif self.等级 > 109 and self.等级 < 120:
            装备等级 = 假人装备等级[11]
        elif self.等级 > 119 and self.等级 < 130:
            装备等级 = 假人装备等级[12]
        elif self.等级 > 129 and self.等级 < 140:
            装备等级 = 假人装备等级[13]
        elif self.等级 > 139 and self.等级 < 150:
            装备等级 = 假人装备等级[14]
        elif self.等级 > 149 and self.等级 < 160:
            装备等级 = 假人装备等级[15]
        self.武器 = 假人武器[self.相性][int(int(装备等级)/10)]
        self.装备形象 = '8' + self.性别 + 装备等级 + self.相性
        if self.是否坐骑 == '7':
            self.坐姿 = random.choice(假人坐姿)
            self.坐骑 = random.choice(假人坐骑[list(self.坐姿.keys())[0]])
            self.变身形象 = self.装备形象
            self.显示形象 = self.是否坐骑 + self.性别 + list(self.坐姿.values())[0] + self.相性
            self.形象类型1 = 4
        else:
            self.坐骑 = 0
            if 是否变身:
                self.变身形象 = 变身卡
                self.显示形象 = 变身卡
                self.形象类型1 = 8
                self.形象类型2 = 8
            else:
                self.显示形象 = self.装备形象
                self.变身形象 = self.装备形象
                if self.相性 == '2' and self.性别 == '6' or self.相性 == '3' and self.性别 == '6' or self.相性 == '5' and self.性别 == '6' :
                    self.形象类型1 = 5
        if self.是否飞行 == 2:
            self.飞行法宝 = random.choice(假人飞行法宝)
        else:
            self.飞行法宝 = 0
    
    def 属性封包(self):
        writ = 写封包()
        allWrit = 写封包()
        writ.写字节集(bytes.fromhex('fff9'))
        writ.写整数型(self.假人id,True)
        writ.写短整数型(self.x,True)
        writ.写短整数型(self.y,True)
        writ.写短整数型(random.randint(1,7),True) #面向方位
        writ.写整数型(self.武器,True) #武器
        writ.写整数型(1,True)
        for a in range(3):# 8
            writ.写整数型(0,True)
        writ.写整数型(int(self.基础形象),True)
        writ.写整数型(0,True)
        writ.写整数型(self.坐骑,True)
        writ.写整数型(0,True)
        writ.写整数型(0,True)
        writ.写文本型(self.名称,True)
        writ.写整数型(0,True)
        writ.写短整数型(self.等级,True)
        writ.写文本型(self.称谓,True)
        writ.写文本型('upgrade',True)
        writ.写文本型(self.门派,True) #门派
        writ.写字节集(bytes.fromhex('0000000000'))
        writ.写短整数型(self.仙魔,True) #仙魔
        writ.写整数型(0,True)
        writ.写整数型(int(self.基础形象),True)
        writ.写整数型(int(self.装备形象),True) #套装形象
        writ.写整数型(int(self.变身形象),True) #显示形象
        writ.写整数型(int(self.显示形象),True) #坐骑形象
        writ.写短整数型(self.形象类型1,True)    #特效 套装底盘效果
        writ.写短整数型(self.形象类型2,True)
        writ.写字节型(self.飞行法宝.to_bytes()) #飞行法宝类型
        writ.写整数型(0,True)
        writ.写字节型(self.是否飞行.to_bytes())#是否飞行
        writ.写字节集(bytes.fromhex('00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '.replace(' ','')))
        allWrit.写字节集(组包包头)
        allWrit.写字节集(writ.取数据(),True,1)
        return allWrit.取数据()
    
    def 显示(self):
        writ = 写封包()
        allWrit = 写封包()
        writ.写字节集(bytes.fromhex('f0e7'))
        writ.写整数型(self.假人id,True)
        writ.写短整数型(1,True)
        writ.写文本型('位列仙班',True)
        allWrit.写字节集(组包包头)
        allWrit.写字节集(writ.取数据(),True,1)
        return allWrit.取数据() + self.帮派图标()
    
    def 帮派图标(self):
        writ = 写封包()
        allWrit = 写封包()
        writ.写字节集(bytes.fromhex('f0d4'))
        writ.写整数型(self.假人id,True)
        writ.写文本型(random.choice(假人帮派图标),True)
        allWrit.写字节集(组包包头)
        allWrit.写字节集(writ.取数据(),True,1)
        return allWrit.取数据()
    
    def 移动(self):
        writ = 写封包()
        allWrit = 写封包()
        writ.写字节集(bytes.fromhex('402f'))
        writ.写整数型(self.假人id,True)
        self.x += random.randint(-30,30)
        self.y += random.randint(-30,30)
        if self.x >= 410:
            self.x -= 40
        elif self.x < 6:
            self.x += 40
        if self.y >= 410:
            self.y -= 40
        elif self.y < 6:
            self.y += 40
        writ.写短整数型(self.x,True)
        writ.写短整数型(self.y,True)
        writ.写短整数型(1,True)
        allWrit.写字节集(组包包头)
        allWrit.写字节集(writ.取数据(),True,1)
        return allWrit.取数据()
    
    
    def 删除假人(self):
        writ = 写封包()
        allWrit = 写封包()
        writ.写字节集(bytes.fromhex('2ffd'))
        writ.写整数型(self.假人id,True)
        writ.写短整数型(1,True)
        allWrit.写字节集(组包包头)
        allWrit.写字节集(writ.取数据(),True,1)
        return allWrit.取数据()
    
    def 重置假人(self,user):
        self.__init__(self.server)
        self.server.服务器发送(self.属性封包(),user)
        self.server.服务器发送(self.显示(),user)
