from setting import *
from ServerData import 服务器
class 逍遥插件:
    def __init__(self) -> None:
      self.server = []
      self.client = []

    def 分配空闲客户(self):
        print("分配客户",len(self.client))
        for i in range(len(self.client)):
            if self.client[i].使用中 == False:
                self.client[i].使用中 = True
                print("分配空闲客户",i)
                return i
        return 0
    




if __name__== '__main__':
    '服务器启动'
    server = 逍遥插件()
    for id in range(len(服务器监听端口)):
      server.server.append(服务器(server))
      #print(server.server[id],id)
      server.server[id].初始化服务器(id,游戏IP,游戏端口[id],服务器监听端口[id])

    m = input("1")