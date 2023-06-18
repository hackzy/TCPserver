from bufferWrit import 写封包
from recBuffer import 读封包
from setting import *
class 基础功能:

    def 中心提示(self,内容):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('1fe5'))
        写.写文本型(内容,True,1,True)
        写.写整数型(0)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1,True)

        return 完整包.取数据()

    def 左下角提示(self,内容):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('2fff'))
        写.写整数型(0,True)
        写.写整数型(0,True)
        写.写文本型(内容,True)
        写.写字节集(bytes.fromhex('00 00 00\
                     00 00 00 12 E6 9B B4 E9\
                     91 84 E8 BC 9D E7 85 8C \
                    E4 B8 80 E7 B7 9A 00 01'\
                             .replace(" ","")))
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1,True)
        return 完整包.取数据()

    def NPC对话包(self,ID,形象ID,对话内容,名字):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('2037'))
        写.写整数型(ID,True)
        写.写整数型(形象ID,True)
        写.写字节集(b'\x00\x01')
        写.写文本型(对话内容,True,1,True)
        写.写整数型(0)
        写.写文本型(名字,True)
        写.写整数型(0)
        写.写字节型(b'\x00')
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1,True)
        return 完整包.取数据()
    
    def 战斗时间(self,buffer):
        读 = 读封包()
        写 = 写封包()
        读.置数据 (buffer)
        写.写字节集 (读.读字节集 (19))
        写.写字节型 (b'\x04')
        读.跳过 (1)
        写.写字节集 (读.剩余数据 ())
        return 写.取数据()