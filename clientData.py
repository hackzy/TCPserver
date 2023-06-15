from setting import *
from threading import Thread as 线程
from sendToClient import 客户接收处理
class 客户端数据处理:
    '''客户端数据处理类，负责处理服务器发来的数据'''
    def __init__(self,server) -> None:
        self.未发送 = bytes()
        self.server = server
        self.客户接收处理 = 客户接收处理(server)
    def 接收处理线程(self,user):
        while self.未发送[:2] == b'MZ':
            leng = int.from_bytes(self.未发送[8:10])
            if len(self.未发送) - 10 >= leng:
                buffer = self.未发送[:leng+10]
                self.未发送 = self.未发送[leng + 10:]
                请求处理线程 = 线程(target=self.接收处理中心,args=(buffer,user))
                请求处理线程.daemon = True
                请求处理线程.start()
                continue
            break

    def 接收处理中心(self,buffer,user):
        包头 = buffer[10:12]
        if 包头.hex() == "3357":
            buffer = self.客户接收处理.登录线路(buffer)
        if 包头.hex() == "4355":
            buffer = self.客户接收处理.显示线路(buffer)
        if 包头.hex() == '20d7':
            buffer = self.客户接收处理.切换角色(buffer)
        
        
        
        
        
        
        if len(buffer) != 0 and getattr(user.客户句柄,'_closed') == False:
            user.客户句柄.send(buffer)
