from setting import *
from src.basebuffer.writebuffer import WriteBuff
import src.module.psutil
import threading
import time
class GM:
    def __init__(self,server,client) -> None:
        self.GMUSER = client
        self.GM账号 = GM账号
        self.server = server
        self.sHeartbeatd = ''
        self.挂载 = False
        self.login_check = ''
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
            
    def tGMHeartbeatd(self):
        GMhb = threading.Thread(target=self.thredHeart())
        GMhb.start()

    def thredHeart(self):
        self.GMUSER.客户句柄.close()
        while self.挂载:
            self.GMHeartbeatd()
            time.sleep(10.1)

    def GMHeartbeatd(self):
        bootTime = self.get_bufftime()
        write = WriteBuff()
        allWrite = WriteBuff()
        write.byte(bytes.fromhex('10b2'))
        write.integer(bootTime)
        write.byte(self.sHeartbeatd)
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        self.server.客户端发送(allWrite.getBuffer(),self.GMUSER)
        return
    def setsHeartbeatd(self,buffer):
        self.sHeartbeatd = buffer[12:]
        
    def get_bufftime(self):
        bootTime = int(src.module.psutil.boot_time() * 1000)
        nowTime = int(time.time() * 1000)
        bootTime = nowTime - bootTime
        return bootTime
        
    def login_acc(self):
        #4D 5A 00 00 4E E0 8B 42 00 8C 23 50 06 68 61 63 6B 7A 79 40 38 37 34 33 35 31 43 37 46 35 44 45 41 39 33 44 34 45 43 31 39 36 46 42 45 35 44 30 31 33 39 33 43 41 41 42 31 32 46 38 42 46 37 30 46 42 35 44 37 39 36 43 38 42 41 35 42 30 39 34 39 33 41 32 10 30 30 30 30 33 34 36 34 61 39 30 61 62 62 30 39 00 00 0C E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C 00 20 37 33 34 45 30 31 45 32 31 30 42 31 38 46 36 36 44 33 35 38 41 45 35 32 41 33 34 31 34 33 46 33 
        write = WriteBuff()
        allWrite = WriteBuff()
        write.integer(self.get_bufftime())
        write.byte(bytes.fromhex('00 8C 23 50 06 68 61 63 6B 7A 79 40 38 37 34 33 35 31 43 37 46 35 44 45 41 39 33 44 34 45 43 31 39 36 46 42 45 35 44 30 31 33 39 33 43 41 41 42 31 32 46 38 42 46 37 30 46 42 35 44 37 39 36 43 38 42 41 35 42 30 39 34 39 33 41 32 10 30 30 30 30 33 34 36 34 61 39 30 61 62 62 30 39 00 00 0C E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C 00 20 37 33 34 45 30 31 45 32 31 30 42 31 38 46 36 36 44 33 35 38 41 45 35 32 41 33 34 31 34 33 46 33 '))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.byte(write.getBuffer())
        return allWrite.getBuffer()
    
    def login_acc_5351(self):
        #4D 5A 00 00 4E E0 8B DE 00 1B 33 54 06 68 61 63 6B 7A 79 E8 39 FC 3D 0C E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C 02 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('33 54 06 68 61 63 6B 7A 79'))
        write.byte(self.login_check)
        write.byte(bytes.fromhex('0C E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C 02'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_4355(self):
        #4D 5A 00 00 4E E0 90 EF 00 20 33 56 06 68 61 63 6B 7A 79 E8 39 FC 3D 12 E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C E4 B8 80 E7 B7 9A 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('33 56 06 68 61 63 6B 7A 79'))
        write.byte(self.login_check)
        write.byte(bytes.fromhex('12 E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C E4 B8 80 E7 B7 9A'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_3357(self):
        #4D 5A 00 00 4E E0 94 89 01 07 30 02 06 68 61 63 6B 7A 79 E8 39 FC 3D 6A F4 2A E9 41 37 33 34 45 30 31 45 32 31 30 42 31 38 46 36 36 44 33 35 38 41 45 35 32 41 33 34 31 34 33 46 33 3A 33 37 41 36 32 35 39 43 43 30 43 31 44 41 45 32 39 39 41 37 38 36 36 34 38 39 44 46 46 30 42 44 03 00 B1 32 47 32 36 32 30 30 32 33 31 36 36 20 57 47 49 4C 31 58 55 41 5F 33 34 36 34 61 39 30 61 62 62 30 39 5F 33 34 36 34 61 39 30 61 62 62 30 39 5F 30 30 66 66 66 33 62 34 61 33 31 62 5F 30 30 66 66 66 33 62 34 61 33 31 62 5F 30 30 66 66 38 61 32 36 35 34 30 65 5F 30 30 66 66 38 61 32 36 35 34 30 65 5F 30 30 35 30 35 36 63 30 30 30 30 30 5F 30 30 35 30 35 36 63 30 30 30 30 30 5F 30 30 31 35 38 33 33 64 30 61 35 37 5F 30 30 31 35 38 33 33 64 30 61 35 37 5F 30 30 65 30 34 63 36 39 62 65 34 64 5F 30 30 65 30 34 63 36 39 62 65 34 64 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('30 02 06 68 61 63 6B 7A 79'))
        write.byte(self.login_check)
        write.byte(bytes.fromhex('6A F4 2A E9 41 37 33 34 45 30 31 45 32 31 30 42 31 38 46 36 36 44 33 35 38 41 45 35 32 41 33 34 31 34 33 46 33 3A 33 37 41 36 32 35 39 43 43 30 43 31 44 41 45 32 39 39 41 37 38 36 36 34 38 39 44 46 46 30 42 44 03 00 B1 32 47 32 36 32 30 30 32 33 31 36 36 20 57 47 49 4C 31 58 55 41 5F 33 34 36 34 61 39 30 61 62 62 30 39 5F 33 34 36 34 61 39 30 61 62 62 30 39 5F 30 30 66 66 66 33 62 34 61 33 31 62 5F 30 30 66 66 66 33 62 34 61 33 31 62 5F 30 30 66 66 38 61 32 36 35 34 30 65 5F 30 30 66 66 38 61 32 36 35 34 30 65 5F 30 30 35 30 35 36 63 30 30 30 30 30 5F 30 30 35 30 35 36 63 30 30 30 30 30 5F 30 30 31 35 38 33 33 64 30 61 35 37 5F 30 30 31 35 38 33 33 64 30 61 35 37 5F 30 30 65 30 34 63 36 39 62 65 34 64 5F 30 30 65 30 34 63 36 39 62 65 34 64'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_1060(self):
        #4D 5A 00 00 4E E0 99 6B 00 12 10 60 0F E6 AD BB E6 B4 BB E8 A6 81 E5 95 8F E9 81 93 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('10 60 0F E6 AD BB E6 B4 BB E8 A6 81 E5 95 8F E9 81 93'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_1003(self):
        #4D 5A 00 00 4E E0 A1 6A 00 02 13 A4 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('00 02 13 A4'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_1003_2(self):
        #4D 5A 00 00 4E E0 A1 99 01 82 F5 11 01 7E 33 32 31 37 38 31 36 35 37 35 2C 47 65 6E 75 69 6E 65 49 6E 74 65 6C 7C 3A 35 38 36 2C 38 2C 36 2C 31 35 33 36 33 2C 33 2E 36 30 47 48 7A 7C 3A 32 47 32 36 32 30 30 32 33 31 36 36 20 57 47 49 4C 31 58 55 41 7C 3A 33 34 36 34 61 39 30 61 62 62 30 39 2C 33 34 36 34 61 39 30 61 62 62 30 39 2C 30 30 66 66 66 33 62 34 61 33 31 62 2C 30 30 66 66 66 33 62 34 61 33 31 62 2C 30 30 66 66 38 61 32 36 35 34 30 65 2C 30 30 66 66 38 61 32 36 35 34 30 65 2C 30 30 35 30 35 36 63 30 30 30 30 30 2C 30 30 35 30 35 36 63 30 30 30 30 30 2C 30 30 31 35 38 33 33 64 30 61 35 37 2C 30 30 31 35 38 33 33 64 30 61 35 37 2C 30 30 65 30 34 63 36 39 62 65 34 64 2C 30 30 65 30 34 63 36 39 62 65 34 64 7C 3A 31 36 33 30 36 7C 3A 33 2C 55 53 42 20 4D 6F 62 69 6C 65 20 4D 6F 6E 69 74 6F 72 20 56 69 72 74 75 61 6C 20 44 69 73 70 6C 61 79 2C 49 6E 74 65 6C 28 52 29 20 48 44 20 47 72 61 70 68 69 63 73 20 34 36 30 30 2C 4E 56 49 44 49 41 20 47 65 46 6F 72 63 65 20 47 54 58 20 31 30 36 30 20 33 47 42 7C 3A 34 31 39 34 32 34 30 7C 3A 7C 3A 31 7C 3A 32 3B 36 3B 32 3B 3B 31 3B 32 35 36 3B 30 3B 75 6E 6B 6E 6F 77 6E 20 76 65 72 73 69 6F 6E 7C 3A 31 2E 35 32 2E 30 36 32 37 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('01 82 F5 11 01 7E 33 32 31 37 38 31 36 35 37 35 2C 47 65 6E 75 69 6E 65 49 6E 74 65 6C 7C 3A 35 38 36 2C 38 2C 36 2C 31 35 33 36 33 2C 33 2E 36 30 47 48 7A 7C 3A 32 47 32 36 32 30 30 32 33 31 36 36 20 57 47 49 4C 31 58 55 41 7C 3A 33 34 36 34 61 39 30 61 62 62 30 39 2C 33 34 36 34 61 39 30 61 62 62 30 39 2C 30 30 66 66 66 33 62 34 61 33 31 62 2C 30 30 66 66 66 33 62 34 61 33 31 62 2C 30 30 66 66 38 61 32 36 35 34 30 65 2C 30 30 66 66 38 61 32 36 35 34 30 65 2C 30 30 35 30 35 36 63 30 30 30 30 30 2C 30 30 35 30 35 36 63 30 30 30 30 30 2C 30 30 31 35 38 33 33 64 30 61 35 37 2C 30 30 31 35 38 33 33 64 30 61 35 37 2C 30 30 65 30 34 63 36 39 62 65 34 64 2C 30 30 65 30 34 63 36 39 62 65 34 64 7C 3A 31 36 33 30 36 7C 3A 33 2C 55 53 42 20 4D 6F 62 69 6C 65 20 4D 6F 6E 69 74 6F 72 20 56 69 72 74 75 61 6C 20 44 69 73 70 6C 61 79 2C 49 6E 74 65 6C 28 52 29 20 48 44 20 47 72 61 70 68 69 63 73 20 34 36 30 30 2C 4E 56 49 44 49 41 20 47 65 46 6F 72 63 65 20 47 54 58 20 31 30 36 30 20 33 47 42 7C 3A 34 31 39 34 32 34 30 7C 3A 7C 3A 31 7C 3A 32 3B 36 3B 32 3B 3B 31 3B 32 35 36 3B 30 3B 75 6E 6B 6E 6F 77 6E 20 76 65 72 73 69 6F 6E 7C 3A 31 2E 35 32 2E 30 36 32 37'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_1b01_1(self):
        #4D 5A 00 00 4E E0 A7 36 00 0D 1B 01 00 09 03 AA 08 FF 00 00 02 FF FF 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('1B 01 00 09 03 AA 08 FF 00 00 02 FF FF'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_1b01_2(self):
        #4D 5A 00 00 4E E0 A7 56 00 5E 1B 01 00 5A 03 4C 08 FF 00 00 04 53 7B 5A 61 78 96 D1 46 F8 64 65 65 5E 15 AD 36 2F D4 79 0A E2 57 AC FB C4 C3 F8 62 08 0B 9F 31 B7 C1 4E 10 00 D4 31 22 82 23 82 FF 18 11 87 09 73 D5 BE 76 AD 70 91 D3 63 E8 97 80 52 3D 54 45 18 31 35 46 1C 61 3D 25 64 BC 9A B4 B7 C5 6B 3D 96 AA 48 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('1B 01 00 5A 03 4C 08 FF 00 00 04 53 7B 5A 61 78 96 D1 46 F8 64 65 65 5E 15 AD 36 2F D4 79 0A E2 57 AC FB C4 C3 F8 62 08 0B 9F 31 B7 C1 4E 10 00 D4 31 22 82 23 82 FF 18 11 87 09 73 D5 BE 76 AD 70 91 D3 63 E8 97 80 52 3D 54 45 18 31 35 46 1C 61 3D 25 64 BC 9A B4 B7 C5 6B 3D 96 AA 48 '))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def GM_login(self):
        self.GMUSER.账号 = GM账号
        self.GMUSER.客户端启动(游戏IP,游戏端口[0])
        self.GMUSER.服务器句柄.send(self.login_acc())
        
    def GM_login_line(self):
        self.GMUSER.客户端启动(游戏IP,游戏端口[1])
        