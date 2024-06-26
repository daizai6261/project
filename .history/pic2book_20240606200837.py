import os
import shutil

import xlrd

from script.base.configer import configer
from script.orc.pelbsorc import pORC
from script.utils.utils import utils
from script.utils.utilsfile import utilsFile
from script.xlsxopt.xlsx2book import xlsx2Book
# from script.tts.pelbstts import pTTS
from script.tts.pelbsttsV2 import pTTS

from script.xlsxopt.pxlsx import pXlsx

# -------------------------------------------------main---------------------------------------------

'''


'''
# 绘本 474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495


# 341,
# data = xlrd.open_workbook("D:/Workship/Pelbs/Gen/data/课文配置.xlsx")
data = xlrd.open_workbook(configer.run_param("EXCEL_PATH"))
data_sheet1 = data.sheets()[0]
rows = data_sheet1.nrows
book_idxs = data_sheet1.col_values(0)[1:]
book_idx_list = list(map(int, book_idxs))  # 99999       73, 82
series = data_sheet1.col_values(5)[1:]
series_list = list(map(int, series))

book_names = data_sheet1.col_values(1)[1:]
book_name_list = list(map(str, book_names))

# 卡通化模型位置
# anime_checkPoint_dir = "D:/Workship/Pelbs/Gen/project/AnimeGAN/checkpoint/AnimeGAN_Hayao_lsgan_300_300_1_3_10"
anime_checkPoint_dir = configer.run_param("ANIMEGAN_CHECKPOINT_PATH")
work_path = configer.run_param("PROJECT_PATH")
error_output_path = work_path + "error/"
error_book_output_path = error_output_path + "book/"
if os.path.exists(error_book_output_path):
    utils.del_file(error_book_output_path)


def pic_to_excel(index, id_):
    # copy_org_dir()
    pORC.orc2xls(True)
    print("识别完毕")

    # 复制config、texture文件夹用来生成


def copy_org_dir():
    book_unit_file = utilsFile.get("book_unit_file")
    res_texture_path = utilsFile.get("res_texture_path")

    utils.delete_folder(res_texture_path)

    utils.mkdir(res_texture_path)
    # utils.copy_files(id_, book_unit_file)


def txt2audio():
    # if book_valid():
    #    print("配置文件错误")
    # else:
    # 合成音频
    pTTS.txt2audio()  # 音频生成
    # # # #合成图片
    # # # # #
    # anime_test_dir = utilsFile.get("res_texture_path")
    # anime_result_dir = utilsFile.get("dest_texture_path")
    # gen(anime_checkPoint_dir, anime_result_dir, anime_test_dir)
    #
    # # # 不进行风格迁移，直接拷贝图片
    # utils.copy_all_folder(anime_test_dir, anime_result_dir)


def book_valid():
    is_valid = True
    # # 修改后的EnglishAudio文件
    osd_audio_file = utilsFile.get("osd_en_audio_file")
    osd_book_unit_file = utilsFile.get("osd_book_unit_file")

    # # 判断tab是否出错
    is_valid_audio_file = utils.tab_valid(osd_audio_file, error_book_output_path, id_, 5, 5)
    is_valid_unit_file = utils.tab_valid(osd_book_unit_file, error_book_output_path, id_, 4, 4)
    if (is_valid_audio_file == False or is_valid_unit_file == False):
        is_valid = False
    return is_valid


# 创建目标文件夹
def clear_dest_folder():
    # 创建目标文件夹
    dest_config_path = utilsFile.get("dest_config_path")
    dest_all_sound_path = utilsFile.get("dest_all_sound_path")

    utils.recreate_folder(dest_config_path)
    utils.recreate_folder(dest_all_sound_path)


def copy_dest_folder():
    temp_sound_path = utilsFile.get("temp_sound_path")
    temp_audio_file = utilsFile.get("temp_audio_file")

    dest_en_audio_file = utilsFile.get("dest_en_audio_file")
    dest_all_sound_path = utilsFile.get("dest_all_sound_path")
    dest_all_audio_file = utilsFile.get("dest_all_audio_file")

    utils.copy_all_folder(temp_sound_path, dest_all_sound_path)

    dest_config_path = utilsFile.get("dest_config_path")
    utils.recreate_folder(dest_config_path)
    shutil.copy(temp_audio_file, dest_en_audio_file)
    os.rename(dest_en_audio_file, dest_all_audio_file)


if __name__ == '__main__':
    for index, bookIdx in enumerate(book_idx_list):
        utilsFile.set_book_idx(index, bookIdx)
        print("开始处理book", bookIdx)
        clear_dest_folder()

        ####### 图片转xls
        pORC.orc2xls(True)
        print("识别完毕")

        ####### xls转txt
        pXlsx.xls2txt(False, True)  # 第一个是否翻译
        print("位置转换完毕")

        ####### 翻译
        # pXlsx.xls2txt(True, True)  #第一个是否翻译
        print("翻译完毕")

        #########合并成最终文件夹
        copy_dest_folder()
        print("合并完毕")

        # #json转txt
        # pXlsx.json2txt()

        ####### txt合成音频
        # txt2audio()

        # 合成讲解音频

        # 合成单元导学音频

        print("合成完毕")
