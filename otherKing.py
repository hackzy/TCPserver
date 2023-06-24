from bufferWrit import 写封包
from recBuffer import 读封包
from setting import *
import threading 
class 基础功能:

    def 中心提示(self,内容):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('1fe5'))
        写.写文本型(内容,True,1,True)
        写.写整数型(0)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1,True)

        return 完整包.取数据()

    def 左下角提示(self,内容):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('2fff'))
        写.写整数型(0,True)
        写.写整数型(0,True)
        写.写文本型(内容,True)
        写.写字节集(bytes.fromhex('00 00 00\
                     00 00 00 12 E6 9B B4 E9\
                     91 84 E8 BC 9D E7 85 8C \
                    E4 B8 80 E7 B7 9A 00 01'\
                             .replace(" ","")))
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1,True)
        return 完整包.取数据()

    def NPC对话包(self,ID,形象ID,对话内容,名字):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('2037'))
        写.写整数型(ID,True)
        写.写整数型(形象ID,True)
        写.写字节集(b'\x00\x01')
        写.写文本型(对话内容,True,1,True)
        写.写整数型(0)
        写.写文本型(名字,True)
        写.写整数型(0)
        写.写字节型(b'\x00')
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1,True)
        return 完整包.取数据()
    
    def 战斗时间(self,buffer):
        读 = 读封包()
        写 = 写封包()
        读.置数据 (buffer)
        写.写字节集 (读.读字节集 (19))
        写.写字节型 (b'\x04')
        读.跳过 (1)
        写.写字节集 (读.剩余数据 ())
        return 写.取数据()
    
    def 奖励_上升提示(self,数值,奖励类型):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('3b04'))
        写.写文本型(奖励类型,True)
        写.写整数型(数值,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        return 完整包.取数据()
    
    def 系统邮件(self,内容):
        
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('3fff'))
        写.写短整数型(9,True)
        写.写整数型(0,True)
        写.写短整数型(1,True)
        写.写文本型(内容,True)
        写.写整数型(1687423220,True)
        写.写短整数型(0,True)
        写.写文本型('更鑄輝煌一線',True)
        写.写短整数型(3,True)
        写.写整数型(363,True)
        写.写文本型('奧斯卡賭神',True)
        写.写整数型(0,True)
        写.写整数型(0,True)
        写.写短整数型(0,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        return 完整包.取数据()

    def 取背包物品id(self,物品名称,user):
        for item in user.gamedata.背包数据:
            if item.名称 == 物品名称:
                return item.id
            
    def T8飞NPC(self,NPC,user):
        写 = 写封包()
        完整包 = 写封包()
        物品id = self.取背包物品id('特級八卦陰陽令',user)
        if 物品id == 0:
            self.商城购买道具(user,'特級八卦陰陽令')
        写.写字节集(bytes.fromhex('40ce'))
        写.写整数型(物品id,True)
        写.写字节集(bytes.fromhex('02000001'))
        写.写文本型(NPC,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        return 完整包.取数据()
    
    def 商城购买道具(self,user,道具,数量 = 1):
        threading.Event().wait(2)
        try:
            if user.gamedata.商城数据 == {}:
                user.服务器句柄.send(bytes.fromhex('4D 5A 00 00 78 70 7B 99 00 14 00 D8 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '.replace(' ',"")))
            写 = 写封包()
            完整包 = 写封包()
            写.写字节集(bytes.fromhex('20da'))
            写.写文本型(user.gamedata.商城数据[道具][0],True)
            写.写短整数型(数量,True)
            写.写文本型(user.gamedata.商城数据[道具][1],True,1,True)
            完整包.写字节集(组包包头)
            完整包.写字节集(写.取数据(),True,1)
            print(完整包.取数据().hex())
            user.服务器句柄.send(完整包.取数据()) 
        except:
            user.服务器句柄.send(bytes.fromhex('4D 5A 00 00 78 70 7B 99 00 14 00 D8 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '.replace(' ',"")))


    def 一键鉴定(self,user):
        for back in user.gamedata.物品数据:
            if back.位置id > 100:
                写 = 写封包()
                写.写字节集(组包包头)
                写.写字节集(bytes.fromhex('0006301c'))
                写.写整数型(back.位置id,True)
                user.服务器句柄.send(写.取数据())
                threading.Event().wait(timeout=0.2)

    def 鉴定二级对话(self,user,NPCID,对话内容):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('3038'))
        写.写整数型(NPCID,True)
        if 对话内容.find('花費') != -1:
            写.写文本型('確定',True)
        else:
            写.写文本型(user.fuzhu.鉴定类型,True)
        写.写字节型(b'\x00')
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        user.服务器句柄.send(完整包.取数据())
        