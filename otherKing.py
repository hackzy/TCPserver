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
    
    def 奖励_上升提示(self,数值,奖励类型):
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('3b04'))
        写.写文本型(奖励类型,True)
        写.写整数型(数值,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        return 完整包.取数据()
    
    def 系统邮件(self,内容):
        '''4D 5A 00 00 00 00 00 00 01 AF 3F FF 00 09 00 00 00 00 00
          01 6B E4 BD A0 E5 9C A8 E6 9B B4 E9 91 84 E8 BC 9D E7 85 
          8C E4 B8 80 E7 B7 9A E8 A8 82 E5 96 AE E8 99 9F E7 82 BA 
          23 52 32 33 30 36 32 32 30 30 33 31 35 38 30 30 31 23 6E 
          E7 9A 84 E5 85 83 E5 AF B6 E4 BA A4 E6 98 93 E4 B8 AD EF 
          BC 8C E5 94 AE E5 87 BA E4 BA 86 23 59 31 30 30 23 6E E5 
          80 8B E9 8A 80 E5 85 83 E5 AF B6 EF BC 8C E7 8D B2 E5 BE 
          97 E4 BA 86 23 47 39 39 30 2C 30 30 30 23 6E E6 96 87 E9 
          8C A2 23 6E EF BC 8C E7 9B AE E5 89 8D E8 A8 82 E5 96 AE 
          E5 89 A9 E9 A4 98 23 52 39 30 39 30 30 23 6E E5 85 83 E5 
          AF B6 E6 9C AA E5 94 AE E5 87 BA EF BC 8C E8 AB 8B E5 8E 
          BB E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C E4 B8 80 E7 B7 9A 
          E5 85 83 E5 AF B6 E4 BA A4 E6 98 93 E5 B8 B3 E6 88 B6 E6 
          9F A5 E6 94 B6 E7 8F BE E9 87 91 E3 80 82 E5 A6 82 E6 9E 
          9C E4 B8 8D E5 8F 8A E6 99 82 E5 8F 96 E5 87 BA E7 B3 BB 
          E7 B5 B1 E5 B0 87 E6 96 BC E7 AC AC E4 BA 8C E5 A4 A9 E8 
          B5 B7 EF BC 8C E9 96 8B E5 A7 8B E6 94 B6 E5 8F 96 E4 BF 
          9D E7 AE A1 E8 B2 BB E7 94 A8 E3 80 82 28 23 52 E5 85 83 
          E5 AF B6 E4 BA A4 E6 98 93 E5 B8 B3 E6 88 B6 E5 9C A8 E5 
          85 83 E5 AF B6 E4 BA A4 E6 98 93 E4 BB 8B E9 9D A2 E5 85 
          A7 23 6E 29 64 94 08 F4 00 00 12 E6 9B B4 E9 91 84 E8 BC 
          9D E7 85 8C E4 B8 80 E7 B7 9A 00 03 00 00 01 6B 0F E5 A5 
          A7 E6 96 AF E5 8D A1 E8 B3 AD E7 A5 9E 00 00 00 00 00 00 00 00 00 00 '''
        写 = 写封包()
        完整包 = 写封包()
        写.写字节集(bytes.fromhex('3fff'))
        写.写短整数型(9,True)
        写.写整数型(0,True)
        写.写短整数型(1,True)
        写.写文本型(内容,True)
        写.写整数型(1687423220,True)
        写.写短整数型(0,True)
        写.写文本型('更鑄輝煌一線',True)
        写.写短整数型(3,True)
        写.写整数型(363,True)
        写.写文本型('奧斯卡賭神',True)
        写.写整数型(0,True)
        写.写整数型(0,True)
        写.写短整数型(0,True)
        完整包.写字节集(组包包头)
        完整包.写字节集(写.取数据(),True,1)
        return 完整包.取数据()


