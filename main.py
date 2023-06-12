from setting import *
from ServerData import 服务器

server = []


if __name__== '__main__':
    '服务器启动'
    server = 服务器()
    for id in range(len(服务器监听端口)):
       服务器组.append(服务器())
       服务器组[id].初始化服务器(id,游戏IP,游戏端口[id],服务器监听端口[id])

    m = input("1")