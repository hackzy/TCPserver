from setting import *
class 客户端:
    def __init__(self) -> None:
        self.未发送 = bytes()

    def 接收处理线程(self,cid):
        包头 = self.未发送[10:12]
        buffer = self.未发送
        #print(包头.hex())
        if 包头.hex() == "3357":
            buffer = self.登录线路(self.未发送)
            print(buffer.hex())
        if 包头.hex() == "4355":
            buffer = self.显示线路(self.未发送)
            print(buffer.hex())
        if len(buffer) != 0 :
            客户端组[cid].连接id.send(buffer)


    def 登录线路(self,buffer):
        '''4d5a000000000000003133570000000103e80c31302e3136382e312e313039177b77a4f34b15e58581e8a8b1e8a9b2e5b8b3e8999fe799bbe585a5'''
        封包 = buffer[0:18]
        封包 = 封包 + len(服务器监听地址).to_bytes(1) +  bytes(服务器监听地址,'UTF-8') + \
                            服务器监听端口[1].to_bytes(2)
        封包 = 封包 + buffer[33:]
        封包 = 组包包头 + len(封包).to_bytes(2) + 封包[10:] 
        return 封包
    
    def 显示线路(self,buffer):
        ''' 4D 5A 00 00 00 00 00 00 00 38 43 55 00 01 12 E6 9B B4 E9 91 84 E8 BC 9D E7 85 8C E4 B8 
        80 E7 B7 9A 0E 31 32 34 2E 32 32 30 2E 31 35 39 2E 36 36 0F 31 31 31 2E 31 37 33 2E 31 31 
        36 2E 31 33 33 00 02'''
        a = 1
        封包 = buffer[10:12] + a.to_bytes(2)+ buffer[14:15] + buffer[15:15+buffer[14:15][0]] + len(服务器监听地址).to_bytes(1) + \
                bytes(服务器监听地址,'UTF-8') + buffer[-2:]
        封包 = 组包包头 + len(封包).to_bytes(2) + 封包
        return 封包