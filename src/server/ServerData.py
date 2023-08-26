
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
                self.server.tlock.acquire()
                user.未请求 += buffer
                self.server.tlock.release()
                self.处理数据(user)
                
        except:
            if user.账号 == GM账号:
                if self.server.GM.挂载:
                    user.客户句柄.close()
                    self.server.写日志('GM挂载成功！')
                    return
            self.server.删除客户(user)
            #del self.server.user[user.cid]
            return

    def 处理数据(self,user):
        """
        处理准备发给服务器的数据
        """
        self.server.tlock.acquire()
        while user.未请求[:2] == b'MZ':
            leng = int.from_bytes(user.未请求[8:10])
            if len(user.未请求) - 10 >= leng:
                buffer = user.未请求[:leng+10]
                user.未请求 = user.未请求[leng + 10:]
                self.server.sThreads.submit(self.请求处理中心,buffer,user)
                continue
            break
        self.server.tlock.release()
    def 请求处理中心(self,buffer,user:Client):
        包头 = buffer[10:12]
        htime = int.from_bytes(buffer[4:8])
        if user.账号 != GM账号 and 屏蔽辅助:
            if htime < user.time or (htime - user.time) > 11000 and user.time != 0 and user.账号 != GM账号:
                self.server.服务器发送(self.server.基础功能.中心提示('#Y检测到您使用了辅助程序，正在断开您的连接，请勿使用辅助程序！'),user)
                time.sleep(2)
                self.server.删除客户(user)
                return
        请求处理 = 客户请求处理(user,self.server)
        if user.fuzhu.luzhi.是否开启:
            if 包头.hex() != '20d2' and 包头.hex() != 'fd72' and 包头.hex() != '3ae4':
                user.fuzhu.luzhi.录制封包(buffer)
        
        if 包头.hex() == '3ae4':
            buffer = 请求处理.喊话(buffer)
        elif 包头.hex() == '215e' or 包头.hex() == '30ca' or 包头.hex() == '1042':
            请求处理.NPC对话点击处理(buffer)
        elif 包头.hex() == '1156':
            if buffer[-2:].hex() == '0133':
                user.fuzhu.小助手.小助手()
                buffer = b''
        elif 包头.hex() == '1060':
            请求处理.选择角色(buffer)
        elif 包头.hex() == '4124':
            if user.账号 == '':
                请求处理.取账号(buffer)
                存档.读取存档信息(user)
        elif 包头.hex() == '2162':
            buffer = 请求处理.心法处理(buffer)
        elif 包头.hex() == '215e' or 包头.hex() == '2314': #屏蔽非法使用GM指令
            if user.账号 != GM账号:
                buffer = b''
        elif 包头.hex() == '20d2':
            user.time = int.from_bytes(buffer[12:16])
            if self.server.GM.挂载 and user.账号 == GM账号:
                self.server.GM.tGMHeartbeatd()
                buffer = b''
        try:
            if buffer != b'':
                self.server.客户端发送(buffer,user)
        except:
            return
