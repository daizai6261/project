from script.utils.utils import utils
from script.utils.utilsword import utilsWord
from script.utils.utilsfile import utilsFile
from script.piccompress.piccompress import picCompress
from script.contentmgr import contentMgr
from script.tts.pelbstts import pTTS
from script.base.configer import configer
from script.tts.alytts import alyTTSApi
from script.base.filefinder import pFFinder
# from AnimeGAN.test import test as gen
import os
import time
import xlrd

# -------------------------------------------------main---------------------------------------------

'''


'''
# 绘本 474,475,476,477,478,479,480,481,482,483,484,485,486,487,488,489,490,491,492,493,494,495


# 341,
# data = xlrd.open_workbook("D:/Workship/Pelbs/Gen/data/系列书名.xlsx")
data = xlrd.open_workbook(configer.run_param("EXCEL_PATH"))
data_sheet1 = data.sheets()[0]
rows = data_sheet1.nrows
book_idxs = data_sheet1.col_values(0)[1:]
book_idx_list = list(map(int, book_idxs))  # 99999       73, 82
# 卡通化模型位置
# anime_checkPoint_dir = "D:/Workship/Pelbs/Gen/project/AnimeGAN/checkpoint/AnimeGAN_Hayao_lsgan_300_300_1_3_10"
anime_checkPoint_dir =  configer.run_param("ANIMEGAN_CHECKPOINT_PATH")
work_path = configer.run_param("PROJECT_PATH")
error_output_path = work_path + "error/"
error_book_output_path = error_output_path + "book/"
if os.path.exists(error_book_output_path):
    utils.del_file(error_book_output_path)

def book_create():
    for index, id_ in enumerate(book_idx_list):
        utilsFile.set_book_idx(index, id_)

        # 合成音频
        pTTS.txt2audio()  # 音频生成
        # # # #合成图片
        # # # # #
        # anime_test_dir = utilsFile.get("res_osd_texture_path")
        # anime_result_dir = utilsFile.get("dest_texture_path")
        # gen(anime_checkPoint_dir, anime_result_dir, anime_test_dir)
        #
        # # # 不进行风格迁移，直接拷贝图片
        # utils.copy_pics(anime_test_dir, anime_result_dir)
        #
        # # 修改EnglishAudio文件
        osd_en_audio_file = utilsFile.get("osd_en_audio_file")
        osd_book_unit_file = utilsFile.get("osd_book_unit_file")
        dest_en_audio_file = utilsFile.get("dest_en_audio_file")

        #
        # # 判断tab是否出错
        # is_valid_audio_file = utils.tab_valid(osd_en_audio_file, error_book_output_path, id_, 5, 4)
        # is_valid_unit_file = utils.tab_valid(osd_book_unit_file, error_book_output_path, id_, 4, 4)
        # if (is_valid_audio_file and is_valid_unit_file):
        utils.modify_configs_v2(osd_en_audio_file, dest_en_audio_file)

def book_valid():
    is_valid = True
    for index, id_ in enumerate(book_idx_list):
        utilsFile.set_book_idx(index, id_)

        # # 修改EnglishAudio文件
        osd_en_audio_file = utilsFile.get("osd_en_audio_file")
        osd_book_unit_file = utilsFile.get("osd_book_unit_file")

        #
        # # 判断tab是否出错
        is_valid_audio_file = utils.tab_valid(osd_en_audio_file, error_book_output_path, id_, 5, 4)
        is_valid_unit_file = utils.tab_valid(osd_book_unit_file, error_book_output_path, id_, 4, 4)
        if (is_valid_audio_file == False or is_valid_unit_file == False):
            is_valid = False
    return is_valid


if __name__ == '__main__':
    # 绘本生成
    if (book_valid()):
        book_create()
    print("end")
