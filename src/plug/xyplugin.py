import datetime
import logging
import os
import time
import threading
import subprocess
from typing import Literal
from src.plug.basefuncs import 基础功能
from src.game.gm import GM
from setting import *
from src.server.server import Server
from src.regserver.regserver import Regserver
from src.game.bot import 假人管理
from src.plug.saveData import 存档
from src.client.client import Client
class 逍遥插件:
    '''全局管理类，负责保存分配客户与服务端信息'''
    def __init__(self) -> None:
        self.server = []
        self.sid = 0
        self.user = {}
        self.基础功能 = 基础功能()
        self.GM = GM(self,Client(self))
        self.测试 = 0
        self.regserver = None
        self.假人 = 假人管理()
        self.假人.启动假人(self,self.user)
        self.ips = []
        self.ip_connections = {}
        
    def 写日志(self, msg, level:Literal["info","error","warning","debug"] = "info", console:bool=True):
        cur_time = datetime.datetime.now()
        filename = str(cur_time.year) + "年" + str(cur_time.month) + '月' + str(cur_time.day) + '日'
        m = ''.join(msg)
        formatter = logging.Formatter(
            "[%(asctime)s] - [%(levelname)s] - %(message)s",
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logger = logging.getLogger(__name__)
        logger.setLevel(level = logging.INFO)
        file_handler = logging.FileHandler('./log/' + filename + '.log',encoding='utf-8')   #log.txt是文件的名字，可以任意修改
        console_handler = logging.StreamHandler()
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        if not logger.handlers:
            logger.addHandler(file_handler)
            if console:
                logger.addHandler(console_handler)
        if level == 'info':
            logger.info(m)
        elif level == 'error':
            logger.error(m)
        elif level == 'warning':
            logger.warning(m)
        elif level == 'debug':
            logger.debug(m)


    def 删除客户(self,user):
        try:
            if user.账号 == GM账号:
                if self.GM.挂载:
                    #user.客户句柄.close()
                    self.写日志('GM挂载成功!')
                    return
            elif user.在线中:
                user.在线中 = False
                self.ips.remove(user.客户IP)
                user.客户句柄.close()
                user.服务器句柄.close()
                user.shutdown()
                del self.user[user.cid]
                if user.gamedata.角色名 != '':
                    self.写日志('玩家: ' + user.gamedata.角色名 + ' 下线 Ip:' + user.客户IP + '  当前在线人数:' + str(len(self.user)))
                    存档.存储账号信息(user)
                    del user
            
        except:
            return

    def 分配空闲客户(self):
        for a in range(len(self.user)+1):
            if a not in self.user.keys():
                return a

    def 客户连接(self,client,ip,sid):
        if self.ips.count(ip) == 5:
            self.服务器发送(self.基础功能.中心提示('#R最多只能支持5個賬號同時在綫，您已超過限制！！'),client)
            client.close()
            return
        self.ips.append(ip)
        cid = self.分配空闲客户()
        self.user.update({cid:Client(self)})
        self.user[cid].初始化客户信息(client,ip,cid)  #保存客户属性
        self.user[cid].客户端启动(sid.游戏ip,sid.游戏端口) #客户连接，启动连接服务端
        if sid.游戏端口 == 游戏端口[0]:
                self.服务器发送(self.基础功能.中心提示('#Y歡迎來到更鑄輝煌\n#B游戲內打字請用打字工具\n#R本服內置輔助\n#G使用#Y玄幻術#n#G即可打開內置輔助功能\n'),self.user[cid])
        sid.开始接受请求(self.user[cid])           #服务器启动接受客户发来的数据


    def 服务器发送(self,buffer,user):
        try:
            if user.在线中:
                user.客户句柄.sendall(buffer)
        except:
            return

    def 客户端发送(self,buffer,user):
        try:
            if user.在线中:
                user.服务器句柄.sendall(buffer)
        except:
            return
        
    def 封包测试(self,buffer):
        try:
            if self.测试.在线中:
                self.测试.客户句柄.sendall(buffer)
        except:
            return
        
    def starServer(self):
        for sid in range(len(服务器监听端口)):
            #启动插件网关,根据线路数量创建服务端，一个线路一个服务端
            self.server.append(Server(self))  #创建服务器对象
            self.server[sid].启动服务器(游戏IP,游戏端口[sid],服务器监听地址,服务器监听端口[sid]) #初始化并创建服务端
        #启动注册网关
        self.regserver = Regserver(self)
        self.regserver.启动服务器(服务器监听地址,2877)
        
        threading.Thread(target=self.chack_gm_online,daemon=True).start()

    def chack_gm_online(self):
        while True:
            if not self.GM.GMUSER.在线中:
                self.GM.GM_login()
            time.sleep(3)
            
            
    
    def create_ip_blacklist_rule(self, rule_name, ip):
        command = [
            'netsh', 'advfirewall', 'firewall', 'add', 'rule',
            f'name={rule_name}',
            'dir=in',
            'action=block',
            f'remoteip={ip}',
            'enable=yes'
        ]
        subprocess.run(command, check=True)
        
    def get_existing_ips(self, rule_name):
        command = [
            'netsh', 'advfirewall', 'firewall', 'show', 'rule',
            f'name={rule_name}'
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if '远程 IP' in line:
                ip_list = line.split(':')[1].strip()
                return ip_list.split(',')
        return []
        
    def inset_blacklist(self,rule_name, ip_address):
        existing_ips = self.get_existing_ips(rule_name)
        if ip_address not in existing_ips:
            existing_ips.append(ip_address)
            new_ip_list = ','.join(existing_ips)
            command = [
                'netsh', 'advfirewall', 'firewall', 'set', 'rule',
                f'name={rule_name}',
                'new',
                f'remoteip={new_ip_list}'
            ]
            subprocess.run(command, check=True)
    
    
        
    def rule_exists(self, rule_name):
        command = [
            'netsh', 'advfirewall', 'firewall', 'show', 'rule',
            f'name={rule_name}'
        ]
        result = subprocess.run(command, capture_output=True, text=True)
        return '没有与指定标准相匹配的规则' not in result.stdout

    def ensure_rule_exists(self, rule_name, ip_address):
        if not self.rule_exists(rule_name):
            self.create_ip_blacklist_rule(rule_name,ip_address)
            return
        self.inset_blacklist(rule_name, ip_address)
        
    def is_allowed(self, ip):
        current_time = time.time()  # 获取当前时间戳
        if ip not in self.ip_connections:
            self.ip_connections[ip] = []

        # 移除超过5秒的时间戳
        new_connips = []
        for timestamp in self.ip_connections[ip]:
            if current_time - timestamp <= 60:  # 计算时间差
                new_connips.append(timestamp)
        self.ip_connections[ip] = new_connips

        # 检查剩余的时间戳数量
        if len(self.ip_connections[ip]) >= 3:
            return True

        # 记录新的连接时间戳
        self.ip_connections[ip].append(current_time)
        return False
    