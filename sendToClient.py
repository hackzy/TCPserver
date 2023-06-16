from recBuffer import 读封包
from bufferWrit import 写封包
from setting import *
class 客户接收处理:
    def __init__(self,server) -> None:
        self.server = server

    def 登录线路(self,buffer):
        #4d5a000000000000003433570000000103e80f3131312e3137332e3131362e313333177bebf42c6315e58581e8a8b1e8a9b2e5b8b3e8999fe799bbe585a5
        写 = 写封包()
        读 = 读封包()
        完整包 = 写封包()
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
        return 完整包.取数据()
    
    def 显示线路(self,buffer):
        #4D 5A 00 00 00 00 00 00 00 23 43 55 00 01 06 E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C E4 B8 80 E7 B7 9A 09 31 32 37 2E 30 2E 30 2E 31 00 02 
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
    '''        if 包头.hex() == 'fff5':
            self.客户接收处理.背包读取(buffer)
        if 包头.hex() == 'fff7':
            self.客户接收处理.人物属性读取(buffer)
        if 包头.hex() == '7feb':
            self.客户接收处理.技能读取(buffer)
        if 包头.hex() == 'fff9':
            self.客户接收处理.周围对象显示(buffer)'''
    def 背包读取(self):
        