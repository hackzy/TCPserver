from writebuffer import WriteBuff
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
            self.y = random.randint(28,254)
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
        self.图标 = random.choice(假人帮派图标)
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
        if self.等级 > 139:
            self.武器 = 0
        self.装备形象 = '8' + self.性别 + 装备等级 + self.相性
        if self.是否坐骑 == '7':
            self.坐姿 = random.choice(假人坐姿)
            self.坐骑 = random.choice(假人坐骑[list(self.坐姿.keys())[0]])
            self.变身形象 = self.装备形象
            r = str(random.randint(1,5))
            g = str(random.randint(1,5))
            b = str(0)
            self.显示形象 = r+g+b+self.是否坐骑 + self.性别 + list(self.坐姿.values())[0] + self.相性
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
                if self.相性 == '2' and self.性别 == '6' or self.相性 == '1' and self.性别 == '6':
                    self.形象类型1 = 1
                elif self.相性 == '3' and self.性别 == '6' :
                    self.形象类型1 = 1
                elif self.相性 == '5' and self.性别 == '6' :
                    self.形象类型1 = 1
                    
        if self.是否飞行 == 2:
            self.飞行法宝 = random.choice(假人飞行法宝)
        else:
            self.飞行法宝 = 0
    
    def 属性封包(self):
        writ = WriteBuff()
        allWrit = WriteBuff()
        writ.byte(bytes.fromhex('fff9'))
        writ.integer(self.假人id)
        writ.integer(self.x,2)
        writ.integer(self.y,2)
        writ.integer(random.randint(1,7),2) #面向方位
        writ.integer(self.武器) #武器
        writ.integer(1)
        for a in range(3):# 8
            writ.integer(0)
        writ.integer(int(self.基础形象))
        writ.integer(0)
        writ.integer(self.坐骑)
        writ.integer(0)
        writ.integer(0)
        writ.string(self.名称,True)
        writ.integer(0)
        writ.integer(self.等级,2)
        writ.string(self.称谓,True)
        writ.string('upgrade',True)
        writ.string(self.门派,True) #门派
        writ.byte(bytes.fromhex('0000000000'))
        writ.integer(self.仙魔,2) #仙魔
        writ.integer(0)
        writ.integer(int(self.基础形象))
        writ.integer(int(self.装备形象)) #套装形象
        writ.integer(int(self.变身形象)) #显示形象
        writ.integer(int(self.显示形象)) #坐骑形象
        writ.integer(self.形象类型1,2)    #特效 套装底盘效果
        writ.integer(self.形象类型2,2)
        writ.byte(self.飞行法宝.to_bytes()) #飞行法宝类型
        writ.integer(0)
        writ.byte(self.是否飞行.to_bytes())#是否飞行
        writ.byte(bytes.fromhex('00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '.replace(' ','')))
        allWrit.byte(组包包头)
        allWrit.byte(writ.getBuffer(),True,1)
        return allWrit.getBuffer()
    
    def 显示(self):
        writ = WriteBuff()
        allWrit = WriteBuff()
        writ.byte(bytes.fromhex('f0e7'))
        writ.integer(self.假人id)
        writ.integer(1,2)
        writ.string('位列仙班',True)
        allWrit.byte(组包包头)
        allWrit.byte(writ.getBuffer(),True,1)
        return allWrit.getBuffer() + self.帮派图标()
    
    def 帮派图标(self):
        writ = WriteBuff()
        allWrit = WriteBuff()
        writ.byte(bytes.fromhex('f0d4'))
        writ.integer(self.假人id)
        writ.string(self.图标,True)
        allWrit.byte(组包包头)
        allWrit.byte(writ.getBuffer(),True,1)
        return allWrit.getBuffer()
    
    def 移动(self):
        writ = WriteBuff()
        allWrit = WriteBuff()
        writ.byte(bytes.fromhex('402f'))
        writ.integer(self.假人id)
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
        writ.integer(self.x,2)
        writ.integer(self.y,2)
        writ.integer(1,2)
        allWrit.byte(组包包头)
        allWrit.byte(writ.getBuffer(),True,1)
        return allWrit.getBuffer()
    
    
    def 删除假人(self):
        writ = WriteBuff()
        allWrit = WriteBuff()
        writ.byte(bytes.fromhex('2ffd'))
        writ.integer(self.假人id)
        writ.integer(1,2)
        allWrit.byte(组包包头)
        allWrit.byte(writ.getBuffer(),True,1)
        return allWrit.getBuffer()

    def 重置假人(self,user):
        self.__init__(self.server)
        self.server.服务器发送(self.属性封包(),user)
        self.server.服务器发送(self.显示(),user)
        self.server.服务器发送(self.移动(),user)

    



    
