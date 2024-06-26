import re
import json
import random
import hashlib
from urllib import parse
import http.client
import string
from script.base.configer import configer
from script.contentmgr import contentMgr
from script.utils.utilsword import utilsWord
# trans
from script.trans.bdtrans import bdTransApi
from script.trans.alytrans import alyTransApi
from script.trans.ydtrans import ydTransApi


class PelbsTrans:
    def __init__(self):

        self.fixed_list = [
            # 译林
            ["Cartoon time", "动画时间"], ["Culture time", "文化时间"], ["Fun time", "轻松一刻"],
            ["Checkout time", "检查时间"],
            ["Say and act", "朗读与扮演"], ["Ticking time", "评价时间"], ["Make and say", "做和说"],
            ["Pick and say", "选和说"],
            ["Let's chant", "一起唱诵"], ["Read,listen and chant", "阅读、聆听并唱"], ["Listen and tick", "聆听并勾选"],
            ["Letter time", "字母时间"],
            ["Rhyme time", "歌谣时间"], ["Read,listen and circle", "阅读、聆听并圈出答案"],
            ["Look and match", "看一看并匹配"], ["Let's check", "一起检查"],
            ["Look and find", "看一看并找出"], ["Look and tick ", "看一看并打钩"],
            ["Listen,circle and write ", "聆听、圈出答案并写下来"],
            ["Look and circle", "看一看并圈出答案"], ["Read and circle", "阅读并圈出答案"],
            ["Listen,circle and say", "聆听、圈出答案并说一说"],
            ["Read,circle and write ", "阅读、圈出答案并写下来"], ["Read,listen and tick", "阅读、聆听、并打钩"],
            ["Read and tick", "阅读和打钩"],
            ["Read,listen and number", "阅读,聆听并编号"], ["Ask,answer and write", "提问,聆听并写下来"],
            ["Let's surveye", "一起调查"],
            ["Look,choose and write", "看一看、选择并写下来"], ["Read and tick or cross", "阅读、聆听并写打钩或打叉"],
            ["Listen,repeat and circle", "聆听，复读指并圈出答案"], ["Listen,read and circle", "聆听，阅读并指出答案"],
            ["Listen,number and say", "聆听，编号并说"], ["Let's try", "一起尝试"], ["Match and say", "匹配和说"],
            ["Let's wrap it up", "让我们来总结吧"], ["Listen,tick and say", "聆听，勾选并说"],
            ["Look and talk", "看和说"],
            ["Listen,answer and write ", "聆听、回答并把答案写下来"], ["Listen,match and say", "听，匹配和说"],
            ["Number the pictures", "给图片编号"],
            ["Listen and tick or cross", "聆听并写打钩或打叉"],

            # 人教起点
            ["Let's talk", "一起说"], ["Let's learn", "一起学"], ["Let's write", "一起写"], ["Let's Spell", "一起拼写"],
            ["Let's read", "一起读"],
            ["Listen and number", "聆听并编号"], ["Let's Review", "一起复习"], ["Read and act", "阅读和扮演"],
            ["Look,listen and circle", "看一看、聆听并圈出答案"],
            ["Look,listen and tick", "看一看、聆听并勾选"], ["Listen,circle and write", "聆听、圈出答案并写下来"],
            ["listen and circle", "聆听并圈出答案"],
            ["Read,number and write", "阅读、编号并写下来"],

            ["Let's make", "一起做"], ["Let's role-play", "一起角色扮演"], ["Let's sing", "唱一唱"],
            ["Let's play", "一起玩"], ["Let's act", "一起演"], ["Listen, point and repeat", "聆听，指出答案并复读"],
            ["Look, write and say", "听，写，说"],
            ["Read and write", "读和写"],

            # 人教精通
            ["Just talk", "说一说"], ["Just practise", "练一练"], ["Just write", "写一写"], ["Just learn", "学一学"],
            ["Revision", "复习"], ["Let's think", "一起想"], ["Look and say", "看一看并说一说"], ["Let's do", "一起做"],
            ["Let's make and say", "一起做和说"], ["Cultural link", "文化联系"],
            ["Can you write them", "你能写它们吗？"], ["Fun Reading", "趣味阅读"], ["Look Them Up", "找一找"],

            # 通用
            ["Unit One", "第一单元"], ["Unit Two", "第二单元"], ["Unit Three", "第三单元"], ["Unit Four", "第四单元"],
            ["Unit Five", "第五单元"], ["Unit Six", "第六单元"],
            ["Unit Seven", "第七单元"], ["Unit Eight", "第八单元"], ["Recycle 1", "复习一"], ["Recycle 2", "复习二"],
            ["here you are", "给你"],
            ["Lesson", "课程"], ["Revision 1", "复习一"], ["Revision 2", "复习二"],

            # 人名
            ["cook", "厨师"],

        ]
        self.name_list = [
            ["陈洁", "陈杰", "陈捷", ],
            ["吴一凡", "吴一帆", ],
            ["佐姆", "变焦", "zoom", ],
            ["泽普", "zip", ],

        ]

    def trans(self, english_txt):
        chinese_txt = ""

        is_fixed, fixed_ret = self.fixed_trans(english_txt)
        if is_fixed:  # 固定翻译
            chineseResult = is_fixed, fixed_ret
        else:
            chineseResult = self.apiTrans(english_txt)

        if chineseResult[0]:
            chinese_txt = chineseResult[1]

        chinese_txt = self.name_fixed_trans(chinese_txt)
        return chinese_txt

    # 直接翻译
    def fixed_trans(self, englishTxt):

        englishTxt = englishTxt.strip(".")
        chinese = ""
        for word in self.fixed_list:

            engTxt = englishTxt.upper().replace(" ", "")
            wordTxt = word[0].upper().replace(" ", "")
            if engTxt == wordTxt:
                chinese = word[1]
                return True, chinese

        return False, englishTxt

    # 名字固定翻译,直接替换会影响翻译效果，采用翻译后替换
    def name_fixed_trans(self, englishTxt):

        englishTxt = englishTxt.strip(".")
        for words in self.name_list:
            for word in words:
                if word != words[0]:
                    englishTxt = englishTxt.lower().replace(word, words[0])
        return englishTxt

    # 单元名称
    def unit_name_fixed_trans(self, englishTxt):
        ret1 = re.match(u"[Unit][0-9]", englishTxt)
        # ret2 = re.match(u"[UNIT][\.\ ][OneTwoThree]", englishTxt)

        if ret1:
            unit_num = utilsWord.find_all_num(englishTxt)
            unit_raw_name = "第x单元"
            chinese = unit_raw_name.replace("x", str(unit_num))
            return True, chinese

        return False, englishTxt

    # api翻译
    def apiTrans(self, english_txt):

        current = configer.api_type("CURRENT_TRANS_API")
        # chineseResult =  bdTransApi.trans(english_txt)
        chineseResult = {False, ''}
        if current == "ALY":
            chineseResult = alyTransApi.trans(english_txt)
        elif current == "YD":
            chineseResult = ydTransApi.trans(english_txt)

        return chineseResult


pTrans = PelbsTrans()
