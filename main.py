from setting import *
from ServerData import 服务器

server = []


if __name__== '__main__':
    '服务器启动'
    for id in range(len(服务器监听端口)):
      server.append(服务器())
      print(server[id],id)
      server[id].初始化服务器(server[id],游戏IP,游戏端口[id],服务器监听端口[id])

    m = input("1")