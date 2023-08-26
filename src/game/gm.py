from setting import *
from src.basebuffer.writebuffer import WriteBuff
import src.module.psutil
import threading
import time
class GM:
    def __init__(self,server) -> None:
        self.GMUSER = None
        self.GM账号 = GM账号
        self.server = server
        self.sHeartbeatd = b''
        self.挂载 = False

    def GM_SEND(self,玩家昵称,角色id,命令,值):
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('fae0'))
        write.string('admin_set_attrib',True)
        write.string(玩家昵称,True)
        write.string(str(角色id),True)
        write.string(命令,True)
        write.string(str(值),True)
        allWrite.byte(组包包头)
        allWrite.byte(write.getBuffer(),True,1)
        if self.GMUSER != None:
            self.server.客户端发送(allWrite.getBuffer(),self.GMUSER)

    def 元宝寄售(self,buffer):
        包头 = buffer[10:12]
        if 包头.hex() == '0a01':
            self.server.客户端发送(buffer,self.GMUSER)
        elif 包头.hex() == '1101':
            evnt = threading.Event()
            if len(buffer) == 15:
                self.server.客户端发送(bytes.fromhex('4D 5A 00 00 22 0D 14 A1 00 03 23 0A 01 '.replace(' ','')),self.GMUSER)
                evnt.wait(1)
                self.GM_SEND(self.GMUSER.gamedata.角色名,self.GMUSER.gamedata.角色id,'cash','0')
                evnt.wait(1)
                self.server.客户端发送(bytes.fromhex('4D 5A 00 00 22 0D 2A D9 00 0B FD 18 01 00 0F 42 40 00 00 03 E8 '.replace(' ','')),self.GMUSER)
                evnt.wait(1)
                self.server.客户端发送(bytes.fromhex('4D 5A 00 00 22 0D 2A D9 00 0B FD 18 01 00 0F 42 40 00 00 03 E8 '.replace(' ','')),self.GMUSER)

    def 检查元宝(self):
        while self.GMUSER != None:
            self.元宝寄售(bytes.fromhex('4D 5A 00 00 08 32 C0 74 00 03 28 0A 01 '.replace(' ','')),)
            if self.GMUSER == None:
                break
            time.sleep(60)
            
    def tGMHeartbeatd(self):
        GMhb = threading.Thread(target=self.thredHeart())
        GMhb.daemon = True
        GMhb.start()

    def thredHeart(self):
        self.GMUSER.客户句柄.close()
        while self.挂载:
            self.GMHeartbeatd()
            time.sleep(10.1)

    def GMHeartbeatd(self):
        bootTime = int(src.module.psutil.boot_time() * 1000)
        nowTime = int(time.time() * 1000)
        bootTime = nowTime - bootTime
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('20d2'))
        write.integer(bootTime)
        write.byte(self.sHeartbeatd)
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        self.server.客户端发送(allWrite.getBuffer(),self.GMUSER)
        return
    def setHeartbeatd(self,buffer):
        self.sHeartbeatd = buffer[12:]