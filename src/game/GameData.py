from src.game.itemData import 背包数据
from src.game.petData import petdata
class GameData:
    def __init__(self) -> None:
        self.所有角色 = {'0':{},'1':{},'2':{},'3':{}}
        self.角色名 = ''
        self.角色id = 0
        self.GID = 0
        self.当前气血 = 0
        self.当前法力 = 0
        self.最大气血 = 0
        self.最大法力 = 0
        self.技能 = {}
        self.形象id = 0
        self.等级 = 0
        self.物品数据 = {}
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
        self.pet = {}
        self.参战宠物id = 0
        self.商城数据 = {}
        self.当前地图 = [0,'']
        self.当前坐标 = [0,0]
        self.屏蔽垃圾 = True
        self.上一地图 = ''
        self.假人所有 = False
        self.假人擂台 = False
        self.假人商会 = False
        self.假人拍卖行 = False





