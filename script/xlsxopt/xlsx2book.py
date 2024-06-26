import shutil

from script.utils.utils import utils
from script.utils.utilsfile import utilsFile

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


class Xlsx2Book:

    def excel2txt(self, index, id_):
        
        # 创建config、texture文件夹
        [config_path, texture_path] = self.remake_dir(series_list[index], id_)
        pXlsx.xls2txt(True, True)
        # # 拷贝生成出来的配置文件到config文件夹
        self.copy_files(id_, config_path)

    # 创建config、texture文件夹
    def remake_dir(self, series_num, book_id):
        book_path = work_path + "res/org/series" + str(series_num) + "/book" + str(book_id)
        utils.delete_folder(book_path)
        config_path = book_path + "/osd_configs/"
        texture_path = book_path + "/osd_texture/"
        utils.mkdir(config_path)
        utils.mkdir(texture_path)
        return [config_path, texture_path]

    # 拷贝生成出来的文件到config
    def copy_files(self, book_id, config_path):
        utils.resFileList = []
        utils.findFiles(work_path + "temp/configs", r"EnglishAudio_" + str(book_id) + ".txt")
        english_audio_file = utils.resFileList[0]
        shutil.copy(english_audio_file, config_path + "EnglishAudio_" + str(book_id) + ".txt")
        utils.resFileList = []


    def pdf_to_img(self, pdf_path, temp_texture_path_raw, split, start_num, book_id):
        # 先清空
        utils.delete_folder(temp_texture_path_raw)
        utils.mkdir(temp_texture_path_raw)
        utils.pdf_to_image(pdf_path, temp_texture_path_raw, 5, 5, 0)

        img_list = os.listdir(temp_texture_path_raw)

        # 用来存储单元图片名称
        unit_list = []
        pattern = re.compile(r'\d+')
        # 读取文件
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

        res_texture_path_excel = utilsFile.get("res_texture_path")
        utils.delete_folder(res_texture_path_excel)
        utils.mkdir(res_texture_path_excel)
        for img_num in range(start_num - 1, len(img_list)):
            res_texture_path = utilsFile.get("res_texture_path")
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


#
# if __name__ == '__main__':
#    excel_to_book()

xlsx2Book = Xlsx2Book()
