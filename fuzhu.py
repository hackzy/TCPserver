from luzhi import Luzhi
from autoFired import 自动战斗
from xiaozhushou import XiaoZhuShou
class fuzhu:
    def __init__(self,server) -> None:
        self.luzhi = Luzhi(server)
        self.自动战斗 = 自动战斗(server)
        self.小助手 = XiaoZhuShou(server)

        