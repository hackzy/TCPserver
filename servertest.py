import datetime
import socket
import traceback
import setting
from threading import Thread
from client import Client

class Server:
    """
    服务端主类
    """
    __user_cls = None

    @staticmethod
    def write_log(msg):
        cur_time = datetime.datetime.now()
        s = "[" + str(cur_time) + "]" + msg
        print(s)

    def __init__(self,sid,ip, port):
        self.connections = []  # 所有客户端连接
        self.使用中 = False
        self.write_log('服务器启动中，请稍候...')
        try:
            self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 监听者，用于接收新的socket连接
            self.listener.bind((ip, port))  # 绑定ip、端口
            self.listener.listen(5)  # 最大等待数
        except:
            self.write_log('服务器启动失败，请检查ip端口是否被占用。详细原因：\n' + traceback.format_exc())

        if self.__user_cls is None:
            self.write_log('服务器启动失败，未注册用户自定义类')
            return

        self.write_log('服务器启动成功：{}:{}'.format(ip,port))
        while True:
            client, 客户端IP = self.listener.accept()  # 阻塞，等待客户端连接
            setting.客户端.append(Client(sid))
            cid = self.分配空闲客户()
            setting.客户端[cid].客户IP = 客户端IP
            setting.客户端[cid].服务器数组id = sid
            setting.客户端[cid].cid = cid
            setting.客户端[cid].连接id = self.listener
            setting.客户端[cid].客户端启动(cid,setting.服务器[sid].游戏IP,setting.服务器[sid].游戏端口)
            print(setting.服务器[sid].游戏IP,setting.服务器[sid].游戏端口)
            user = self.__user_cls(client, self.connections,cid)
            self.connections.append(user)
            self.write_log('有新连接进入，当前连接数：{}'.format(len(self.connections)))


    def 分配空闲客户(self):
        
        for i in range(len(setting.客户端)):
            if self.使用中 == False:
                self.使用中 = True
                return i
        return 0
    


    @classmethod
    def register_cls(cls, sub_cls):
        """
        注册玩家的自定义类
        """
        if not issubclass(sub_cls, Connection):
            cls.write_log('注册用户自定义类失败，类型不匹配')
            return

        cls.__user_cls = sub_cls


class Connection:
    """
    连接类，每个socket连接都是一个connection
    """

    def __init__(self, socket, connections,cid):
        self.socket = socket
        self.connections = connections
        self.data_handler(cid)

    def data_handler(self,cid):
        # 给每个连接创建一个独立的线程进行管理
        thread = Thread(target=self.recv_data,args=(cid,))
        thread.setDaemon(True)
        thread.start()

    def recv_data(self,cid):
        # 接收数据
        try:
            while True:
                bytes = self.socket.recv(10000)  # 我们这里只做一个简单的服务端框架，不去做分包处理。所以每个数据包不要大于2048
                if len(bytes) == 0:
                    self.socket.close()
                    # 删除连接
                    print("客户断开")
                    self.connections.remove(self)
                    break
                # 处理数据
                self.deal_data(bytes,cid)
        except:
            self.connections.remove(self)
            Server.write_log('有用户接收数据异常，已强制下线，详细原因：\n' + traceback.format_exc())

    def deal_data(self, bytes,cid):
        """
        处理客户端的数据，需要子类实现
        """
        raise NotImplementedError


@Server.register_cls
class Player(Connection):
    """
    玩家类，我们的游戏中，每个连接都是一个Player对象
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.login_state = False  # 登录状态
        self.nickname = None  # 昵称
        self.x = None  # 人物在地图上的坐标
        self.y = None

    def deal_data(self, bytes,cid):
        """
        处理服务端发送的数据
        :param bytes:
        :return:
        """
        setting.客户端[cid].未请求 = setting.客户端[cid].未请求 + bytes
        setting.客户端[cid].客户端id.send(bytes)
        print('\n客户端消息：',bytes)


