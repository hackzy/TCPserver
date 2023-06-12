import socket
import setting
from threading import Thread as 线程
class Client:
    def __init__(self,sid) -> None:
        self.cid = 0
        self.客户IP = 0
        self.连接id = 0
        self.服务器数组id = sid
        self.客户端id = 0
        self.未发送 = bytes()
        self.未请求 = bytes()
    
    def 客户端启动(self,cid,ip,端口):
        self.客户端id = socket.socket()
        self.客户端id.connect((ip,端口))
        c1 = 线程(target=self.数据到达,args=(cid,))
        c1.setDaemon(True)
        c1.start()
        return cid
    
    def 数据到达(self,cid):
        while True:
            buffer = self.客户端id.recv(50000)
            print("客户端数据",buffer.hex())
            if cid != None:
                self.未发送 = buffer
                t = 线程(target=self.接收处理线程,args=(cid,))
                t.setDaemon(True)
                t.start()
                
            if len(buffer) == 0:
                self.客户端id.close()
                # 删除连接
                setting.客户端.remove(cid)
                print("服务器断开")
                break

    def 接收处理线程(self,cid):
        包头 = self.未发送[10:12]
        buffer = self.未发送
        print(包头.hex())
        if 包头.hex() == "3357":
            buffer = self.登录线路(self.未发送)
            print(buffer.hex())
        if 包头.hex() == "4355":
            buffer = self.显示线路(self.未发送)
            print(buffer.hex())
        setting.服务器[setting.客户端[cid].服务器数组id].服务器.send(buffer)


    def 登录线路(self,buffer):
        封包 = buffer[0:18]
        封包 = 封包 + len(setting.服务器监听地址).to_bytes(1) +  bytes(setting.服务器监听地址,'UTF-8') + \
                            setting.服务器监听端口[1].to_bytes(2)
        封包 = 封包 + buffer[30:]
        封包 = setting.组包包头 + len(封包).to_bytes(2) + 封包[10:] 
        return 封包
    
    def 显示线路(self,buffer):
        ''' 4D 5A 00 00 00 00 00 00 00 38 43 55 00 01 12 E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C E4 B8 
        80 E7 B7 9A 0E 31 32 34 2E 32 32 30 2E 31 35 39 2E 36 36 0F 31 31 31 2E 31 37 33 2E 31 31 
        36 2E 31 33 33 00 02'''
        a = 1
        封包 = buffer[10:12] + a.to_bytes(2)+ buffer[14:15] + buffer[15:15+buffer[14:15][0]] + len(setting.服务器监听地址).to_bytes(1) + \
                bytes(setting.服务器监听地址,'UTF-8') + buffer[-2:]
        封包 = setting.组包包头 + len(封包).to_bytes(2) + 封包
        return 封包