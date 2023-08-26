from src.plug.xyplugin import 逍遥插件
if __name__== '__main__':
    '服务器启动'
    server = 逍遥插件() #创建全局对象
    server.starServer() #启动服务
    while True:
        #print(菜单.format(time.strftime("%H:%M:%S",time.gmtime(time.time()-startime)),len(server.user)))
        #threading.Event().wait(1)
        input()
