from script.utils.utilsfile import utilsFile
from script.utils.utils import utils
import os
import time
from script.tts.alytts import alyTTSApi


def word_create():
    work_path = "D:/Workship/Pelbs/Gen/"

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
        if not cur_idx: cur_idx = 1
        for num, line in enumerate(file_content):
            if (len(line) == 0 or line == "\n"):
                continue
            if (num > 1) & (num > int(cur_idx)):
                time.sleep(1)
                words = line.split("\t")
                if(len(words) != 3):
                    print("【" + file + "】中的第" + str(num + 1) + "行的tab个数不对")
                    return
                sound_file = words[0]
                englishWord = words[1]
                unit_folder = sound_file.split("_")[0]
                # 生成语音
                sound_path = osd_sound_path + unit_folder + "/" + sound_file
                utils.mkdir(osd_sound_path + unit_folder)
                print("txt2audio", sound_path)
                alyTTSApi.tts(englishWord, sound_path)


if __name__ == '__main__':
    # 单词音频生成
    word_create()
