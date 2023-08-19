
import time
from threading import Thread
class Luzhi:
    
    #from client import Client
    #from xyplugin import 逍遥插件
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
                    .中心提示("录制操作超过上限！已自动停止!"),self.user)
            self.录制停止()
            return
        self.封包.append(buffer.hex())

    def 录制开始(self):
        if not self.是否开启:
            self.server.服务器发送(self.server.基础功能.中心提示("录制已开始!"),self.user)
            self.server.服务器发送(self.server.基础功能.左下角提示("#R录制已开始!"),self.user)
            self.封包.clear()
            self.是否开启 = True
            return
    
    def 录制停止(self):
        if self.是否开启:
            self.server.服务器发送(self.server.基础功能.中心提示("录制已停止!"),self.user)
            self.server.服务器发送(self.server.基础功能.左下角提示("#R录制已停止!#n录制了#Y" + str(len(self.封包)) + "#n个操作！"),self.user)
            self.是否开启 = False
            return
    
    def 发送开始(self):
        if len(self.封包) == 0:
            self.server.服务器发送(self.server.基础功能.中心提示("没有录制任何操作!请检查！"),self.user)
            return
        self.server.服务器发送(self.server.基础功能.中心提示("发送已开始!"),self.user)
        self.server.服务器发送(self.server.基础功能.左下角提示("#R发送已开始!"),self.user)
        self.录制停止()
        if self.是否发送 == False:
            self.是否发送 = True
            t = Thread(target=self.发送线程)
            t.daemon = True
            t.start()
        return
    
    def 发送停止(self):
        self.server.服务器发送(self.server.基础功能.中心提示("发送已停止!"),self.user)
        self.server.服务器发送(self.server.基础功能.左下角提示("#R发送已停止!"),self.user)
        if self.是否发送:
            self.是否发送 = False
        return
    
    def 发送线程(self):
        while self.是否发送:
            for i in range(len(self.封包)):
                self.server.客户端发送(bytes.fromhex(self.封包[i]),self.user)
                time.sleep(self.发送延时/1000)

    def 单次发送(self):
        if len(self.封包) == 0:
            self.server.服务器发送(self.server.基础功能.中心提示("没用录制任何操作!请检查！"),self.user)
            return
        self.server.服务器发送(self.server.基础功能.中心提示("单次发送!"),self.user)
        self.server.服务器发送(self.server.基础功能.左下角提示("#R已发送!"),self.user)
        for i in range(len(self.封包)):
            self.server.客户端发送(bytes.fromhex(self.封包[i]),self.user)
            time.sleep(self.发送延时/1000)

    def 取录制数量(self):
        return len(self.封包)

    def 设置延时(self,内容):
        try:
            if int(内容[7:]) <= 1000 and int(内容[7:]) >= 100:
                self.发送延时 = int(内容[7:])
                self.server.服务器发送(self.server.基础功能.中心提示(\
                    "设置延时成功，当前延时：" + 内容[7:]),self.user)
                self.server.服务器发送(self.server.基础功能.左下角提示(\
                    "#R设置延时成功，当前延时：#n" + 内容[7:]),self.user)
            else:
                self.server.服务器发送(self.server.基础功能.左下角提示(
                    "延时设置失败！设定范围：100-1000"),self.user)
        except:
            self.server.服务器发送(self.server.基础功能.左下角提示(
                    "延时设置失败！设定范围：100-1000"),self.user)
            
    def 保存录制(self,名称):
        if len(self.封包) == 0:
            return False
        self.user.fuzhu.录制保存.update({名称:self.封包})
        self.server.服务器发送(self.server.基础功能.中心提示("保存成功!"),self.user)
        self.server.服务器发送(self.server.基础功能.左下角提示("#G录制保存成功!当前存有录制:#Y%s#n"%(list(self.user.fuzhu.录制保存.keys()))),self.user)
        return True
    def 设置封包(self,名称):
        try:
            self.封包 = self.user.fuzhu.录制保存[名称]
            self.server.服务器发送(self.server.基础功能.中心提示("设置成功,当前录制:#G%s#n！"%(名称)),self.user)
            self.server.服务器发送(self.server.基础功能.左下角提示("设置成功,当前录制:#G%s#n！"%(名称)),self.user)
        except:
            self.server.服务器发送(self.server.基础功能.中心提示("设置失败,录制不存在！"),self.user)
            self.server.服务器发送(self.server.基础功能.左下角提示("#R设置失败,录制不存在！"),self.user)
    def 删除录制(self,名称):
        try:
            self.user.fuzhu.录制保存.pop(名称)
        except:
            pass