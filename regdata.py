from reg import Reg
from rc4 import *
from dafeireg import Dafei

class RegData():
    def __init__(self, server,ip) -> None:
        self.客户ip = ip
        self.server = server

    def 请求处理线程(self,user):
        # 接收数据
        try:
            while True:
                buffer = user.recv(500)  # 我们这里只做一个简单的服务端框架，不去做分包处理。所以每个数据包不要大于2048
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
            self.请求处理中心(buffer,user)
            #self.server.删除客户(user)
            #del self.server.user[user.cid]
            return
        

    def 请求处理中心(self,buffer,user):
        reg = Reg(self.server)
        try:
            解密后的数据 = decrypt(b'Kzml',buffer).decode('gb2312','ignore')
            包头 = 解密后的数据[:2]
            if 包头 == 'lz':
                语句 = 'SELECT * FROM linxz WHERE ip=\'%s\'' % (self.客户ip)
                cur = reg.mysql.cursor()
                if cur.execute(语句) >= 5:
                    buffer = encrypt(b'Fzml','你已被限制注册'.encode('gb2312','ignore')) 
                    cur.close()
                    return
                else:
                    去包头 = 解密后的数据[2:].split('#o_o')
                    buffer = encrypt(b'Fzml',reg.accreg(去包头,self.客户ip).encode('gb2312','ignore'))
                    cur.close()

            if 包头 == 'lg':
                去包头 = 解密后的数据[2:]
                buffer = encrypt(b'Fzml',reg.passwdchange(去包头).encode('gb2312','ignore'))

            
            if 包头 == 'ld':
                语句 = 'SELECT * FROM linxz WHERE ip=\'%s\'' % (self.客户ip)
                cur = reg.mysql.cursor()
                if cur.execute(语句) >= 5:
                    buffer = encrypt(b'Fzml','你已被限制注册'.encode('gb2312','ignore'))
                    cur.close()
                    return
                else:
                    去包头 = 解密后的数据[2:].split('#o_o')
                    dafeireg = Dafei(self.server)
                    buffer = encrypt(b'Fzml',reg.accreg(去包头,self.客户ip).encode('gb2312','ignore') + dafeireg.大飞注册(去包头[0],去包头[4],去包头[3],'旧',去包头[5],'逍遙大飛').encode('gb2312','ignore'))
        except:
            buffer = encrypt(b'Fzml','信息错误,请重试!'.encode('gb2312','ignore'))


        try:
            if buffer != b'':
                user.send(buffer)
        except:
            return