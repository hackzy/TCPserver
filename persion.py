from bufferWrit import 写封包
import random
from setting import *
import threading
class 逍遥假人:
    def __init__(self,server) -> None:
        self.server = server
        self.假人id = 0
        self.x = 0
        self.y = 0
        self.称谓 = ''
        self.名称 = ''
        self.等级 = random.randint(130,139)
        self.门派 = ['終南山玉柱洞','五龍山云霄洞','鳳凰山斗闕宮','乾元山金光洞','骷髏山白骨洞']
        self.形象 = {'五龍山云霄洞':[6001,7001,1168,861301,871301],'終南山玉柱洞':[6002,7002,1166,861302,871302],'鳳凰山斗闕宮':[6003,7003,1169,861303,871303],
                   '乾元山金光洞':[6004,7004,1167,861304,871304],'骷髏山白骨洞':[6005,7005,1170,861305,871305]}
        self.新建假人()

    def 新建假人(self):
        self.假人id = len(self.server.假人) + 1000
        self.x = random.randint(345,350)
        self.y = random.randint(215,224)
        self.称谓 = ['QQ:959683906','飛升','二劫散仙','無量天尊','逍遙大飛','錢多多']
        #self.名称 = random.choice(假人名字) + random.choice(假人名字) + random.choice(假人名字) + random.choice(假人名字)#'逍遙大飛' + self.假人id.to_bytes(2).hex()
        self.名称 = ''.join(random.sample(假人名字,random.randint(3,6)))
    
    def 属性封包(self):
        writ = 写封包()
        allWrit = 写封包()
        for i in self.形象:
            if i == self.门派[random.randint(0,4)]:
                break
        性别 = random.randint(0,1)
        形象 = self.形象[i][性别]
        套装形象 = self.形象[i][性别 + 3]
        变身卡 = random.choice([6129,6164,6183,6146,6187,6283,20018])
        writ.写字节集(bytes.fromhex('fff9'))
        writ.写整数型(self.假人id,True)
        writ.写短整数型(self.x,True)
        writ.写短整数型(self.y,True)
        writ.写短整数型(random.randint(1,7),True) #面向方位
        writ.写整数型(self.形象[i][2],True) #武器
        writ.写整数型(1,True)
        for a in range(3):# 8
            writ.写整数型(0,True)
        writ.写整数型(形象,True)
        writ.写整数型(0,True)
        是否变身 = random.randint(0,2)
        
        if i == '終南山玉柱洞':
            坐骑 = random.choice([31025,31550,31015,31024,31501,31020,31046,31542,31004,31018])
            坐骑形象 = 770032
            是否坐骑 = 4
            flag = 1
            变身形象 = 套装形象
            形象类型 = 4
        else:
            if 是否变身 == 0:
                坐骑形象 = 变身卡
                变身形象 = 变身卡
                是否坐骑 = 8
                形象类型 = 8
            else:
                变身形象 = 套装形象
                坐骑形象 = 套装形象
                是否坐骑 = 1
                形象类型 = 3
            flag = 0
            坐骑 = 0
        writ.写整数型(坐骑,True)
        writ.写整数型(0,True)
        writ.写整数型(flag,True)
        writ.写文本型(self.名称,True)
        writ.写整数型(0,True)
        writ.写短整数型(self.等级,True)
        writ.写文本型(self.称谓[random.randint(0,5)],True)
        writ.写文本型('upgrade',True)
        writ.写文本型(i,True) #门派
        writ.写字节集(bytes.fromhex('0000000000'))
        writ.写短整数型(random.randint(3,4),True) #仙魔
        writ.写整数型(21,True)
        writ.写整数型(形象,True)
        writ.写整数型(套装形象,True) #套装形象
        writ.写整数型(变身形象,True) #套装形象
        writ.写整数型(坐骑形象,True) #坐骑形象
        writ.写短整数型(是否坐骑,True)    #特效 套装底盘效果
        writ.写短整数型(形象类型,True)
        writ.写字节型(int.to_bytes(2)) #飞行法宝类型
        writ.写整数型(0,True)
        writ.写字节型(int.to_bytes(random.choice([2 , 0])))#是否飞行
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
    
    
