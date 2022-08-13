from script.utils.utilsfile import utilsFile
from script.utils.utils import utils
import os
import time
from script.tts.alytts import alyTTSApi
from script.base.configer import configer
import shutil

def sentence_create():
    # work_path = "D:/Workship/Pelbs/Gen/"
    work_path = configer.run_param("PROJECT_PATH")
    # 单词输入路径
    word_file_path = work_path + "res/org/sentence_file/"
    # 语音输出路径
    word_audio_output_path = work_path + "dest/sentence_audio_output_path/"
    utils.mkdir(word_audio_output_path)

    files = os.listdir(word_file_path)

    # 错误输出路径
    error_output_path = work_path + "error/"
    error_sentence_output_path = error_output_path + "sentence/"
    # self.paths["error_word_output_path"] = error_output_path + "word/"
    # self.paths["error_book_output_path"] = error_output_path + "book/"
    if os.path.exists(error_sentence_output_path):
        utils.del_file(error_sentence_output_path)
    for file in files:
        file_path = word_file_path + file
        tts_idx_path = work_path + "data/tts_idx.txt"
        fdata = open(tts_idx_path, "r+", encoding="utf-8")
        file_content = open(file_path, 'r', encoding="utf-8")
        cur_idx = fdata.readline()
        book_name = file.split("_")[0].lower()
        book_num = str(file.split("_")[1].split(".")[0])
        osd_sound_path = word_audio_output_path + "book" + book_num + "/osd_sound/"
        osd_configs_path = word_audio_output_path + "book" + book_num + "/osd_configs/"

        # 删除原音频
        utils.delete_folder(osd_sound_path)

        if not os.path.exists(osd_configs_path):
            # 如果目标路径不存在原文件夹的话就创建
            os.makedirs(osd_configs_path)
        shutil.copy(file_path, osd_configs_path)
        if not cur_idx: cur_idx = 1
        msg = ""
        for num, line in enumerate(file_content):
            if (num > 1) & (num > int(cur_idx)):
                time.sleep(1)
                sentences = line.split("\t")
                if (len(sentences) != 3):
                    msg += "【" + file + "】中的第" + str(num + 1) + "行的tab个数不对\n"
                    print("【" + file + "】中的第" + str(num + 1) + "行的tab个数不对")
                    continue
                sound_file = line.split("\t")[0]
                first_sentence = line.split("\t")[1]
                second_sentence = line.split("\t")[2]
                unit_name = sound_file.split("_")[0]
                # 生成语音
                sound_path1 = osd_sound_path + unit_name + "/" + unit_name + "_" + book_name + "_audio1"
                sound_path2 = osd_sound_path + unit_name + "/" + unit_name + "_point_audio1"
                utils.mkdir(osd_sound_path + unit_name)
                print("txt2audio", sound_path1)
                print("txt2audio", sound_path2)
                alyTTSApi.tts(first_sentence, sound_path1)
                alyTTSApi.tts(second_sentence, sound_path2)
        if msg != "":
            if not os.path.exists(error_sentence_output_path):
                # 如果目标路径不存在原文件夹的话就创建
                os.makedirs(error_sentence_output_path)
            result_file = error_sentence_output_path + "book" + book_num + ".txt"
            with open(result_file, "w", encoding="utf-8") as f:
                f.write(msg)

if __name__ == '__main__':
    # 单词音频生成
    sentence_create()
