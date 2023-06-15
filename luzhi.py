
import time
class Luzhi:
    def __init__(self,server) -> None:
        self.是否开启 = False
        self.封包 = []
        self.发送延时 = 500
        self.server = server
    def 录制封包(self,buffer):
        if len(self.封包) >= 30:
            self.server.服务器发送(self.server.基础功能\
                    .中心提醒("錄製操作超過上限！已自動停止!"))
            self.录制停止()
            return
        self.封包.append(buffer)

    def 录制开始(self):
        self.封包.clear()
        self.是否开启 = True
        return
    
    def 录制停止(self):
        self.是否开启 = False
        return
    
    def 发送开始(self):
        self.录制停止()
        if self.是否发送 == False:
            self.是否发送 = True
            self.发送线程()
        return
    
    def 发送停止(self):
        if self.是否发送:
            self.是否发送 = False
        return
    
    def 发送线程(self):
        while self.是否发送:
            for i in range(len(self.封包)):
                self.server.客户端发送(self.封包[i])
                time.sleep(self.发送延时/1000)

    def 单次发送(self):
        for i in range(len(self.封包)):
            self.server.客户端发送(self.封包[i])
            time.sleep(self.发送延时/1000)

    def 取录制数量(self):
        return len(self.封包)
