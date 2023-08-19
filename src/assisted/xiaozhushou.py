from threading import Thread

class XiaoZhuShou:
    
    def __init__(self,server,user) -> None:
        self.server = server
        self.user = user
        self.小助手id = 5003
        self.对象id = 0

    def 助手处理中心(self,点击对话):
        if 点击对话 == '自动战斗':
            if self.user.fuzhu.自动战斗.开关:
                战斗开关 = '【关闭】'
            else:
                战斗开关 = '【开启】'
            对话 = '自动战斗功能设置：\n#Y当前配置#n：人物：#G' + self\
                    .user.fuzhu.自动战斗.人物使用技能 + '#n     宠物：#G' + \
                    self.user.fuzhu.自动战斗.宠物使用技能 + '[自动战斗'\
                    + 战斗开关 + '/战斗开关]' + '[人物战斗配置/人物战斗配置][\
宠物战斗配置/宠物战斗配置]'
            npcid = 2
        elif 点击对话 == '装备相关':
            对话 = '请选择装备功能:[一键鉴定/一键鉴定][装备改造/装备改造]'
            npcid = 3
        elif 点击对话 == '录制相关':
            对话 = '当前未选择任何已保存录制，'
            for key in self.user.fuzhu.录制保存:
                if self.user.fuzhu.录制保存[key] == self.user.fuzhu.luzhi.封包:
                    对话 = '当前选择录制：#G' + key + '\n'
                    break
            对话 = 对话 + '请选择录制功能：[保存录制/保存录制][选择录制/选择录制][删除录制/删除录制][查询已保存录制/查询已保存录制][录制指令查询/录制指令查询]'
            npcid = 4
        elif 点击对话 == '挖宝':
            if self.user.fuzhu.autoTreasure.flag:
                对话 = '自动挖宝已停止'
                self.user.fuzhu.autoTreasure.flag = False
            else:
                对话 = '确定要开始自动挖宝吗？如需停止请重新进入当前菜单：\n#G请使用腾云驾雾后点开始#n[开始/确定挖宝][取消/取消]'
            npcid = 5
        self.server.服务器发送(self.server.基础功能.NPC对话包(
                                    npcid,
                                    self.小助手id,对话,'逍遥小助手'),self.user)
    
    def 助手_自动战斗(self,点击对话):
        if 点击对话 == '战斗开关':
            if self.user.fuzhu.自动战斗.开关:
                self.user.fuzhu.自动战斗.开关 = False
            else:
                self.user.fuzhu.自动战斗.开关 = True
            if self.user.fuzhu.自动战斗.开关:
                战斗开关 = '【关闭】'
            else:
                战斗开关 = '【开启】'
            对话 = '自动战斗功能设置：\n#Y当前配置#n：人物：#G' + self\
                    .user.fuzhu.自动战斗.人物使用技能 + '#n     宠物：#G' + \
                    self.user.fuzhu.自动战斗.宠物使用技能 + '[自动战斗'\
                    + 战斗开关 + '/战斗开关]' + '[人物战斗配置/人物战斗配置][\
宠物战斗配置/宠物战斗配置]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    2,\
                                    self.小助手id,对话,'逍遥小助手'),self.user)
            return
        elif 点击对话 == '人物战斗配置' or 点击对话 == '宠物战斗配置':
            if 点击对话 == '宠物战斗配置':
                临时对象 = '宠物'
                self.对象id = self.user.gamedata.参战宠物id
            else:
                临时对象 = '人物'
                self.对象id = self.user.gamedata.角色id
            对话 = 临时对象 + '战斗配置：[使用技能/使用技能][普通攻击/' \
            + '普通攻击][防御/' + '防御]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    2,\
                                    self.小助手id,对话,'逍遥小助手'),self.user)
            return
        elif 点击对话 == '使用技能':
            对话 = '请选择技能：'
            try:
                skills = self.user.gamedata.技能[self.对象id].keys()
                for s in skills:
                    if len(s) == 4:
                        对话 = 对话 + '[' + s + '/' + s + ']'
                self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                        2,\
                                        self.小助手id,对话,'逍遥小助手'),self.user)
                return
            except:
                self.server.服务器发送(self.server.基础功能.中心提示('宠物技能获取失败,重新参战宠物后重试!'),self.user)
        
        elif 点击对话 == '1' or 点击对话 == '2' or 点击对话 == '3' or \
            点击对话 == '4' or 点击对话 == '5' or 点击对话 == '6' \
             or 点击对话 == '7' or 点击对话 == '8' or 点击对话 == '9'\
              or 点击对话 == '10':
            if self.对象id == self.user.gamedata.角色id:
                self.user.fuzhu.自动战斗.人物攻击位置 = 点击对话
                对话 = '设置成功！当前人物技能：#G' + \
            self.user.fuzhu.自动战斗.人物使用技能 + '#n  攻击位置：#Y'\
            + 点击对话 + '#n[返回/自动战斗]'
            else:
                self.user.fuzhu.自动战斗.宠物攻击位置 = 点击对话
                对话 = '设置成功！当前宠物技能：#G' + \
            self.user.fuzhu.自动战斗.宠物使用技能 + '#n  攻击位置：#Y'\
            + 点击对话 + '#n[返回/自动战斗]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    10,\
                                    self.小助手id,对话,'逍遥小助手'),self.user)
            return
        elif 点击对话 == '普通攻击' or 点击对话 == '防御':
            if self.对象id == self.user.gamedata.角色id:
                self.user.fuzhu.自动战斗.人物使用技能 = 点击对话
                对话 = '设置成功！当前人物：#G' + self.user.fuzhu.自动战斗.人物使用技能\
                + '#n。[返回/自动战斗]'
            else:
                self.user.fuzhu.自动战斗.宠物使用技能 = 点击对话
                对话 = '设置成功！当前宠物：#G' + self.user.fuzhu.自动战斗.宠物使用技能\
                + '#n。[返回/自动战斗]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    2,\
                                    self.小助手id,对话,'逍遥小助手'),self.user)
            return
        try:
            if 点击对话 in self.user.gamedata.技能[self.对象id].keys():
                if self.对象id == self.user.gamedata.角色id:
                    self.user.fuzhu.自动战斗.人物使用技能 = 点击对话
                else:
                    self.user.fuzhu.自动战斗.宠物使用技能 = 点击对话
                对话 = '请选择自动攻击位置：\n#Y（第一排6-10，第二排1-5）#n\
        [1/1][2/2][3/3][4/4][5/5][6/6][7/7][8/8][9/9][10/10]'
                self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                            2,\
                                            self.小助手id,对话,'逍遥小助手'),self.user)
                return
        except:
            return

    def 小助手(self):
        对话 = '您好，欢迎来到独家逍遥更铸辉煌，我是逍遥小助手，请问有什么\
能帮到您：[自动战斗/自动战斗][装备相关/装备相关][录制相关/录制相关][自动挖宝/挖宝]'
        self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    10,\
                                    self.小助手id,对话,'逍遥小助手'),self.user)
        
    def 装备相关(self,点击对话):
        if 点击对话 == '一键鉴定':
            对话 = '请选择鉴定品质：[普通鉴定/普通鉴定][精致鉴定/精致鉴定][鉴定宝石/鉴定宝石]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    3,\
                                    self.小助手id,对话,'逍遥小助手'),self.user)
        elif 点击对话 == '普通鉴定' or 点击对话 == '精致鉴定' or 点击对话 == '鉴定宝石':
            self.user.fuzhu.鉴定类型 = 点击对话
            self.user.fuzhu.一键鉴定()

        elif 点击对话 == '装备改造':
            对话 = '请选择改造的装备类型：[改造武器/改造武器][改造防具/改造防具]'
            if self.user.fuzhu.开始改造:
                对话 += '[【停止改造】/停止改造]'
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    3,\
                                    self.小助手id,对话,'逍遥小助手'),self.user)
            
        elif 点击对话 == '改造武器' or 点击对话 == '改造防具':
            对话 = '请把需要改造的装备放在#G包裹#Y第一格#n，\n然后点击#G开始改造#n，\n如需要#R停止#n，请重新打开小助手点击#G【停止改造】#n。[开始改造/开始改造]'
            self.user.fuzhu.改造类型 = 点击对话
            self.server.服务器发送(self.server.基础功能.NPC对话包(\
                                    3,\
                                    self.小助手id,
                                    对话,
                                    '逍遥小助手'),self.user)
            
        elif 点击对话 == '开始改造' or 点击对话 == '停止改造':
            if 点击对话 == '开始改造':
                self.user.fuzhu.开始改造 = True
                t = Thread(target=self.user.fuzhu.改造线程)
                t.daemon = True
                t.start()
                buffer = self.server.基础功能.中心提示('#Y开始改造中。。。') + self.server.基础功能.左下角提示('#Y开始改造中。。。')
            else:
                self.user.fuzhu.开始改造 = False
                buffer = self.server.基础功能.中心提示('#Y改造已停止!') + self.server.基础功能.左下角提示('#Y改造已停止!')
                self.user.fuzhu.改造类型 = ''
            self.server.服务器发送(buffer,self.user)

    def 录制相关(self,对话:str,填写内容 = ''):
        if 对话 == "保存录制":
            if len(self.user.fuzhu.luzhi.封包) != 0:
                self.server.服务器发送(self.server.基础功能.输入框(4,self.小助手id,'请输入保存的名字:','逍遥小助手'),self.user)
                return
            对话 = '当前未录制任何操作，请录制后再保存!'
        elif 对话 == '!请输入':
            self.user.fuzhu.luzhi.保存录制(填写内容)
            所有录制 = ''
            for bc in self.user.fuzhu.录制保存:
                所有录制 = '#Y' + bc + "\n" + 所有录制
            对话 = '录制保存成功!当前存有录制:\n%s'%(所有录制)
        elif 对话 == '录制指令查询':
            对话 = '在当前频道输入下列指令即可开启对应功能,录制相关指令：\n开始录制：LZKS\n停止录制：LZTZ\n开始发送：LZFSKS\n停止发送：LZFSTZ\n单次发送：LZFS\n设置发送延迟：SZLZYS 延时值'
        elif 对话 == '删除录制':
            所有录制 = ''
            for bc in self.user.fuzhu.录制保存:
                所有录制 = '[' + bc + '/' + bc + 'sc]' + 所有录制
            对话 = '要删除哪个录制：%s'%(所有录制)
        elif 对话.find('sc') != -1:
            if 对话[:-2] in self.user.fuzhu.录制保存:
                self.user.fuzhu.录制保存.pop(对话[:-2])
                所有录制 = ''
                for bc in self.user.fuzhu.录制保存:
                    所有录制 = '[' + bc + '/' + bc + ']' + 所有录制
                if 所有录制 == '[/]':
                    对话 = '删除成功！当前无任何已保存录制!'
                else:
                    对话 = '删除成功！当前存有录制：%s'%(所有录制)
        elif 对话 == '查询已保存录制':
            所有录制 = ''
            for bc in self.user.fuzhu.录制保存:
                所有录制 = '#G' + bc + '\n' + 所有录制
            if 所有录制 == '':
                对话 = '当前无任何已保存录制!'
            else:
                对话 = '当前存有录制：\n%s'%(所有录制)
        elif 对话 == '选择录制':
            所有录制 = ''
            for bc in self.user.fuzhu.录制保存:
                所有录制 = '[' + bc + '/' + bc + 'xz]' + 所有录制
            对话 = '要使用哪个录制：' + 所有录制
        elif 对话.find('xz') != -1:
            if 对话[:-2] in self.user.fuzhu.录制保存:
                self.user.fuzhu.luzhi.设置封包(对话[:-2])
                对话 = '设置成功当前选择录制：#G' + 对话[:-2]
        
        self.server.服务器发送(self.server.基础功能.NPC对话包(4,self.小助手id,对话,'逍遥小助手'),self.user)
        
    def 自动挖宝(self,对话):
        if 对话 == '确定挖宝':
            if self.user.fuzhu.autoTreasure.flag == False:
                self.user.fuzhu.autoTreasure.flag = True
                self.user.fuzhu.autoTreasure.startTreasure(self.user,self.server)
            else:
                self.user.fuzhu.autoTreasure.flag = False