class 假人管理:
    def __init__(self) -> None:
        self.假人 = []
        self.擂台假人 = []
        self.商会假人 = []
        self.拍卖行假人 = []
        self.活动大使假人 = []

    def 启动假人(self,server,alluser):
        for i in range(400):
            self.假人.append(逍遥假人(self,'所有'))
        for i in range(50):
            self.擂台假人.append(逍遥假人(self,'擂台'))
        for i in range(50):
            self.商会假人.append(逍遥假人(self,'商会'))
        for i in range(50):
            self.拍卖行假人.append(逍遥假人(self,'拍卖'))
        for i in range(50):
            self.活动大使假人.append(逍遥假人(self,'活动大使'))
        移动线程 = threading.Thread(target=self.假人事件线程,args=(alluser,server))
        移动线程.daemon = True
        移动线程.start()

    def 假人事件线程(self,alluser,server):
        while True:
            for 假人 in range(random.randint(30,60)):
                随机假人 = self.假人[random.randint(0,len(self.假人)-1)]
                try:
                    for user in alluser:
                            if alluser[user].gamedata.当前地图[1] == '天墉城':
                                alluser[user].客户句柄.send(随机假人.移动())
                                if 随机假人.x >= alluser[user].gamedata.当前坐标[0] + 80 or \
                                    随机假人.y >= alluser[user].gamedata.当前坐标[1] + 80 or \
                                        随机假人.x <= alluser[user].gamedata.当前坐标[0] - 80 or \
                                            随机假人.y <= alluser[user].gamedata.当前坐标[1] - 80:
                                    随机假人.重置假人(self.user[user])
                except:
                    continue

            for user in alluser:
                for 随机假人 in self.假人:
                    if alluser[user].gamedata.当前地图[1] == '天墉城' and\
                        随机假人.x >= alluser[user].gamedata.当前坐标[0] - 5 and \
                                    随机假人.y >= alluser[user].gamedata.当前坐标[1] - 5 and \
                                        随机假人.x <= alluser[user].gamedata.当前坐标[0] + 5 and \
                                            随机假人.y <= alluser[user].gamedata.当前坐标[1] + 5:
                        内容 = ['#Q101','#Q102','#Q103','#Q133','#Q115','#Q116','#Q156','#Q167','#Q166','#Q165']
                        server.服务器发送(server.基础功能.喊话(随机假人.假人id,随机假人.名称,1,random.choice(内容)),alluser[user])
                        #def 喊话(self,id,名字,频道,内容):
            threading.Event().wait(10)

    def 假人线程(self,server,user,假人类型):
        for a in range(50):
            if 假人类型 == '所有':
                temp = self.假人[a*50:a*50+50]
            elif 假人类型 == '擂台':
                temp = self.擂台假人[a*50:a*50+50]
            elif 假人类型 == '商会':
                temp = self.商会假人[a*50:a*50+50]
            elif 假人类型 == '拍卖':
                temp = self.拍卖行假人[a*50:a*50+50]
            elif 假人类型 == '活动大使':
                temp = self.活动大使假人[a*50:a*50+50]
            for i in temp:
                server.服务器发送(i.属性封包(),user)
                server.服务器发送(i.显示(),user)
            
            #threading.Event().wait(10)

    def 地图假人刷新(self,server,user,类型):
        if user.gamedata.假人所有 == False:
            地图所有 = threading.Thread(target=server.假人.假人线程,args=(server,user,'所有'))
            地图所有.daemon = True
            地图所有.start()
            user.gamedata.假人所有 = True
        if user.gamedata.当前坐标[0] <= 400 and user.gamedata.当前坐标[0] >= 304 and \
            user.gamedata.当前坐标[1] <= 236 and user.gamedata.当前坐标[1] >= 180 and \
                user.gamedata.假人擂台 == False:
            server.假人.假人删除线程(server,user,类型)
            地图擂台 = threading.Thread(target=server.假人.假人线程,args=(server,user,'擂台'))
            地图擂台.daemon = True
            地图擂台.start()
            user.gamedata.假人擂台 = True
        elif user.gamedata.当前坐标[0] <= 286 and user.gamedata.当前坐标[0] >= 200 and \
            user.gamedata.当前坐标[1] <= 208 and user.gamedata.当前坐标[1] >= 124 and \
                user.gamedata.假人商会 == False:
            server.假人.假人删除线程(server,user,类型)
            地图商会 = threading.Thread(target=server.假人.假人线程,args=(server,user,'商会'))
            地图商会.daemon = True
            地图商会.start()
            地图活动大使 = threading.Thread(target=server.假人.假人线程,args=(server,user,'活动大使'))
            地图活动大使.daemon = True
            地图活动大使.start()
            user.gamedata.假人商会 = True
        elif user.gamedata.当前坐标[0] <= 275 and user.gamedata.当前坐标[0] >= 192 and \
            user.gamedata.当前坐标[1] <= 124 and user.gamedata.当前坐标[1] >= 65 and \
                user.gamedata.假人拍卖行 == False:
            server.假人.假人删除线程(server,user,类型)
            地图拍卖 = threading.Thread(target=server.假人.假人线程,args=(server,user,'拍卖'))
            地图拍卖.daemon = True
            地图拍卖.start()
            user.gamedata.假人拍卖行 = True

    def 假人删除线程(self,server,user,类型):
        if 类型 == '地图':
            if user.gamedata.假人所有:
                for 假人 in server.假人.假人:
                    server.服务器发送(假人.删除假人(),user)
                user.gamedata.假人所有 = False
                #threading.Event().wait(5)
        if user.gamedata.假人擂台:
            for 擂台假人 in server.假人.擂台假人:
                server.服务器发送(擂台假人.删除假人(),user)
            user.gamedata.假人擂台 = False
            #threading.Event().wait(5)
        if user.gamedata.假人商会:
            for 商会假人 in server.假人.商会假人:
                server.服务器发送(商会假人.删除假人(),user)
            #threading.Event().wait(5)
            for 活动大使假人 in server.假人.活动大使假人:
                server.服务器发送(活动大使假人.删除假人(),user)
            user.gamedata.假人商会 = False
            #threading.Event().wait(5)
        if user.gamedata.假人拍卖行:
            for 拍卖行假人 in server.假人.拍卖行假人:
                server.服务器发送(拍卖行假人.删除假人(),user)
            user.gamedata.假人拍卖行 = False
            #threading.Event().wait(5)