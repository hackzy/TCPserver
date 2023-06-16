from recBuffer import 读封包
from threading import  Thread
class 客户请求处理:
    def __init__(self,server) -> None:
        self.server = server


    def 喊话(self,buffer):
        读 = 读封包()
        读.置数据(buffer)
        读.跳过(12)
        频道 = 读.读短整数型(True)
        读.跳过(5)
        内容 = 读.读文本型()
        内容 = 内容[8:]
        if 内容 == "LZKS":
            self.server.user.fuzhu.luzhi.录制开始()
            return
        if 内容 == 'LZTZ':
            self.server.user.fuzhu.luzhi.录制停止()
            return
        if 内容 == 'LZFSKS':
            self.server.user.fuzhu.luzhi.发送开始()
            return
        if 内容 == 'LZFSTZ':
            self.server.user.fuzhu.luzhi.发送停止()
            return
        if 内容.find('SZLZYS') != -1:
            self.server.user.fuzhu.luzhi.设置延时(内容)
            return
        if 内容 == 'LZFS':
            self.server.user.fuzhu.luzhi.单次发送()
            return
        
        return buffer