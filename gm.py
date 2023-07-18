from setting import *
from writebuffer import 写封包
import psutil
import threading
class GM:
    def __init__(self,server) -> None:
        self.GMUSER = None
        self.GM账号 = GM账号
        self.server = server

    def GM_SEND(self,玩家昵称,角色id,命令,值):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('fae0'))
        写.写文本型('admin_set_attrib',True)
        写.写文本型(玩家昵称,True)
        写.写文本型(str(角色id),True)
        写.写文本型(命令,True)
        写.写文本型(str(值),True)
        完整包.写字节集(bytes.fromhex('4d5a0000'))
        完整包.写整数型(int(psutil.boot_time()),True)
        完整包.写字节集(写.取数据(),True,1,True)
        if self.GMUSER != None:
            self.server.客户端发送(完整包.取数据(),self.GMUSER)

    def 元宝寄售(self,buffer):
        包头 = buffer[10:12]
        if 包头.hex() == '2300':
            self.server.客户端发送(buffer,self.GMUSER)
        elif 包头.hex() == '2301':
            evnt = threading.Event()
            if len(buffer) == 15:
                self.server.客户端发送(bytes.fromhex('4D 5A 00 00 22 0D 14 A1 00 03 23 0A 01 '.replace(' ','')),self.GMUSER)
                evnt.wait(1)
                self.GM_SEND(self.GMUSER.gamedata.角色名,self.GMUSER.gamedata.角色id,'cash','0')
                evnt.wait(1)
                self.server.客户端发送(bytes.fromhex('4D 5A 00 00 22 0D 2A D9 00 0B 23 06 01 00 0F 42 40 00 00 03 E8 '.replace(' ','')),self.GMUSER)
                evnt.wait(1)
                self.server.客户端发送(bytes.fromhex('4D 5A 00 00 22 0D 2A D9 00 0B 23 06 01 00 0F 42 40 00 00 03 E8 '.replace(' ','')),self.GMUSER)

    def 检查元宝(self):
        while True:
            t = threading.Timer(60,self.元宝寄售,args=(bytes.fromhex('4D 5A 00 00 20 71 0B 7D 00 03 23 00 01 '.replace(' ','')),))
            t.start()
            t.join()
            if self.GMUSER == None:
                break
            