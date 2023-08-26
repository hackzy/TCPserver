from src.basebuffer.writebuffer import WriteBuff
from src.basebuffer.readBuffer import ReadBuffer
from setting import *
import threading 
from datetime import datetime
import src.module.psutil as psutil
import time
class 基础功能:

    def 中心提示(self,内容):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('1fe5'))
        write.string(内容,True,1)
        write.integer(0)
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()

    def 左下角提示(self,内容):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('0b0d'))
        write.integer(0)
        write.integer(0,2)
        write.string(内容,True,1)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        write.string(current_time)
        write.byte(bytes.fromhex('0000'))
        write.string('一线')
        write.integer(3,2)
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def 输入框(self,ID:int,形象ID:int,内容:str,名字:str):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('2037'))
        write.integer(ID)
        write.integer(形象ID)
        write.integer(1,2)
        内容 = '[@请输入/!^请输入#prompt:' + 内容 + ']'
        write.string(内容,True,1)
        write.integer(0)
        write.string(名字)
        write.integer(80)
        write.byte(b'00')
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def NPC对话包(self,ID,形象ID,对话内容,名字):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('2037'))
        write.integer(ID)
        write.integer(形象ID)
        write.byte(b'\x00\x01')
        write.string(对话内容,True,1)
        write.integer(0)
        write.string(名字,True)
        write.integer(0)
        write.byte(b'\x00')
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def 战斗时间(self,buffer):
        read = ReadBuffer()
        write = WriteBuff()
        read.setBuffer(buffer)
        write.byte(read.byte(19))
        write.byte (b'\x04')
        read.skip(1)
        write.byte(read.residBuffer())
        return write.getBuffer()
    
    def 奖励_上升提示(self,数值,奖励类型):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('3b04'))
        write.string(奖励类型,True)
        write.integer(数值)
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def 系统邮件(self,内容):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('3fff'))
        write.integer(9,2)
        write.integer(0)
        write.integer(1,2)
        write.string(内容,True)
        write.integer(1687423220)
        write.integer(0,2)
        write.string('更铸辉煌一线',True)
        write.integer(3,2)
        write.integer(363)
        write.string('奥斯卡赌神',True)
        write.integer(0)
        write.integer(0)
        write.integer(0,2)
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()

    def getItemPot(self,user,item:str,vague = True):
        for key in user.gamedata.物品数据:
            if vague:
                if user.gamedata.物品数据[key].名称.find(item) != -1:
                    return key
            else:
                if user.gamedata.物品数据[key].名称 == item:
                    return key
        return 0
            
    def T8飞NPC(self,NPC,user,bTask = False):
        write = WriteBuff()
        allWrite = WriteBuff()
        if bTask:
            物品id = 4294967295
            flytype = '10'
        else:
            物品id = self.取背包物品id('特级八卦阴阳令',user)
            if 物品id == 0:
                self.商城购买道具(user,'特级八卦阴阳令')
                物品id = self.取背包物品id('特级八卦阴阳令',user)
            flytype = '02'
        write.byte(bytes.fromhex('40ce'))
        write.integer(物品id)
        write.byte(bytes.fromhex(flytype))
        write.byte(bytes.fromhex('000001'))
        write.string(NPC,True)
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def 商城购买道具(self,user,道具,数量 = 1):
        try:
            if user.gamedata.商城数据 == {}:
                user.服务器句柄.send(bytes.fromhex('4D 5A 00 00 0E 19 7A 8C 00 2C 3E 24 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '.replace(' ',"")))
            threading.Event().wait(2)
            write = WriteBuff()
            allWrite = WriteBuff()
            write.byte(bytes.fromhex('1166'))
            write.string(user.gamedata.商城数据[道具][0],True)
            write.integer(数量,2)
            write.string(user.gamedata.商城数据[道具][1],True,1)
            write.byte(bytes.fromhex('00'))
            allWrite.byte(组包包头)
            allWrite.byte(write.getBuffer(),True,1)
            user.服务器句柄.send(allWrite.getBuffer()) 
        except:
            user.服务器句柄.send(bytes.fromhex('4D 5A 00 00 0E 19 7A 8C 00 2C 3E 24 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 '.replace(' ',"")))

    def 喊话(self,id,名字,频道,内容):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('3fff'))
        write.integer(频道,2)
        write.integer(id)
        write.string(名字,True)
        write.string('#dFFFFFF' + 内容,True,1)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        write.string(current_time)
        write.byte(bytes.fromhex('0000'))
        write.string('一线',True)
        write.integer(3,2) #大表情模式
        write.integer(len(内容))
        write.byte(bytes.fromhex('00000000000000000000A0000100010000000000'))
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def 对话点击(self,id,对话):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('30ca'))
        write.integer(id)
        write.string(对话)
        write.byte(bytes.fromhex('00'))
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def getBootTime(self):
        boot_time = psutil.boot_time() * 1000
        now = time.time() * 1000
        return int(now - boot_time)