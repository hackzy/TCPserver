import ServerData
from reg import Reg
from rc4 import *
from dafeireg import Dafei

class RegData(ServerData.服务器数据处理):
    def __init__(self, server,ip) -> None:
        super().__init__(server)
        self.客户ip = ip
        self.server = server

    def 请求处理线程(self,user):
        # 接收数据
        try:
            while True:
                buffer = user.客户句柄.recv(500)  # 我们这里只做一个简单的服务端框架，不去做分包处理。所以每个数据包不要大于2048
                if len(buffer) > 500:
                    buffer = b''
                    self.server.写日志("客户数据过大")
                    self.server.删除客户(user)
                    return
                if buffer == b'':
                    self.server.删除客户(user)
                    return
                self.请求处理中心(buffer,user)
                
        except:
            self.server.删除客户(user)
            #del self.server.user[user.cid]
            return
        

    def 请求处理中心(self,buffer,user):
        reg = Reg(user,self.server)
        解密后的数据 = decrypt(b'Kzml',buffer)
        包头 = 解密后的数据[:2]
        if 包头 == 'lz':
            语句 = 'SELECT adb FROM linxz WHERE ip=\'%s\'' % (self.客户ip)
            cur = reg.mysql.cursor()
            cur.execute(语句)
            if len(cur.fetchall()) >= 5:
                buffer = encrypt(b'Fzml','你已被限制注册'.encode('gbk')) 
                cur.close()
            else:
                去包头 = 解密后的数据[2:]
                buffer = encrypt(b'Fzml',reg.accreg(去包头,self.客户ip).encode('gbk'))
                cur.close()

        if 包头 == 'lg':
            去包头 = 解密后的数据[2:]
            buffer = encrypt(b'Fzml',reg.passwdchange(去包头).encode('gbk'))

        
        if 包头 == 'ld':
            语句 = 'SELECT adb FROM linxz WHERE ip=\'%s\'' % (self.客户ip)
            cur = reg.mysql.cursor()
            cur.execute(语句)
            if len(cur.fetchall()) >= 5:
                buffer = encrypt(b'Fzml','你已被限制注册'.encode('gbk'))
                cur.close()
                return
            else:
                去包头 = 解密后的数据[2:].split('#o_o')
                dafeireg = Dafei(self.server)
                buffer = encrypt(b'Fzml',reg.accreg(去包头,self.客户ip) + dafeireg.大飞注册(去包头[0],去包头[4],去包头[3],'旧',去包头[5],'逍遙大飛').encode('gbk'))
                
                


        try:
            if buffer != b'':
                user.send(buffer)
        except:
            return