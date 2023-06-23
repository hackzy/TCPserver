
import time
from threading import Thread
class Luzhi:
    def __init__(self,server,user) -> None:
        self.是否开启 = False
        self.封包 = []
        self.发送延时 = 500
        self.server = server
        self.user = user
        self.是否发送 = False
    def 录制封包(self,buffer):
        if len(self.封包) >= 30:
            self.server.服务器发送(self.server.基础功能\
                    .中心提醒("錄製操作超過上限！已自動停止!"),self.user)
            self.录制停止()
            return
        self.封包.append(buffer)

    def 录制开始(self):
        if not self.是否开启:
            self.server.服务器发送(self.server.基础功能.中心提示("錄製已開始!"),self.user)
            self.server.服务器发送(self.server.基础功能.左下角提示("#R錄製已開始!"),self.user)
            self.封包.clear()
            self.是否开启 = True
            return
    
    def 录制停止(self):
        if self.是否开启:
            self.server.服务器发送(self.server.基础功能.中心提示("錄製已停止!"),self.user)
            self.server.服务器发送(self.server.基础功能.左下角提示("#R錄製已停止!#n錄制了#Y" + str(len(self.封包)) + "#n個操作！"),self.user)
            self.是否开启 = False
            return
    
    def 发送开始(self):
        if len(self.封包) == 0:
            self.server.服务器发送(self.server.基础功能.中心提示("沒用錄製任何操作!請檢查！"),self.user)
            return
        self.server.服务器发送(self.server.基础功能.中心提示("發送已開始!"),self.user)
        self.server.服务器发送(self.server.基础功能.左下角提示("#R發送已開始!"),self.user)
        self.录制停止()
        if self.是否发送 == False:
            self.是否发送 = True
            t = Thread(target=self.发送线程)
            t.daemon = True
            t.start()
        return
    
    def 发送停止(self):
        self.server.服务器发送(self.server.基础功能.中心提示("發送已停止!"),self.user)
        self.server.服务器发送(self.server.基础功能.左下角提示("#R發送已停止!"),self.user)
        if self.是否发送:
            self.是否发送 = False
        return
    
    def 发送线程(self):
        while self.是否发送:
            for i in range(len(self.封包)):
                self.server.客户端发送(self.封包[i])
                time.sleep(self.发送延时/1000)

    def 单次发送(self):
        if len(self.封包) == 0:
            self.server.服务器发送(self.server.基础功能.中心提示("沒用錄製任何操作!請檢查！"),self.user)
            return
        self.server.服务器发送(self.server.基础功能.中心提示("單次發送!"),self.user)
        self.server.服务器发送(self.server.基础功能.左下角提示("#R已發送!"),self.user)
        for i in range(len(self.封包)):
            self.server.客户端发送(self.封包[i],self.user)
            time.sleep(self.发送延时/1000)

    def 取录制数量(self):
        return len(self.封包)

    def 设置延时(self,内容):
        try:
            if int(内容[7:]) <= 1000 and int(内容[7:]) >= 100:
                self.发送延时 = int(内容[7:])
                self.server.服务器发送(self.server.基础功能.中心提示(\
                    "設置延時成功，當前延時：" + 内容[7:]),self.user)
                self.server.服务器发送(self.server.基础功能.左下角提示(\
                    "#R設置延時成功，當前延時：#n" + 内容[7:]),self.user)
            else:
                self.server.服务器发送(self.server.基础功能.左下角提示(
                    "延時設置失敗！設定範圍：100-1000"),self.user)
        except:
            self.server.服务器发送(self.server.基础功能.左下角提示(
                    "延時設置失敗！設定範圍：100-1000"),self.user)