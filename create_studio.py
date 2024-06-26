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
    """根据单个文件生成音频
    :param file: 文件路径
    :param out_put_path: 输出路径
    :return:
    """
    if os.path.exists(out_put_path):
        raise ValueError(f"输出目标文件夹{out_put_path}已存在，请检查")
    else:
        utils.mkdir(out_put_path)

    speaker_en = configer.program_param("CURRENT_SPEAKER_EN")
    long_text_speaker_en = configer.program_param("LONG_TEXT_SPEAKER_EN")

    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            line_contents = line.split("\t")
            file_name = line_contents[0]
            word_contents = line_contents[1]
            print(word_contents)
            altts_en = AlyTTS(speaker_en, long_text_speaker_en)
            altts_en.tts(word_contents, out_put_path + file_name)

def gen_explain_audio_from_file(file, out_put_file):
    """根据txt文件生成讲解音频
    :param file: 文件路径
    :param out_put_file: 输出文件
    :return:
    """
    if os.path.exists(out_put_file):
        raise ValueError(f"输出目标文件夹{out_put_file}已存在，请检查")
    else:
        utils.mkdir(out_put_file)


def gen_explain_audio_from_folder(folder, out_put_folder):
    """根据文件夹生成讲解音频
    :param folder: 文件夹路径
    :param out_put_folder: 输出文件夹
    :return:
    """
    if os.path.exists(out_put_folder):
        raise ValueError(f"输出目标文件夹{out_put_folder}已存在，请检查")
    else:
        utils.mkdir(out_put_folder)


def gen_explain_audio_from_folder_and_file(folder, file, out_put_folder):
    pass

if __name__ =='__main__':
    PROJECT_PATH = configer.run_param("PROJECT_PATH")
    VIDEO_PATH = PROJECT_PATH + "dest/video/"
    print('输出路径为：', VIDEO_PATH)
    create_audio(r"D:\Workship\Pelbs\Books\教材\小学英语\人教小学英语\PEP\book16\osd_configs\AllAudio_16.txt",
                 VIDEO_PATH)
