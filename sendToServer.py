from recBuffer import 读封包

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
        if 内容 == "123456789":
            return b'MZ'
        return buffer