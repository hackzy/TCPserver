from setting import *
from data import 数据池
from threading import Thread as 线程
from recBuffer import 读封包
from bufferWrit import 写封包
class 客户端数据处理:
    '''客户端数据处理类，负责处理服务器发来的数据'''
    def __init__(self,server) -> None:
        self.未发送 = bytes()
        self.server = server
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
            buffer = self.登录线路(buffer)
        if 包头.hex() == "4355":
            buffer = self.显示线路(buffer)
        if 包头.hex() == '20d7':
            buffer = self.切换角色(buffer)
        if len(buffer) != 0 and getattr(user.客户句柄,'_closed') == False:
            user.客户句柄.send(buffer)

    def 登录线路(self,buffer):
        #4d5a000000000000003433570000000103e80f3131312e3137332e3131362e313333177bebf42c6315e58581e8a8b1e8a9b2e5b8b3e8999fe799bbe585a5
        写 = 写封包()
        读 = 读封包()
        完整包 = 写封包()
        print(buffer.hex())
        读.置数据(buffer)
        读.跳过(10)
        写.写字节集(读.读字节集(8))
        写.写文本型(服务器监听地址,True)
        写.写短整数型(服务器监听端口[1],True)
        读.读文本型()
        读.读字节集(2)
        写.写字节集(读.剩余数据())
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        print("取数据",完整包.取数据().hex())
        return 完整包.取数据()
    
    def 显示线路(self,buffer):
        #4D 5A 00 00 00 00 00 00 00 23 43 55 00 01 06 E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C E4 B8 80 E7 B7 9A 09 31 32 37 2E 30 2E 30 2E 31 00 02 
        #4D 5A 00 00 00 00 00 00 00 29 43 55 00 01 12 E69BB4E99184E8BC9DE7858CE4B880E7B79A0F3131312E3137332E3131362E3133330002
        print(buffer.hex().upper())
        写 = 写封包()
        读 = 读封包()
        完整包 = 写封包()
        读.置数据(buffer)
        读.跳过(10)
        写.写字节集(读.读字节集(4))
        写.写文本型(读.读文本型(),True)
        写.写文本型(服务器监听地址,True)
        写.写短整数型(2,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        print(完整包.取数据().hex().upper())
        return 完整包.取数据()
    
    def 切换角色(self,buffer):
        读 = 读封包()
        写 = 写封包()
        完整包 = 写封包()
        读.置数据(buffer)
        读.跳过(10)
        写.写字节集(读.读字节集(4))
        data = 读.读文本型()
        stri = data.split(" ")
        data = 服务器监听地址 + ' ' + str(服务器监听端口[1]) + ' '
        for i in range(len(stri) - 2):
            data = data + stri[i + 2] + ' '
        data = data[:len(data) - 1]
        写.写文本型(data,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1,True)
        return 完整包.取数据()