from setting import *
from ServerData import 服务器数据处理
import datetime
class 逍遥插件:
    '''全局管理类，负责保存分配客户与服务端信息'''
    def __init__(self) -> None:
      self.server = []
      self.client = []
      
    def 分配空闲客户(self):
        '''分配客户id'''
        for i in range(len(self.client)):
            if self.client[i].使用中 == False:
                self.client[i].使用中 = True
                print("分配空闲客户",i)
                return i
        self.client[0].使用中 = True
        return 0
    
    def 写日志(self,msg):
        cur_time = datetime.datetime.now()
        s = "[" + str(cur_time) + "]" + msg
        print(s+"\n")




if __name__== '__main__':
    '服务器启动'
    server = 逍遥插件() #创建全局对象
    for id in range(len(服务器监听端口)):           #根据线路数量创建服务端，一个线路一个服务端
      server.server.append(服务器数据处理(server))  #创建服务器管理对象
      server.server[id].初始化服务器(id,游戏IP,游戏端口[id],服务器监听端口[id]) #初始化并创建服务端

    m = input()