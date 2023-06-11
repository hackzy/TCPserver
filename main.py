from servertest import Server
from threading import Thread as 线程
import setting
from Server import 服务器
import socketserver

class 初始化服务器:
    def __init__(self,serverid,游戏ip,游戏端口,监听端口) -> None:
        setting.服务器.append(服务器())
        setting.服务器[serverid].监听端口 = 监听端口
        setting.服务器[serverid].游戏IP = 游戏ip
        setting.服务器[serverid].游戏端口 = 游戏端口
        t = 线程(target=Server,args=(serverid,'127.0.0.1',监听端口))
        t.setDaemon(True)
        t.start()
        




i = []
if __name__== '__main__':
    '服务器启动'
    for id in range(len(setting.服务器监听端口)):
       i.append(初始化服务器(id,setting.游戏IP,setting.游戏端口[id],setting.服务器监听端口[id]))

    m = input("1")