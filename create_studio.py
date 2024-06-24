#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2023-01-07 13:55
# @Author : lgh
# @File : create_studio.py
# @Software: PyCharm
import os.path

from script.base.configer import configer
from script.tts.alyttsV2 import AlyTTS
from script.utils.utils import utils


def create_audio(file, out_put_path):
    if os.path.exists(out_put_path):
        utils.delete_folder(out_put_path)
    utils.mkdir(out_put_path)

    speaker_en = configer.program_param("CURRENT_SPEAKER_EN")
    long_text_speaker_en = configer.program_param("LONG_TEXT_SPEAKER_EN")

    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line_contents = line.split("\t")
            file_name = line_contents[0]
            word_contents = line_contents[1]
            altts_en = AlyTTS(speaker_en, long_text_speaker_en)
            altts_en.tts(word_contents, out_put_path + file_name)


if __name__ == '__main__':
    PROJECT_PATH = configer.run_param("PROJECT_PATH")
    VIDEO_PATH = PROJECT_PATH + "dest/video/"
    create_audio("D:/software/WeChat/datas/WeChat Files/wxid_78zus7tutfn122/FileStorage/File/2023-01/单次音频.txt",
                 VIDEO_PATH)
