import shutil

from script.orc.pelbsorc import pORC
from script.utils.utils import utils
from script.utils.utilsfile import utilsFile
from script.tts.pelbstts import pTTS
from script.base.configer import configer
import os
import xlrd
import re

from script.xlsxopt.pxlsx import pXlsx

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
series = data_sheet1.col_values(5)[1:]
series_list = list(map(int, series))
splits = data_sheet1.col_values(8)[1:]
split_list = list(map(int, splits))
start_nums = data_sheet1.col_values(7)[1:]
start_num_list = list(map(int, start_nums))

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

def pdf_to_excel():
    for index, id_ in enumerate(book_idx_list):
        utilsFile.set_book_idx(index, id_)
        # 创建config、texture文件夹
        [config_path, texture_path] = remake_dir(series_list[index], id_)
        # pdf转图片、并拷贝图片文件
        pdf_to_img(work_path + "temp/pdf/" + book_name_list[index] + ".pdf",
                   utilsFile.get("temp_texture_path_raw"), split_list[index], start_num_list[index], id_)
        pORC.orc2xls(True)
        pXlsx.xls2txt(True, True)
        # # 拷贝生成出来的配置文件到config文件夹
        copy_files(id_, config_path)
        # 绘本生成
        if book_valid():
            book_create()


# 创建config、texture文件夹
def remake_dir(series_num, book_id):
    book_path = work_path + "res/org/series" + str(series_num) + "/book" + str(book_id)
    utils.delete_folder(book_path)
    config_path = book_path + "/osd_configs/"
    texture_path = book_path + "/osd_texture/"
    utils.mkdir(config_path)
    utils.mkdir(texture_path)
    return [config_path, texture_path]


# 拷贝生成出来的文件到config
def copy_files(book_id, config_path):
    utils.resFileList = []
    utils.findFiles(work_path + "temp/bookCfg", r"BookUnit_" + str(book_id) + ".txt")
    book_unit_file = utils.resFileList[0]
    utils.resFileList = []
    utils.findFiles(work_path + "temp/configs", r"EnglishAudio_" + str(book_id) + ".txt")
    english_audio_file = utils.resFileList[0]
    shutil.copy(book_unit_file, config_path + "BookUnit_" + str(book_id) + ".txt")
    shutil.copy(english_audio_file, config_path + "EnglishAudio_" + str(book_id) + ".txt")
    utils.resFileList = []


def book_create():
    for index, id_ in enumerate(book_idx_list):
        utilsFile.set_book_idx(index, id_)

        # 合成音频
        pTTS.txt2audio()  # 音频生成
        # # # #合成图片
        # # # # #
        anime_test_dir = utilsFile.get("res_osd_texture_path")
        anime_result_dir = utilsFile.get("dest_texture_path")
        # gen(anime_checkPoint_dir, anime_result_dir, anime_test_dir)
        #
        # # # 不进行风格迁移，直接拷贝图片
        utils.copy_pics(anime_test_dir, anime_result_dir)
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
        utils.modify_configs_v3(osd_en_audio_file, dest_en_audio_file)


def book_valid():
    is_valid = True
    for index, id_ in enumerate(book_idx_list):
        utilsFile.set_book_idx(index, id_)

        # # 修改EnglishAudio文件
        osd_en_audio_file = utilsFile.get("osd_en_audio_file")
        osd_book_unit_file = utilsFile.get("osd_book_unit_file")

        #
        # # 判断tab是否出错
        is_valid_audio_file = utils.tab_valid(osd_en_audio_file, error_book_output_path, id_, 6, 5)
        is_valid_unit_file = utils.tab_valid(osd_book_unit_file, error_book_output_path, id_, 4, 4)
        if (is_valid_audio_file == False or is_valid_unit_file == False):
            is_valid = False
    return is_valid


def pdf_to_img(pdf_path, temp_texture_path_raw, split, start_num, book_id):
    # 先清空
    utils.delete_folder(temp_texture_path_raw)
    utils.mkdir(temp_texture_path_raw)
    utils.pdf_to_image(pdf_path, temp_texture_path_raw, 5, 5, 0)

    img_list = os.listdir(temp_texture_path_raw)

    # 用来存储单元图片名称
    unit_list = []
    pattern = re.compile(r'\d+')
    # 读取BookUnit文件
    utils.resFileList = []
    utils.findFiles(work_path + "temp/bookCfg", r"BookUnit_" + str(book_id) + ".txt")
    book_unit_file = utils.resFileList[0]
    count = 0
    with open(book_unit_file, "r", encoding="utf-8") as f:
        for line in f:
            count += 1
            # 前两行忽略
            if count <= 2:
                continue
            else:
                numbers = pattern.findall(line)
                unit_name = line.split("\t")[1]
                for i in range(0, int(numbers[-1])):
                    unit_list.append(unit_name + "_page" + str(i + 1) + ".png")

    pic_index = 0

    res_texture_path_excel = utilsFile.get("res_texture_path_1")
    utils.delete_folder(res_texture_path_excel)
    utils.mkdir(res_texture_path_excel)
    for img_num in range(start_num - 1, len(img_list)):
        res_texture_path = utilsFile.get("res_texture_path_2")
        unit_name = unit_list[pic_index].split("_")[0]
        utils.mkdir(res_texture_path_excel + unit_name)
        # 1表示需要进行图片切割)
        if split == 1:
            [left_img, right_img] = utils.img_split(temp_texture_path_raw + str(img_num) + ".png")
            # 保存一份到res文件夹
            left_img.save(res_texture_path + unit_list[pic_index])
            # 保存一份到res的texture中按unit区分
            left_img.save(res_texture_path_excel + unit_name + "/" + unit_list[pic_index])
            pic_index += 1
            # 保存一份到res文件夹
            right_img.save(res_texture_path + unit_list[pic_index])
            right_img.save(res_texture_path_excel + unit_name + "/" + unit_list[pic_index])
            pic_index += 1
            pass
        else:
            # 拷贝一份到res文件夹
            shutil.copy(temp_texture_path_raw + str(img_num) + ".png", res_texture_path + unit_list[pic_index])
            shutil.copy(res_texture_path_excel + unit_name + "/" + unit_list[pic_index])
            pic_index += 1
            pass


if __name__ == '__main__':
    pdf_to_excel()
