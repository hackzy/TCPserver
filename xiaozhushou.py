from threading import Thread

class XiaoZhuShou:
    def __init__(self,server,user) -> None:
        self.server = server
        self.user = user
        self.小助手id = 5003
        self.对象id = 0

    def 助手处理中心(self,点击对话):
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
            npcid = 2
        elif 点击对话 == '裝備相關':
            对话 = '請選擇裝備功能:[一鍵鑒定/一鍵鑒定][裝備改造/裝備改造]'
            npcid = 3
        elif 点击对话 == '錄制指令查詢':
            对话 = '你好，以下是錄制相關指令：\n開始錄制：LZKS\n停止錄制：LZTZ\n開始發送：LZFSKS\n停止發送：LZFSTZ\n單次發送：LZFS\n設置發送延遲：SZLZYS 延時值'
            npcid = 10
        self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    npcid,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
    
    def 助手_自动战斗(self,点击对话):
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
                                    2,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
            return
        elif 点击对话 == '人物戰斗配置' or 点击对话 == '寵物戰斗配置':
            if 点击对话 == '寵物戰斗配置':
                临时对象 = '寵物'
                self.对象id = self.user.gamedata.参战宠物id
            else:
                临时对象 = '人物'
                self.对象id = self.user.gamedata.角色id
            对话 = 临时对象 + '戰斗配置：[使用技能/使用技能][普通攻擊/' \
            + '普通攻擊][防御/' + '防御]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    2,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
            return
        elif 点击对话 == '使用技能':
            对话 = '請選擇技能：'
            try:
                skills = self.user.gamedata.技能[self.对象id].keys()
                for s in skills:
                    if len(s) == 4:
                        对话 = 对话 + '[' + s + '/' + s + ']'
                self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                        2,\
                                        self.小助手id,对话,'逍遙小助手'),self.user)
                return
            except:
                self.server.服务器发送(self.server.基础功能.中心提示('寵物技能獲取失敗,重新參戰寵物后重試!'),self.user)
        
        elif 点击对话 == '1' or 点击对话 == '2' or 点击对话 == '3' or \
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
                                    10,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
            return
        elif 点击对话 == '普通攻擊' or 点击对话 == '防御':
            if self.对象id == self.user.gamedata.角色id:
                self.user.fuzhu.自动战斗.人物使用技能 = 点击对话
                对话 = '設置成功！當前人物：#G' + self.user.fuzhu.自动战斗.人物使用技能\
                + '#n。[返回/自動戰斗]'
            else:
                self.user.fuzhu.自动战斗.宠物使用技能 = 点击对话
                对话 = '設置成功！當前寵物：#G' + self.user.fuzhu.自动战斗.宠物使用技能\
                + '#n。[返回/自動戰斗]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    2,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
            return
        try:
            if 点击对话 in self.user.gamedata.技能[self.对象id].keys():
                if self.对象id == self.user.gamedata.角色id:
                    self.user.fuzhu.自动战斗.人物使用技能 = 点击对话
                else:
                    self.user.fuzhu.自动战斗.宠物使用技能 = 点击对话
                对话 = '請選擇自動攻擊位置：\n#Y（第一排6-10，第二排1-5）#n\
        [1/1][2/2][3/3][4/4][5/5][6/6][7/7][8/8][9/9][10/10]'
                self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                            2,\
                                            self.小助手id,对话,'逍遙小助手'),self.user)
                return
        except:
            return

    def 小助手(self):
        对话 = '您好，歡迎來到獨家逍遙更鑄輝煌，我是逍遙小助手，請問有什么\
能幫到您：[自動戰斗/自動戰斗][裝備相關/裝備相關][錄制指令查詢/錄制指令查詢]'
        self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    10,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
        
    def 装备相关(self,点击对话):
        if 点击对话 == '一鍵鑒定':
            对话 = '請選擇鑒定品質：[普通鑒定/普通鑒定][精緻鑒定/精緻鑒定][鑒定寶石/鑒定寶石]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    3,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
        elif 点击对话 == '普通鑒定' or 点击对话 == '精緻鑒定' or 点击对话 == '鑒定寶石':
            self.user.fuzhu.鉴定类型 = 点击对话
            self.user.fuzhu.一键鉴定()

        elif 点击对话 == '裝備改造':
            对话 = '請選擇改造的裝備類型：[改造武器/改造武器][改造防具/改造防具]'
            if self.user.fuzhu.开始改造:
                对话 += '[【停止改造】/停止改造]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    3,\
                                    self.小助手id,对话,'逍遙小助手'),self.user)
            
        elif 点击对话 == '改造武器' or 点击对话 == '改造防具':
            对话 = '請把需要改造的裝備放在#G包裹#Y第一格#n，\n然后點擊#G開始改造#n，\n如需要#R停止#n，請重新打開小助手點擊#G【停止改造】#n。[開始改造/開始改造]'
            self.user.fuzhu.改造类型 = 点击对话
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    3,\
                                    self.小助手id,
                                    对话,
                                    '逍遙小助手'),self.user)
            
        elif 点击对话 == '開始改造' or 点击对话 == '停止改造':
            if 点击对话 == '開始改造':
                self.user.fuzhu.开始改造 = True
                t = Thread(target=self.user.fuzhu.改造线程)
                t.daemon = True
                t.start()
                buffer = self.server.基础功能.中心提示('#Y開始改造中。。。') + self.server.基础功能.左下角提示('#Y開始改造中。。。')
            else:
                self.user.fuzhu.开始改造 = False
                buffer = self.server.基础功能.中心提示('#Y改造已停止!') + self.server.基础功能.左下角提示('#Y改造已停止!')
                self.user.fuzhu.改造类型 = ''
            self.server.服务器发送(buffer,self.user)