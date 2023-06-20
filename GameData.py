from itemData import 背包数据
from petData import petdata
class GameData:
    def __init__(self) -> None:
        self.所有角色 = {'0':{},'1':{},'2':{},'3':{}}
        self.角色名 = ''
        self.角色id = 0
        self.GID = 0
        self.当前气血 = 0
        self.当前法力 = 0
        self.技能 = {}
        self.形象id = 0
        self.等级 = 0
        self.物品数据 = 背包数据()
        self.银元宝 = 0
        self.金元宝 = 0
        self.金币 = 0
        self.代金券 = 0
        self.道行 = 0
        self.潜能 = 0
        self.经验 = 0
        self.战绩 = 0
        self.血池 = 0
        self.灵池 = 0
        self.门派 = ''
        self.师尊 = ''
        self.五行 = ''
        self.pet = petdata()
        self.参战宠物id = 0
        




