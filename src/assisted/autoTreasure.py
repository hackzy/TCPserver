from src.basebuffer.writebuffer import WriteBuff
import time
class AutoTreasure:
    flag = False
    def getTreasurePot(self,user,server):
        return server.基础功能.getItemPot(user,'藏寶圖')
    def getHoe(self,user,server):
        return server.基础功能.getItemPot(user,'鋤頭')
    
    def buyHoe(self,user,server):
        xianlingkaPot = server.基础功能.getItemPot(user,'仙靈卡')
        if xianlingkaPot == 0:
            server.基礎功能.商城购买道具(user,'仙靈卡')
            xianlingkaPot = server.基础功能.getItemPot(user,'仙靈卡')
        server.客户端发送(user.fuzhu.使用物品(xianlingkaPot),user)
        time.sleep(1)
        server.客户端发送(server.基础功能.对话点击(user.gamedata.角色id,'打開商店'),user)
        time.sleep(1)
        server.客户端发送(bytes.fromhex('4D 5A 00 00 22 4B 9D C9 00 0C 30 44 00 00 5D C9 00 0C 00 01 00 67 '.replace(' ','')),user)
        time.sleep(0.3)
        server.客户端发送(bytes.fromhex('4d5a0000000000000006003c00005e40'),user)
        
    def startTreasure(self,user,server):
        try:
            while True:
                if self.flag == False:
                    return
                treasPot = self.getTreasurePot(user,server)
                if treasPot == 0:
                    self.flag = False
                    server.客户端发送(server.基础功能.中心提示('當前背包裏沒有藏寶圖！'),user)
                    return
                hoe = self.getHoe(user,server)
                if hoe == 0:
                    self.buyHoe(user,server)
                    hoe = self.getHoe(user,server)
                #server.客户端发送(user.fuzhu.使用技能(308),user)
                loca = None
                for task in user.gamedata.任务:
                    if task.find('寶藏') != -1:
                        break
                if user.gamedata.任务[task] == '' or task.find('寶藏') == -1:
                    server.客户端发送(user.fuzhu.使用物品(treasPot),user)
                    time.sleep(1)
                    continue
                loca = user.gamedata.任务[task].split('#Z')
                server.客户端发送(server.基础功能.T8飞NPC(loca[1],user,True),user)#T8飞NPC(self,NPC,user,bTask = False):
                time.sleep(0.3)
                server.客户端发送(user.fuzhu.使用物品(hoe),user)
                time.sleep(0.3)
            
        except:
            return