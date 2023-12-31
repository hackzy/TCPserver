import json
class 存档:
    
    def 存储账号信息(user):
        
        savedata = {'自动战斗':{'人物使用技能':user.fuzhu.自动战斗.人物使用技能,
                            '宠物使用技能':user.fuzhu.自动战斗.宠物使用技能,
                            '人物攻击位置':user.fuzhu.自动战斗.人物攻击位置,
                            '宠物攻击位置':user.fuzhu.自动战斗.宠物攻击位置,},
                    '录制保存':user.fuzhu.录制保存,
                    '所有角色':user.gamedata.所有角色}

        with open('./json/'+user.账号+'.json','w',encoding='utf-8') as f:
            json.dump(savedata,f,ensure_ascii=False,indent=2)
            f.close()
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