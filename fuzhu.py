from luzhi import Luzhi
from autoFired import 自动战斗
from xiaozhushou import XiaoZhuShou
class fuzhu:
    def __init__(self,server,user) -> None:
        self.luzhi = Luzhi(server,user)
        self.自动战斗 = 自动战斗(server,user)
        self.小助手 = XiaoZhuShou(server,user)

        