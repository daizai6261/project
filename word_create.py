from script.utils.utilsfile import utilsFile
from script.utils.utils import utils
from script.utils.WordUtil import wordUtil
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
                            msg += "检查【" +file + "】第" + str(num + 1) + "行单词拼写是否出错\n"
                            print("检查【" +file + "】第" + str(num + 1) + "行单词拼写是否出错")
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

def word_config_create():
    PROJECT_PATH = configer.run_param("PROJECT_PATH")
    wordUtil.findFiles("D:\Workship\Pelbs\Books\教材\小学英语")
    files = wordUtil.resFileList
    # 单词出错路径
    error_output_path = PROJECT_PATH + "error/"
    error_word_output_path = error_output_path + "word/"

    target_path = PROJECT_PATH + "dest/word_audio_output_path/" + "book" + "/osd_configs/"

    word_code_dict = utils.get_word_code(PROJECT_PATH + "dest/pic_word/result-小学英语.txt")

    if not os.path.exists(target_path):
        # 如果目标路径不存在原文件夹的话就创建
        os.makedirs(target_path)

    if os.path.exists(error_word_output_path):
        utils.del_file(error_word_output_path)
    wordslist_file = ""
    for file in files:
        file_path = file
        file_content = open(file_path, 'r', encoding="utf-8")
        book_num = str(file.split("_")[2].split(".")[0])
        book_file_name = file.split("\\")[-1]
        target_path = file.replace(book_file_name, "")

        file_data = ""
        count = 0
        msg = ""
        # 用于标识是否是wordList文件
        flag = 0
        for num, line in enumerate(file_content):
            if len(line) == 0 or line == "\n":
                count = count + 1
                continue
            if count < 2:
                if count == 0:
                    new_line = line[:-1] + "\t" + "美式音标\t" + "英式音标\t" + "图片编号\n"
                else:
                    new_line = line[:-1] + "\t" + "KkSymbol\t" + "IpaSymbol\t" + "PicCode\n"
            else:
                words = line.split("\t")
                if len(words) == 2 and "wordslist_" in words[1]:
                    flag = 1
                    wordslist_file += file + "\n"
                    print("【" + file + "】:是wordlist文件，不进行操作")
                    break
                if len(words) != 3:
                    msg += "【" + file + "】中的第" + str(num + 1) + "行的tab个数不对\n"
                    print("【" + file + "】中的第" + str(num + 1) + "行的tab个数不对")
                    line_contents = line.split("\t")
                    word = line_contents[1]
                    pic_code = "NoneCode"
                    if word_code_dict.get(word):
                        pic_code = word_code_dict.get(word)
                    new_line = line[: -1] + "\t" + pic_code + '\n'
                else:
                    line_contents = line.split("\t")
                    word = line_contents[1]
                    _words = word.split(" ")
                    US = ''
                    UK = ''
                    for w in _words:
                        try:
                            res, n = re.subn(r"[^a-zA-Z’]+", "", w)
                            [UK_temp, US_temp] = utils.getPhonetic(res)
                            UK += UK_temp + " "
                            US += US_temp + " "
                        except:
                            msg += "检查【" +file + "】第" + str(num + 1) + "行单词拼写是否出错\n"
                            print("检查【" +file + "】第" + str(num + 1) + "行单词拼写是否出错")
                            break
                    pic_code = "NoneCode"
                    if word_code_dict.get(word):
                        pic_code = word_code_dict.get(word)
                    new_line = line[: -1] + "\t" + US[:-1] + '\t' + UK[:-1] + '\t' + pic_code + '\n'
            file_data += new_line
            count += 1
        if msg != "" and flag == 0:
            if not os.path.exists(error_word_output_path):
                # 如果目标路径不存在原文件夹的话就创建
                os.makedirs(error_word_output_path)
            result_file = error_word_output_path + "book" + book_num + ".txt"
            with open(result_file, "w", encoding="utf-8") as f:
                f.write(msg)
        if flag == 0:
            file_data = file_data[: -1]

            with open(target_path + "s_" + book_file_name, "w", encoding="utf-8") as f:
                f.write(file_data)
            file_content.close()
            os.remove(file)
            shutil.copyfile(target_path + "s_" + book_file_name, file)
            os.remove(target_path + "s_" + book_file_name)
        elif flag == 1:
            if not os.path.exists(error_word_output_path):
                # 如果目标路径不存在原文件夹的话就创建
                os.makedirs(error_word_output_path)
            result_file = error_word_output_path + "wordListFiles.txt"
            with open(result_file, "w", encoding="utf-8") as f:
                f.write(wordslist_file)


if __name__ == '__main__':
    word_config_create()