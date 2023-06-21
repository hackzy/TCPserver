
class XiaoZhuShou:
    def __init__(self,server,user) -> None:
        self.server = server
        self.user = user
        self.小助手id = 5003
        self.对象id = 0

    def 助手_自动战斗(self,点击对话):
        if 点击对话 == '自動戰斗':
            if self.user.fuzhu.自动战斗.开关:
                战斗开关 = '【關閉】'
            else:
                战斗开关 = '【開啟】'
            对话 = '自動戰斗功能設置：\n#Y當前配置#n：人物：#G' + self\
                    .user.fuzhu.自动战斗.人物使用技能 + '#n     寵物：#G' + \
                    self.user.fuzhu.自动战斗.宠物使用技能 + '[自動戰斗'\
                    + 战斗开关 + '/戰斗開關]' + '[人物戰斗配置/人物戰斗配置][\
寵物戰斗配置/寵物戰斗配置]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
            return
        if 点击对话 == '戰斗開關':
            if self.user.fuzhu.自动战斗.开关:
                self.user.fuzhu.自动战斗.开关 = False
            else:
                self.user.fuzhu.自动战斗.开关 = True
            if self.user.fuzhu.自动战斗.开关:
                战斗开关 = '【關閉】'
            else:
                战斗开关 = '【開啟】'
            对话 = '自動戰斗功能設置：\n#Y當前配置#n：人物：#G' + self\
                    .user.fuzhu.自动战斗.人物使用技能 + '#n     寵物：#G' + \
                    self.user.fuzhu.自动战斗.宠物使用技能 + '[自動戰斗'\
                    + 战斗开关 + '/戰斗開關]' + '[人物戰斗配置/人物戰斗配置][\
寵物戰斗配置/寵物戰斗配置]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
            return
        if 点击对话 == '人物戰斗配置' or 点击对话 == '寵物戰斗配置':
            if 点击对话 == '寵物戰斗配置':
                临时对象 = '寵物'
                self.对象id = self.user.gamedata.参战宠物id
            else:
                临时对象 = '人物'
                self.对象id = self.user.gamedata.角色id
            对话 = 临时对象 + '戰斗配置：[使用技能/使用技能][普通攻擊/' \
            + '普通攻擊][防御/' + '防御]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
            return
        if 点击对话 == '使用技能':
            对话 = '請選擇技能：'
            try:
                skills = self.user.gamedata.技能[self.对象id].keys()
                for s in skills:
                    if len(s) == 4:
                        对话 = 对话 + '[' + s + '/' + s + ']'
                self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                        self.user.gamedata.角色id,\
                                        self.小助手id,对话,'逍遙小助手'),self.user)
                return
            except:
                self.server.服务器发送(self.server.基础功能.中心提示('寵物技能獲取失敗,重新參戰寵物后重試!'),self.user)
        
        if 点击对话 == '1' or 点击对话 == '2' or 点击对话 == '3' or \
            点击对话 == '4' or 点击对话 == '5' or 点击对话 == '6' \
             or 点击对话 == '7' or 点击对话 == '8' or 点击对话 == '9'\
              or 点击对话 == '10':
            if self.对象id == self.user.gamedata.角色id:
                self.user.fuzhu.自动战斗.人物攻击位置 = 点击对话
                对话 = '設置成功！當前人物技能：#G' + \
            self.user.fuzhu.自动战斗.人物使用技能 + '#n  攻擊位置：#Y'\
            + 点击对话 + '#n[返回/自動戰斗]'
            else:
                self.user.fuzhu.自动战斗.宠物攻击位置 = 点击对话
                对话 = '設置成功！當前寵物技能：#G' + \
            self.user.fuzhu.自动战斗.宠物使用技能 + '#n  攻擊位置：#Y'\
            + 点击对话 + '#n[返回/自動戰斗]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
            return
        if 点击对话 == '普通攻擊' or 点击对话 == '防御':
            if self.对象id == self.user.gamedata.角色id:
                self.user.fuzhu.自动战斗.人物使用技能 = 点击对话
                对话 = '設置成功！當前人物：#G' + self.user.fuzhu.自动战斗.人物使用技能\
                + '#n。[返回/自動戰斗]'
            else:
                self.user.fuzhu.自动战斗.宠物使用技能 = 点击对话
                对话 = '設置成功！當前寵物：#G' + self.user.fuzhu.自动战斗.宠物使用技能\
                + '#n。[返回/自動戰斗]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
            return
        for a in range(len(self.user.gamedata.技能)):
            if 点击对话 in self.user.gamedata.技能[a]:
                if self.对象id == self.user.gamedata.角色id:
                    self.user.fuzhu.自动战斗.人物使用技能 = 点击对话
                else:
                    self.user.fuzhu.自动战斗.宠物使用技能 = 点击对话
                对话 = '請選擇自動攻擊位置：\n#Y（第一排6-10，第二排1-5）#n\
    [1/1][2/2][3/3][4/4][5/5][6/6][7/7][8/8][9/9][10/10]'
                self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                        self.user.gamedata.角色id,\
                                        self.小助手id,对话,'逍遙小助手'),self.user)
                return
    def 小助手(self):
        对话 = '您好，歡迎來到獨家逍遙更鑄輝煌，我是逍遙小助手，請問有什么\
能幫到您：[自動戰斗/自動戰斗]'
        self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    self.user.gamedata.角色id,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)