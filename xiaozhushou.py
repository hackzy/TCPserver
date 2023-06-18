
class XiaoZhuShou:
    def __init__(self,server) -> None:
        self.server = server
        self.小助手id = 5003
        self.对象id = 0

    def 助手_自动战斗(self,点击对话):
        if 点击对话 == '自動戰斗':
            if self.server.user.fuzhu.自动战斗.开关:
                战斗开关 = '【關閉】'
            else:
                战斗开关 = '【開啟】'
            对话 = '自動戰斗功能設置：\n#Y當前配置#n：人物：#G' + self.server\
                    .user.fuzhu.自动战斗.人物使用技能 + '#n     寵物：#G' + \
                    self.server.user.fuzhu.自动战斗.宠物使用技能 + '[自動戰斗'\
                    + 战斗开关 + '/戰斗開關]' + '[人物戰斗配置/人物戰斗配置][\
寵物戰斗配置/寵物戰斗配置]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.server.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'))
            return
        if 点击对话 == '戰斗開關':
            if self.server.user.fuzhu.自动战斗.开关:
                self.server.user.fuzhu.自动战斗.开关 = False
            else:
                self.server.user.fuzhu.自动战斗.开关 = True
            if self.server.user.fuzhu.自动战斗.开关:
                战斗开关 = '【關閉】'
            else:
                战斗开关 = '【開啟】'
            对话 = '自動戰斗功能設置：\n#Y當前配置#n：人物：#G' + self.server\
                    .user.fuzhu.自动战斗.人物使用技能 + '#n     寵物：#G' + \
                    self.server.user.fuzhu.自动战斗.宠物使用技能 + '[自動戰斗'\
                    + 战斗开关 + '/戰斗開關]' + '[人物戰斗配置/人物戰斗配置][\
寵物戰斗配置/寵物戰斗配置]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.server.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'))
            return
        if 点击对话 == '人物戰斗配置' or 点击对话 == '寵物戰斗配置':
            if 点击对话 == '寵物戰斗配置':
                临时对象 = '寵物'
                self.对象id = self.server.user.gamedata.参战宠物id
            else:
                临时对象 = '人物'
                self.对象id = self.server.user.gamedata.角色id
            对话 = 临时对象 + '戰斗配置：[使用技能/使用技能][普通攻擊/' \
            + '普通攻擊][防御/' + '防御]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.server.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'))
            return
        if 点击对话 == '使用技能':
            对话 = '請選擇技能：'
            try:
                skills = self.server.user.gamedata.技能[self.对象id].keys()
                for s in skills:
                    对话 = 对话 + '[' + s + '/' + s + ']'
                self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                        self.server.user.gamedata.角色id,\
                                        self.小助手id,对话,'逍遙小助手'))
                return
            except:
                self.server.服务器发送(self.server.基础功能.中心提示('宠物技能获取失败,重新参战宠物后重试!'))
        if self.server.user.gamedata.技能[self.对象id].get(点击对话) != None:
            if self.对象id == self.server.user.gamedata.角色id:
                self.server.user.fuzhu.自动战斗.人物使用技能 = 点击对话
            else:
                self.server.user.fuzhu.自动战斗.宠物使用技能 = 点击对话
            对话 = '請選擇自動攻擊位置：\n#Y（第一排6-10，第二排1-5）#n\
[1/1][2/2][3/3][4/4][5/5][6/6][7/7][8/8][9/9][10/10]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.server.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'))
            return
        if 点击对话 == '1' or 点击对话 == '2' or 点击对话 == '3' or \
            点击对话 == '4' or 点击对话 == '5' or 点击对话 == '6' \
             or 点击对话 == '7' or 点击对话 == '8' or 点击对话 == '9'\
              or 点击对话 == '10':
            if self.对象id == self.server.user.gamedata.角色id:
                self.server.user.fuzhu.自动战斗.人物攻击位置 = 点击对话
                对话 = '設置成功！當前人物技能：#G' + \
            self.server.user.fuzhu.自动战斗.人物使用技能 + '#n  攻擊位置：#Y'\
            + 点击对话 + '#n[返回/自動戰斗]'
            else:
                self.server.user.fuzhu.自动战斗.宠物攻击位置 = 点击对话
                对话 = '設置成功！當前寵物技能：#G' + \
            self.server.user.fuzhu.自动战斗.宠物使用技能 + '#n  攻擊位置：#Y'\
            + 点击对话 + '#n[返回/自動戰斗]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.server.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'))
            return
        if 点击对话 == '普通攻擊' or 点击对话 == '防御':
            if self.对象id == self.server.user.gamedata.角色id:
                self.server.user.fuzhu.自动战斗.人物使用技能 = 点击对话
                对话 = '設置成功！當前人物：#G' + self.server.user.fuzhu.自动战斗.人物使用技能\
                + '#n。[返回/自動戰斗]'
            else:
                self.server.user.fuzhu.自动战斗.宠物使用技能 = 点击对话
                对话 = '設置成功！當前寵物：#G' + self.server.user.fuzhu.自动战斗.宠物使用技能\
                + '#n。[返回/自動戰斗]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.server.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'))
            return
        
    def 小助手(self):
        对话 = '您好，歡迎來到獨家逍遙更鑄輝煌，我是逍遙小助手，請問有什么\
能幫到您：[自動戰斗/自動戰斗]'
        self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.server.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'))