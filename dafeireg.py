from reg import Reg
import pymysql
from setting import *
import askCheckSum
import random
class Dafei(Reg):
    def __init__(self, server) -> None:
        super().__init__(server)
        try:
            self.dfmysql = pymysql.connect(host=数据库ip,password=数据库密码,user=数据库用户,database='ddb',charset='utf8')
        except:
            self.server.写日志('数据库连接失败')
        self.server = server
    def 大飞注册(self,account,性别,门派,新老,仙魔,名字):
        if 性别 == '男':
            性别 = '1'
        else:
            性别 = '2'
        if 新老 == '旧':
            新老 = '1'
        else:
            新老 = '2'
        if 仙魔 == '魔':
            仙魔 = '4'
        else:
            仙魔 = '3'
        if 门派 == '金':
            临时五系 = '1'
            临时门派 = '五龍山雲霄洞'
            临时师尊 = '元始天尊'
            临时回城 = 'jindun-shu'
        if 门派 == '木':
            临时五系 = '2'
            临时门派 = '終南山玉柱洞'
            临时师尊 = '准提道人'
            临时回城 = 'mudun-shu'
        if 门派 == '水':
            临时五系 = '3'
            临时门派 = '鳳凰山斗闕宮'
            临时师尊 = '西方教主'
            临时回城 = 'shuidun-shu'
        if 门派 == '火':
            临时五系 = '4'
            临时门派 = '乾元山金光洞'
            临时师尊 = '太上老君'
            临时回城 = 'huodun-shu'
        if 门派 == '土':
            临时五系 = '5'
            临时门派 = '骷髏山白骨洞'
            临时师尊 = '通天教主'
            临时回城 = 'tudun-shu'
        a = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n',\
            'o','p','q','r','s','t','u','v','w','x','y','z']
        名字 = 名字 + random.choice(a) + random.choice(a) + random.randint(16,255).to_bytes(1).hex()
        dfcur = self.dfmysql.cursor()
        dfcur.execute('set names latin1')
        curlen = dfcur.execute('SELECT * FROM ddb.gid_info')
        for i in range(curlen):
            data = dfcur.fetchone()
            gid = data[0] + 1
        大飞新增id = int.to_bytes(gid,8).hex().upper()
        gid添加 = 'insert into gid_info (gid,type,name,time,memo) values (\'%d\',\'%s\',\'%s\',\'%s\',\'%s\');'\
            %(gid,'user',名字,'20190000000000','')
        gid_info添加 = dfcur.execute(gid添加)
        if gid_info添加 != 1:
            self.server.写日志('gid_info添加失败')
        basic_char_info添加 = 'insert into basic_char_info (gid,name,polar,gender,tt_weibo_name,hide_tt_weibo,time) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');'\
            %(大飞新增id,名字,临时五系,性别,'','0','20190000000000')
        basic_char_info添加 = dfcur.execute(basic_char_info添加)
        if basic_char_info添加 != 1:
            self.server.写日志('basic_char_info添加失败')
        path = 'login'
        data_name = account
        branch = ''
        content = data_login.replace('[GID]',大飞新增id)
        checksum = askCheckSum.getCheckSum(path+data_name+branch+content)
        datalogin添加 = 'insert into data (path,name,branch,content,time,checksum,memo) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');'\
            %(path,data_name,branch,content,'20190000000000',checksum,'')
        datalogin添加 = dfcur.execute(datalogin添加)
        if datalogin添加 != 1:
            self.server.写日志('datalogin添加失败')
        临时道行 = str(3000 * 360)
        大飞data = 角色data.replace('[GID]',大飞新增id).replace('[等级]','139').replace('[名字]',名字).replace('[账号]',account)\
        .replace('[游戏币]','200000').replace('[代金券]','0').replace('[新老]',新老).replace('[男女]',性别).replace('[相性]',临时五系)\
        .replace('[道行]',临时道行).replace('[门派]',临时门派).replace('[师尊]',临时师尊).replace('[回城]',临时回城).replace('[称谓]','QQ:959683906')\
        .replace('[金元宝]','2000000000').replace('[仙魔]',仙魔)
        for iid in range(11):
            装备iid = '642D712E' + random.randint(18764998447377,281474976710655).to_bytes(6).hex().upper()
            大飞data = 大飞data.replace('装备iid',装备iid,1)
        path = 'user'
        data_name = 大飞新增id
        branch = ''
        content = 大飞data
        checksum = askCheckSum.getCheckSum(path+data_name+branch+content)
        content = 大飞data.replace('\\','\\\\')
        角色data一添加 = 'insert into data (path,name,branch,content,time,checksum,memo) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');'\
            %(path,data_name,branch,content,'20190000000000',checksum,'')
        角色data一添加 = dfcur.execute(角色data一添加)
        if 角色data一添加 != 1:
            self.server.写日志('角色data一添加失败')
        branch = 'achieve'
        content = 角色大飞二
        checksum = askCheckSum.getCheckSum(path+data_name+branch+content)
        角色data二添加 = 'insert into data (path,name,branch,content,time,checksum,memo) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');'\
            %(path,data_name,branch,content,'20190000000000',checksum,'')
        角色data二添加 = dfcur.execute(角色data二添加)
        if 角色data二添加 != 1:
            self.server.写日志('角色data二添加失败')

        宠物iid = '2F000CDF' + random.randint(18764998447377,281474976710655).to_bytes(6).hex().upper()
        branch = 'patch'
        content = 角色大飞三.replace('GID',大飞新增id).replace('宠物iid',宠物iid)
        checksum = askCheckSum.getCheckSum(path+data_name+branch+content)
        content = content.replace('\\','\\\\')
        角色data三添加 = 'insert into data (path,name,branch,content,time,checksum,memo) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');'\
            %(path,data_name,branch,content,'20190000000000',checksum,'')
        角色data三添加 = dfcur.execute(角色data三添加)
        if 角色data三添加 != 1:
            self.server.写日志('角色data三添加失败')
        branch = 'upgrade'
        content = 角色大飞四
        checksum = askCheckSum.getCheckSum(path+data_name+branch+content)
        角色data四添加 = 'insert into data (path,name,branch,content,time,checksum,memo) values (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\');'\
            %(path,data_name,branch,content,'20190000000000',checksum,'')
        角色data四添加 = dfcur.execute(角色data四添加)
        if 角色data四添加 != 1:
            self.server.写日志('角色data四添加失败')
        if gid_info添加 and basic_char_info添加 and datalogin添加 and 角色data一添加 and 角色data二添加 and\
        角色data三添加 and 角色data四添加 == 1:
            self.server.写日志('角色:%s 注册大飞成功!'%(名字))
            self.dfmysql.commit()
            return '角色:%s 注册大飞成功!'%(名字)
        else:
            self.dfmysql.close()
            return '注册大飞失败!请重试!'
        

