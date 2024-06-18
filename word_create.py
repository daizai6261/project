from script.utils.utilsfile import utilsFile
from script.utils.utils import utils
import os
import time
from script.tts.alytts import alyTTSApi
from script.base.configer import configer
import shutil
import re


def word_create():
    # work_path = "D:/Workship/Pelbs/Gen/"
    work_path = configer.run_param("PROJECT_PATH")
    # 单词输入路径
    word_file_path = work_path + "res/org/word_en_file/"
    # 语音输出路径
    word_audio_output_path = work_path + "dest/word_audio_output_path/"
    utils.mkdir(word_audio_output_path)

    files = os.listdir(word_file_path)

    for file in files:
        file_path = word_file_path + file
        tts_idx_path = work_path + "data/tts_idx.txt"
        fdata = open(tts_idx_path, "r+", encoding="utf-8")
        file_content = open(file_path, 'r', encoding="utf-8")
        cur_idx = fdata.readline()
        book_num = str(file.split("_")[1].split(".")[0])
        osd_sound_path = word_audio_output_path + "book" + book_num + "/osd_sound/"
        osd_configs_path = word_audio_output_path + "book" + book_num + "/osd_configs/"

        # 删除原音频
        utils.delete_folder(osd_sound_path)

        if not os.path.exists(osd_configs_path):
            # 如果目标路径不存在原文件夹的话就创建
            os.makedirs(osd_configs_path)
        if not utils.genPhonetics(file_path, osd_configs_path + file):
            return
        # shutil.copy(file_path, osd_configs_path)

        if not cur_idx: cur_idx = 1

        for num, line in enumerate(file_content):
            if len(line) == 0 or line == "\n":
                continue
            if (num > 1) & (num > int(cur_idx)):
                # time.sleep(1)
                words = line.split("\t")
                sound_file = words[0]
                englishWord = words[1]
                unit_folder = sound_file.split("_")[0]
                # 生成语音
                sound_path = osd_sound_path + unit_folder + "/" + sound_file
                utils.mkdir(osd_sound_path + unit_folder)
                print("txt2audio", sound_path)
                alyTTSApi.tts(englishWord, sound_path)


def word_valid():
    is_valid = True
    # work_path = "D:/Workship/Pelbs/Gen/"
    work_path = configer.run_param("PROJECT_PATH")
    # 单词输入路径
    word_file_path = work_path + "res/org/word_en_file/"

    files = os.listdir(word_file_path)
    # 单词出错路径
    error_output_path = work_path + "error/"
    error_word_output_path = error_output_path + "word/"
    if os.path.exists(error_word_output_path):
        utils.del_file(error_word_output_path)
    for file in files:
        file_path = word_file_path + file
        tts_idx_path = work_path + "data/tts_idx.txt"
        fdata = open(tts_idx_path, "r+", encoding="utf-8")
        file_content = open(file_path, 'r', encoding="utf-8")
        cur_idx = fdata.readline()
        book_num = str(file.split("_")[1].split(".")[0])

        if not cur_idx: cur_idx = 1
        msg = ""
        for num, line in enumerate(file_content):
            if len(line) == 0 or line == "\n":
                continue
            if (num > 1) & (num > int(cur_idx)):
                words = line.split("\t")
                if len(words) != 3:
                    is_valid = False
                    msg += "【" + file + "】中的第" + str(num + 1) + "行的tab个数不对\n"
                    print("【" + file + "】中的第" + str(num + 1) + "行的tab个数不对")
                    continue
                else:
                    for w in words[1].split(" "):
                        try:
                            res, n = re.subn(r"[^a-zA-Z’]+", "", w)
                            [UK_temp, US_temp] = utils.getPhonetic(res)
                        except:
                            msg += "检查【" + file + "】第" + str(num + 1) + "行单词拼写是否出错\n"
                            print("检查【" + file + "】第" + str(num + 1) + "行单词拼写是否出错")
                            is_valid = False
                            break
        if msg != "":
            if not os.path.exists(error_word_output_path):
                # 如果目标路径不存在原文件夹的话就创建
                os.makedirs(error_word_output_path)
            result_file = error_word_output_path + "book" + book_num + ".txt"
            with open(result_file, "w", encoding="utf-8") as f:
                f.write(msg)
    return is_valid


if __name__ == '__main__':
    # 单词音频生成
    if word_valid():
        word_create()
