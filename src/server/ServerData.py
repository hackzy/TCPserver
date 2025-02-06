
from threading import Thread as 线程
from setting import *
from .sendToServer import 客户请求处理
from src.plug.saveData import 存档
import time
class 服务器数据处理:
    from src.client.client import Client
    def __init__(self,server) -> None:
        self.server = server
                
    def 请求处理线程(self,user):
        # 接收数据
        try:
            while True:
                buffer = user.客户句柄.recv(500)  # 
                if len(buffer) > 500:
                    buffer = b''
                    self.server.写日志("客户数据过大")
                    self.server.删除客户(user)
                    return
                if buffer == b'':
                    self.server.删除客户(user)
                    return
                user.未请求 += buffer
                self.处理数据(user)
                
        except:
            self.server.删除客户(user)
            #del self.server.user[user.cid]
            return

    def 处理数据(self,user):
        """
        处理准备发给服务器的数据
        """
        while user.未请求[:2] == b'MZ':
            leng = int.from_bytes(user.未请求[8:10])
            if len(user.未请求) - 10 >= leng:
                buffer = user.未请求[:leng+10]
                user.未请求 = user.未请求[leng + 10:]
                请求处理线程 = 线程(target=self.请求处理中心,args=(buffer,user))
                请求处理线程.daemon = True
                请求处理线程.start()
                continue
            break

    def 请求处理中心(self,buffer,user:Client):
        包头 = buffer[10:12]
        htime = int.from_bytes(buffer[4:8])
        if user.账号 != GM账号 and 屏蔽辅助:
            if htime < user.time or (htime - user.time) > 11000 and user.time != 0 and user.账号 != GM账号:
                self.server.服务器发送(self.server.基础功能.中心提示('#Y檢測到您使用了輔助程序，正在斷開您的鏈接，請勿使用輔助程序！'),user)
                time.sleep(2)
                self.server.删除客户(user)
                return
        请求处理 = 客户请求处理(user,self.server)
        if user.fuzhu.luzhi.是否开启:
            if 包头.hex() != '10b2' and 包头.hex() != 'f0c2'\
                                    and 包头.hex() != '4062':
                user.fuzhu.luzhi.录制封包(buffer)
        if 包头.hex() == '4062':
            buffer = 请求处理.喊话(buffer)
        elif 包头.hex() == '3038':
            请求处理.NPC对话点击处理(buffer)
        elif 包头.hex() == '2032':
            if buffer[-2:].hex() == '0133':
                user.fuzhu.小助手.小助手()
                buffer = b''
        elif 包头.hex() == '3002':
            if user.账号 == '':
                请求处理.取账号(buffer)
                存档.读取存档信息(user)
        elif 包头.hex() == '10b2' : 
            user.time = int.from_bytes(buffer[12:16])
            if self.server.GM.挂载 and self.server.GM.sHeartbeatd != '' and user.账号 == GM账号:
                self.server.GM.tGMHeartbeatd()
                buffer = b''
        try:
            if buffer != b'':
                self.server.客户端发送(buffer,user)
        except:
            return
