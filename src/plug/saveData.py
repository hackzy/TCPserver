import json
import os
class 存档:
    
    def 存储账号信息(user):
        with open('./json/'+user.账号+'.json','r+',encoding='utf-8') as f:
            loaddata = dict(json.load(f))
            savedata = {'自动战斗':{'人物使用技能':user.fuzhu.自动战斗.人物使用技能,
                                '宠物使用技能':user.fuzhu.自动战斗.宠物使用技能,
                                '人物攻击位置':user.fuzhu.自动战斗.人物攻击位置,
                                '宠物攻击位置':user.fuzhu.自动战斗.宠物攻击位置,},
                        '录制保存':user.fuzhu.录制保存,
                        '所有角色':user.gamedata.所有角色
                        }
            loaddata.update(savedata)
            f.seek(0)
            json.dump(loaddata,f,ensure_ascii=False,indent=2)
            f.truncate()

    def saveAllData(users:dict):
        for user in users.values():
            存档.存储账号信息(user)

    def 读取存档信息(user):
        try:
            with open('./json/'+user.账号+'.json','r',encoding='utf-8') as f:
                savedata = json.load(f)
            user.fuzhu.自动战斗.人物使用技能 = savedata['自动战斗']['人物使用技能']
            user.fuzhu.自动战斗.宠物使用技能 = savedata['自动战斗']['宠物使用技能']
            user.fuzhu.自动战斗.人物攻击位置 = savedata['自动战斗']['人物攻击位置']
            user.fuzhu.自动战斗.宠物攻击位置 = savedata['自动战斗']['宠物攻击位置']
            user.gamedata.所有角色 = savedata['所有角色']
            user.fuzhu.录制保存 = savedata['录制保存']
            if len(user.fuzhu.录制保存) != 0:
                user.fuzhu.luzhi.封包 = list(user.fuzhu.录制保存.values())[0].copy() #列表赋值必须使用深拷贝
                
        except:
            return

    def getLimtSave(user):
        with open('./json/' + user.账号 + '.json','r',encoding='utf-8') as file:
            每日限制 = json.load(file)
        return 每日限制

    def setLimtSave(user,saveData):
        with open('./json/' + user.账号 + '.json','r+',encoding='utf-8') as file:
            loadData = dict(json.load(file))
            loadData.update(saveData)
            file.seek(0)
            json.dump(loadData,file,ensure_ascii=False,indent=2)
            file.truncate()

    def 每日数据刷新():
        data = {
            '每日限制':{
                '使用道具':{
                    '锦囊':5,
                    '超级天书':3,
                    '超级藏宝图':5,
                    '特级藏宝图':5
                    },
                '任务':{
                    '通天塔':1,
                    '神石抽奖':1,
                    '抓坐骑':3
                    }
            }
        }
        filesName = os.listdir('./json')
        for name in filesName:
            with open('./json/' + name,'r+',encoding='utf-8') as file:
                loadData = dict(json.load(file))
                loadData.update(data)
                file.seek(0)
                json.dump(loadData,file,ensure_ascii=False,indent=2)
                file.truncate()
        