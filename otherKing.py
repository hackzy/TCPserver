from bufferWrit import 写封包
from recBuffer import 读封包
from setting import *
class 基础功能:
    def __init__(self,server) -> None:
        self.server = server
    def 中心提醒(self,内容):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('1fe5'))
        写.写文本型(内容,True,1,True)
        写.写整数型(0,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据,True,1,True)
        return 完整包.取数据()

