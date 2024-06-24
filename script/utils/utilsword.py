import re
from script.base.configer import configer
from string import punctuation


class UtilsWord():
    def __init__(self, ):

        error_word_list = [
            [" l ", " I "], ["l've", "I've"], ["I m ", "I'm "], ["Im ", "I'm "], ["Tm", "I'm"], ["lim ", "I'm"],
            ["l want", "I want"],
            [" l can", " I can"], [" lts ", " It's "],
            ["lt's", "It's"], ["isnt", "isn't"], ["Itis ", "It is "], [" ls ", " is "], [" ln ", " In "],
            ["Guessl", "Guess!"], ["friendl", "friend!"], ["Greatel", "Greate!"], ["ideal", "idea!"],
            ["Lookl", "look!"], ["lookl", "look!"],
            ["of ten", "often"], ["loften", "I often"], ["offcn", "often"],
            ["Wow", "wow"], ["furure", "future"], ["Dont", "Don't"], ["moming", "morning"], ["miming", " morning"],
            ["Idlike", "I'd like"], ["They re ", "They're "], ["gomg ", "going "], ["tomorow", "tomorrow"],
            ["treel", "tree!"], ["lt", "It"],
            [" oclock ", " o'clock "], [" alock ", " o'clock "], [" o'dock ", " o'clock "],
            [" fime", " time"],
            ["Lef's", " Let's"],
            ["TaIk", "Talk"],
            ["leamt", "learnt"],
            ["(v)", ""], ["(V)", ""],
        ]
        # self.error_word_list = configer.get_orc_error_list()
        self.error_word_list = error_word_list

    # 是否全部标点符号
    def is_all_punctuation(self, strs):
        is_all = True
        for _char in strs:
            contain = re.search(r"\W", _char)
            if not contain:
                is_all = False

        return is_all

    def is_number(self, strs):
        try:
            float(strs)
            return True
        except ValueError:
            pass
        try:
            import unicodedata
            unicodedata.numeric(strs)
            return True
        except (TypeError, ValueError):
            pass
        return False

    # 找到全部数字
    def find_all_num(self, strs):

        strs = strs.lstrip('0')
        num = re.findall(r"\d+\.?\d*", strs)
        if num:
            return int(num[0])
        else:
            return None

    # 找到全部英文
    def find_all_en(self, strs):
        en = re.sub(u"([^\u0041-\u007a])", "", strs)
        return en

    # 英文转阿拉伯数字
    def En2AlabNum(self, txt):

        ret1 = re.match(u"[PpD][\.\-][0-999]", txt)
        if ret1 or ret2: return ""
        return txt

    # 替换指定位置
    def multi_replace(self, str, p, c):
        new = []
        for s in str:
            new.append(s)
        for i in p:
            new[i] = c
        return ''.join(new)

    # 去除特定符号之间的
    def delete_between_symbol(self, txt, symbol):
        if txt.count(symbol) > 1:
            listPos = [i.start() for i in re.finditer(symbol, txt)]
            start = listPos[0]
            end = listPos[1]
            txt = txt[:start + 1] + "" + txt[end:]
            # print("delete _between _symbol",txt )
        return txt

    # 特定文字的不处理
    def filter_special_word(self, txt):

        ret1 = re.match(u"[PpD][\.\-][0-999]", txt)
        ret2 = re.match(u"[PpD][\.\-][I?][0-999]", txt)
        ret3 = re.match(u"[(\d{1,3})]", txt)

        if ret1 or ret2 or ret3:
            return ""
        return txt

    # 过滤下特殊符号
    def filter_special_symbol(self, txt):
        txt = txt.strip()
        txt = re.sub(u"([^{} \u0030-\u0039\u0041-\u005a\u0061-\u007a\×\÷])".format(punctuation), "", txt)
        return txt

    # 过滤下标点符号
    def filter_punctuation(self, txt):
        dicts = {i: '' for i in punctuation}
        punc_table = str.maketrans(dicts)
        new_txt = txt.translate(punc_table)
        return new_txt

    # 替换下容易识别错误文字，存在空格无法走配置
    def replace_error_word(self, txt):

        for item in self.error_word_list:
            # print("replace_error_word", item)
            txt = txt.replace(item[0], item[1])
        return txt

    # 过滤音标
    def filter_phonetic_symbol(self, txt):
        while txt.count('/') > 1:
            listPos = [i.start() for i in re.finditer('/', txt)]
            start = listPos[0]
            end = listPos[1]
            subtxt = txt[start: end + 1]
            txt = txt.replace(subtxt, " ")
        return txt

    ####################################中文#####################################################
    # 是否包含中文
    def is_contain_zh(self, strs):

        RE = re.compile(u'[\u4e00-\u9fa5]', re.UNICODE)
        match = re.search(RE, strs)
        if match is None:
            return False
        else:
            return True

    # 是否全部中文
    def is_all_zh(self, strs):
        for _char in strs:
            if not '\u4e00' <= _char <= '\u9fa5':
                return False
        return True

    # 找到全部中文
    def find_all_cn(self, strs):
        cn = re.sub(u"([^\u4e00-\u9fa5])", "", strs)
        return cn

    # 过滤中文
    def filter_cn(self, txt):
        for _char in txt:
            if not '\u4e00' <= _char <= '\u9fa5':
                txt.replace(_char, "")

    # 删除包含中文的文本
    def delete_contain_cn(self, txt):
        is_chinese = self.is_contain_zh(txt)
        if is_chinese:
            return ""
        return txt

    # 过滤包含中文的文字
    def split_en_cn(self, txt):
        en = ""
        cn = ""
        for _char in txt:
            if '\u4e00' <= _char <= '\u9fa5':
                cn = cn + _char
            else:
                en = en + _char
        return en, cn


utilsWord = UtilsWord()
