# 音频生成
import os
import re
import time


class ContentMgr:
    def __init__(self):
        self.cur_audio_path = ""

    def get_unit_type(self, strs):
        if re.match("wordslist", strs) or re.match("vocabulary", strs):
            return "WORD"
        elif re.match("expressions", strs):
            return "EXPRESSION"
        elif re.match("recycle", strs) or re.match("revision", strs) or re.match("review", strs):
            return "RECYCLE"
        elif re.match("unit", strs) or re.match("starter unit", strs) or re.match("module", strs) or re.match("project",
                                                                                                              strs) or re.match(
                "learning", strs) or re.match("alphabet", strs) or re.match("assessment1", strs) or re.match("bonus",
                                                                                                             strs) or re.match(
                "appendices", strs) or re.match("grammar", strs) or re.match("tapescripts", strs) or re.match(
                "pronunciation", strs) or re.match("notes", strs) or re.match("additional", strs) or re.match(
                "irregular verbs", strs) or re.match("supplementary", strs) or re.match("starterunit", strs):
            return "LESSON"
        else:
            return ""

    def get_english_format_type(self, strs):
        if re.match("WORD", strs) or re.match("EXPRESSION", strs):
            return "WORD_FORMAT"
        elif re.match("EXPRESSION", strs):
            return "EXPRESSION_FORMAT"
        else:
            return "LESSON_FORMAT"

    # 翻译类型
    def get_trans_type(self, strs):
        if re.match("WORD", strs) or re.match("EXPRESSION", strs):
            return "TRANS_SPLIT"
        else:
            return "TRANS_API"

    # 聚合类型
    def get_sort_type(self, strs):
        if re.match("WORD", strs) or re.match("EXPRESSION", strs):
            return "LEFT_RIGHT"
        else:
            return "TOP_BOTTOM"

    # 音频切割类型
    def get_audio_split_type(self, strs):
        if re.match("WORD", strs) or re.match("EXPRESSION", strs):
            return "NOT_SPLIT"
        else:
            return "SPLIT"

    # 是否包含unitxxx
    def is_unit_str(self, txt):

        ret1 = re.match(u"unit[0-99]", txt)
        ret2 = re.match(u"Unit", txt)

        ret3 = re.match("module", txt)

        if ret1 or ret2 or ret3:
            return True
        return False


contentMgr = ContentMgr()
