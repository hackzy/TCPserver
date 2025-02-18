from setting import *
from src.basebuffer.writebuffer import WriteBuff
import src.module.psutil
import threading
import time
import pymysql


class GM:
    def __init__(self,server,client) -> None:
        self.GMUSER = client
        self.GM账号 = GM账号
        self.server = server
        self.sHeartbeatd = b''
        self.挂载 = False
        self.login_check = b''
        self.login_line_check = b''
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
                self.删寄售数据()
                self.server.客户端发送(bytes.fromhex('4D 5A 00 00 22 0D 14 A1 00 03 23 0A 01 '),self.GMUSER)
                evnt.wait(1)
                self.GM_SEND(self.GMUSER.gamedata.角色名,self.GMUSER.gamedata.角色id,'cash','0')
                evnt.wait(1)
                self.server.客户端发送(bytes.fromhex('4D 5A 00 00 22 0D 2A D9 00 0B 23 06 01 00 0F 42 40 00 00 03 E8 '),self.GMUSER)
                evnt.wait(1)
                self.server.客户端发送(bytes.fromhex('4D 5A 00 00 22 0D 2A D9 00 0B 23 06 01 00 0F 42 40 00 00 03 E8 '),self.GMUSER)
                
    def 删寄售数据(self):
        try:
            self.mysql = pymysql.connect(host=数据库ip,port=sqlport,password=数据库密码,user=数据库用户,charset='utf8',database='ddb')
        except:
            self.server.写日志('删寄售数据时，数据库连接失败')
            return
        cur = self.mysql.cursor()
        if cur.execute("DELETE FROM ddb.data WHERE (`path`='coin_trade_store')"):
            self.server.写日志('删寄售数据成功！')
            self.mysql.commit()
            self.mysql.close()
        
    def 检查元宝(self):
        self.server.写日志('开始定时检查元宝')
        while self.挂载:
            self.元宝寄售(bytes.fromhex('4D 5A 00 00 20 71 0B 7D 00 03 23 00 01'))
            time.sleep(60)
            if not self.挂载:
                break
            
    def tGMHeartbeatd(self):
        GMhb = threading.Thread(target=self.thredHeart)
        GMhb.daemon = True
        GMhb.start()
        self.server.写日志('GM号已上线,现在可执行GM操作')
        t = threading.Thread(target=self.检查元宝)
        t.daemon = True
        t.start()


    def thredHeart(self):
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
        self.GMUSER.服务器句柄.send(allWrite.getBuffer())
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
        write.byte(bytes.fromhex('00 8D 23 50 07 68 61 63 6B 7A 79 32 40 38 37 34 33 35 31 43 37 46 35 44 45 41 39 33 44 34 45 43 31 39 36 46 42 45 35 44 30 31 33 39 33 43 41 41 42 31 32 46 38 42 46 37 30 46 42 35 44 37 39 36 43 38 42 41 35 42 30 39 34 39 33 41 32 10 30 30 30 30 33 34 36 34 61 39 30 61 62 62 30 39 00 00 0C E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C 00 20 37 33 34 45 30 31 45 32 31 30 42 31 38 46 36 36 44 33 35 38 41 45 35 32 41 33 34 31 34 33 46 33'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.byte(write.getBuffer())
        return allWrite.getBuffer()
    
    def login_acc_5351(self):
        #4D 5A 00 00 4E E0 8B DE 00 1B 33 54 06 68 61 63 6B 7A 79 E8 39 FC 3D 0C E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C 02 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('33 54 07 68 61 63 6B 7A 79 32 '))
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
        write.byte(bytes.fromhex('33 56 07 68 61 63 6B 7A 79 32 '))
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
        write.byte(bytes.fromhex('30 02 07 68 61 63 6B 7A 79 32 '))
        write.byte(self.login_check)
        write.byte(self.login_line_check)
        write.byte(bytes.fromhex(' 41 37 33 34 45 30 31 45 32 31 30 42 31 38 46 36 36 44 33 35 38 41 45 35 32 41 33 34 31 34 33 46 33 3A 33 37 41 36 32 35 39 43 43 30 43 31 44 41 45 32 39 39 41 37 38 36 36 34 38 39 44 46 46 30 42 44 03 00 B1 32 47 32 36 32 30 30 32 33 31 36 36 20 57 47 49 4C 31 58 55 41 5F 33 34 36 34 61 39 30 61 62 62 30 39 5F 33 34 36 34 61 39 30 61 62 62 30 39 5F 30 30 66 66 66 33 62 34 61 33 31 62 5F 30 30 66 66 66 33 62 34 61 33 31 62 5F 30 30 66 66 38 61 32 36 35 34 30 65 5F 30 30 66 66 38 61 32 36 35 34 30 65 5F 30 30 35 30 35 36 63 30 30 30 30 30 5F 30 30 35 30 35 36 63 30 30 30 30 30 5F 30 30 31 35 38 33 33 64 30 61 35 37 5F 30 30 31 35 38 33 33 64 30 61 35 37 5F 30 30 65 30 34 63 36 39 62 65 34 64 5F 30 30 65 30 34 63 36 39 62 65 34 64'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_1060(self):
        #4D 5A 00 00 4E E0 99 6B 00 12 10 60 0F E6 AD BB E6 B4 BB E8 A6 81 E5 95 8F E9 81 93 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('10 60 0F E5 A5 A7 E6 96 AF E5 8D A1 E8 B3 AD E7 A5 9E '))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_10d1(self):
        # 4D 5A 00 00 50 51 F8 CE 00 03 10 D1 00 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('00 03 10 D1 00'))
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
        write.byte(bytes.fromhex('1B 01 00 4C 07 7C 08 FF 00 00 04 14 E7 F3 5C B5 29 59 62 C1 4E 52 ED 2F 98 AA 71 91 24 74 53 B4 ED 12 68 55 F9 16 CB F7 86 A2 65 24 E5 D8 7D 3E 9A 83 83 AE 82 55 31 A0 B3 76 11 4D 8B 2E 5D DD 7B 64 79 45 F7 13 24 BE B0 B6 DD 45 A5 B3 1A B2 '))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()

    def login_acc_success(self):
        #4D 5A 00 00 50 14 B2 87 00 06 00 3A 00 03 2F DB 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('00 06 00 3A 00 03 2F DB'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_10b1_3(self):
        #1B 01 00 4D 07 47 08 FF 00 00 04 93 F7 CD 77 58 11 8D 00 B6 7C 1B E9 51 7F BF 2C 0D DD 58 F4 23 68 DC 8D 70 65 F3 64 62 12 C2 24 6B 2F 71 0C 9C 17 C2 1B 38 02 61 F6 63 C9 B2 BD DE 1B 5E 86 BA EE 7C DE AE 86 60 2D 72 13 F2 EA 1D 6B 8A 5A 07 98 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('1B 01 00 4D 07 47 08 FF 00 00 04 93 F7 CD 77 58 11 8D 00 B6 7C 1B E9 51 7F BF 2C 0D DD 58 F4 23 68 DC 8D 70 65 F3 64 62 12 C2 24 6B 2F 71 0C 9C 17 C2 1B 38 02 61 F6 63 C9 B2 BD DE 1B 5E 86 BA EE 7C DE AE 86 60 2D 72 13 F2 EA 1D 6B 8A 5A 07 98 '))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_heartbeatd(self):
        #4D 5A 00 00 50 14 C6 2E 00 0A 10 B2 50 14 C6 2E FF FF FF FF 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('10 B2'))
        write.integer(bootTime)
        write.byte(bytes.fromhex('FF FF FF FF'))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_10b1_4(self):
        #1B 01 00 44 07 1D 08 FF 00 00 04 0A A8 A9 19 53 0B 6E AF 67 BA 36 CE AB 9B 23 85 22 D1 8D FF DE C7 5D 6D 09 45 03 6E 32 1C 40 4D 0B 0F F0 1F 0D DB F2 39 AA 29 25 FD 21 20 25 5D 37 8D 25 AC 9B E3 D6 B4 38 68 9F 7D 3F 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('1B 01 00 44 07 1D 08 FF 00 00 04 0A A8 A9 19 53 0B 6E AF 67 BA 36 CE AB 9B 23 85 22 D1 8D FF DE C7 5D 6D 09 45 03 6E 32 1C 40 4D 0B 0F F0 1F 0D DB F2 39 AA 29 25 FD 21 20 25 5D 37 8D 25 AC 9B E3 D6 B4 38 68 9F 7D 3F '))
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def login_acc_10b2(self):
        #4D 5A 00 00 50 14 9D 97 00 06 10 B3 50 14 9D 97 
        write = WriteBuff()
        allWrite = WriteBuff()
        bootTime = self.get_bufftime()
        write.byte(bytes.fromhex('10 B3'))
        write.integer(bootTime)
        allWrite.byte(b'MZ\x00\x00')
        allWrite.integer(bootTime)
        allWrite.byte(write.getBuffer(),True,1)
        return allWrite.getBuffer()
    
    def GM_login(self):
        self.GMUSER.账号 = GM账号
        self.GMUSER.在线中 = True
        self.GMUSER.客户端启动(游戏IP,游戏端口[0])
        self.GMUSER.服务器句柄.send(self.login_acc())
        
    def GM_login_line(self):
        self.GMUSER.在线中 = True
        self.GMUSER.客户端启动(游戏IP,游戏端口[1])
        
        