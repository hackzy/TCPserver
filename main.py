from setting import *
from ServerData import 服务器




s = []
if __name__== '__main__':
    '服务器启动'
    for id in range(len(服务器监听端口)):
       s.append(服务器())
       s[id].初始化服务器(id,游戏IP,游戏端口[id],服务器监听端口[id])

    m = input("1")