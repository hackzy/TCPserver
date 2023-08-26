from src.basebuffer.readBuffer import ReadBuffer
from src.basebuffer.writebuffer import WriteBuff
from threading import  Thread
from src.plug.saveData import 存档
from setting import *
class 客户请求处理:
    def __init__(self,user,server) -> None:
        self.user = user
        self.server = server

    def 喊话(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        频道 = read.integer(2)
        read.skip(5)
        内容 = read.string()
        内容 = 内容[8:]
        if 内容 == "LZKS":
            self.user.fuzhu.luzhi.录制开始()
            return
        elif 内容 == 'LZTZ':
            self.user.fuzhu.luzhi.录制停止()
            return
        elif 内容 == 'LZFSKS':
            self.user.fuzhu.luzhi.发送开始()
            return
        elif 内容 == 'LZFSTZ':
            self.user.fuzhu.luzhi.发送停止()
            return
        elif 内容.find('SZLZYS') != -1:
            self.user.fuzhu.luzhi.设置延时(内容)
            return
        elif 内容 == 'LZFS':
            self.user.fuzhu.luzhi.单次发送()
            return
        elif 内容.find('BCLZ') != -1:
            self.user.fuzhu.luzhi.设置延时(内容)
            return
        elif 内容.find('fbcs') != -1:
            self.server.测试 = self.user
        elif 内容 == 'GZ' and self.user.账号 == GM账号:
            self.server.GM.挂载 = True
            return
        return buffer
    
    def NPC对话点击处理(self,buffer):
        解包 = self.取对话内容(buffer)
        npcid = 解包[0]
        内容 = 解包[1]
        填写内容 = 解包[2]
        if npcid == 10:
            self.user.fuzhu.小助手.助手处理中心(内容)
        elif npcid == 2:
            self.user.fuzhu.小助手.助手_自动战斗(内容)
        elif npcid == 3:
            self.user.fuzhu.小助手.装备相关(内容)
        elif npcid == 4:
            if 填写内容 != '':
                self.user.fuzhu.小助手.录制相关(内容,填写内容)
                return
            self.user.fuzhu.小助手.录制相关(内容)
        elif npcid == 5:
            self.user.fuzhu.小助手.自动挖宝(内容)


    def 取对话内容(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        npcid = read.integer()
        内容 = read.string()
        填写内容 = read.string()
        return [npcid,内容,填写内容]
    
    def 选择角色(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        昵称 = read.string()
        for a in self.user.gamedata.所有角色:
            if self.user.gamedata.所有角色[a]['名称'] == 昵称:
                self.user.gamedata.GID = self.user.gamedata.所有角色[a]['GID']
                self.server.写日志('玩家：'+ 昵称 + ' 上线 ip:'+self.user.客户IP+'  当前在线人数:'+str(len(self.server.user)))
                break

    def 取账号(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        self.user.账号 = read.string()
        if self.user.账号 == GM账号:
            self.server.GM.GMUSER = self.user
            self.server.写日志('GM号已上线,现在可执行GM操作')
            t = Thread(target=self.server.GM.检查元宝)
            t.daemon = True
            t.start()

    def 心法处理(self,buffer):
        read = ReadBuffer()
        read.setBuffer(buffer)
        read.skip(12)
        NPCID = read.integer()
        对象ID = read.integer()
        技能id = read.byte(2).hex().upper()
        for xf in 心法:
            if 技能id == xf.split('|')[1]:
                self.server.服务器发送(self.server.基础功能.中心提示("操作非法!"),self.user)
                return b''
        return buffer
    
    def 切换加点(self):
        #4D 5A 00 00 0F 33 3B 55 00 02 FD A6 
        write = WriteBuff()
        write.byte(b'MZ\x00\x00')
        write.integer(self.server.基础功能.getBootTime())
        write.integer(2,2)
        write.byte(bytes.fromhex('fda6'))
        return write.getBuffer()