import pymysql
import hashlib
import datetime
from setting import *
class Reg:
    def __init__(self,server) -> None:
        self.server = server
        try:
            self.mysql = pymysql.connect(host=数据库ip,password=数据库密码,port=数据库端口,user=数据库用户,charset='latin1',database=adb库)
        except:
            self.server.写日志('数据库连接失败')
            return
        
    def accreg(self,账号密码,ip):
        if len(账号密码) < 3:
            return '缺少必要信息，请检查后重试！'
        cur = self.mysql.cursor()
        cur.execute('SELECT * FROM account WHERE account=\'%s\'' % (账号密码[0]))
        if len(cur.fetchall()) >= 1:
            return '账号已存在，请更换后重试！'
        cur.close()
        password = self.MD5(账号密码[1])
        password = self.MD5(账号密码[0] + password + '20070201')
        checksum = self.MD5(账号密码[0] + password + 注册权限.to_bytes(4).hex() + goldcoin.to_bytes(4).hex() + silvercoin.to_bytes(4).hex() + 'ABCDEF')
        insert = 'insert into account (account,password,gold_coin,silver_coin,checksum,privilege,blocked_time) values (\'%s\',\'%s\',\'%d\',\'%d\',\'%s\',\'%d\',\'\');'\
            %(账号密码[0],password,goldcoin,silvercoin,checksum,注册权限)
        cur = self.mysql.cursor()
        if cur.execute(insert) == 1:
            insert = 'insert into linxz (zh,mm,ip,sj,aqm) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');'\
            %(账号密码[0],账号密码[1],ip,str(datetime.datetime.now()),账号密码[2])
            cur.execute(insert)
            self.mysql.commit()
            self.mysql.close()
            return '注册成功！账号:%s 密码:%s'%(账号密码[0],账号密码[1])
        else:
            self.mysql = pymysql.connect(host='127.0.0.1',password='Chen1021',user='root',charset='utf8',database='adb')
            self.mysql.close()
            return '注册失败，请重试！'

    def passwdchange(self,账号密码):
        newacc = 账号密码.split('#o_o')
        if len(newacc) != 3:
            return '修改错误，请出入密码和安全码'
        语句 = 'SELECT * FROM linxz WHERE zh=\'%s\' and aqm=\'%s\''%(newacc[0],newacc[2])
        cur = self.mysql.cursor()
        cur.execute(语句)
        if len(cur.fetchall()) == 0:
            cur.close()
            self.mysql.close()
            return '修改错误，账号或安全码错误！'
        else:
            语句 = 'UPDATE linxz SET mm=\'%s\',zh=\'%s\' WHERE zh=\'%s\''%(newacc[1],newacc[0],newacc[0])
            cur.execute(语句)
            self.mysql.commit()
            self.mysql.close()
            return '密码修改成功！'

    def MD5(self,text):
        md5 = hashlib.md5()
        md5.update(text.encode())
        return md5.hexdigest().upper()

