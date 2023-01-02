import os
import math
import random
import shutil
import time

import requests
from script.utils.utilsfile import utilsFile
from script.utils.utilsword import utilsWord
from script.base.configer import configer
import cv2
from pydub import AudioSegment
import pypinyin
from bs4 import BeautifulSoup
import re
import demjson
from selenium import webdriver
import fitz
from PIL import Image

class Utils():
    # 用于存储非法的文件夹路径
    in_valid_files = []
    resFileList = []

    def cal_pos_max(self, max_pos_list, pos_list):
        lista = max_pos_list.split(",")
        listb = pos_list.split(",")

        if len(lista) != len(listb): return

        max_top = int(lista[0])
        max_left = int(lista[1])
        max_right = max_left + int(lista[2])
        max_buttom = max_top + int(lista[3])
        arr_max_pos = [max_top, max_left, max_right, max_buttom]

        top = int(listb[0])
        left = int(listb[1])
        right = left + int(listb[2])
        buttom = top + int(listb[3])
        arr_pos = [top, left, right, buttom]

        new_top = self.min(arr_max_pos[0], arr_pos[0])
        new_left = self.min(arr_max_pos[1], arr_pos[1])
        new_right = self.max(arr_max_pos[2], arr_pos[2])
        new_buttom = self.max(arr_max_pos[3], arr_pos[3])

        new_pos = str(new_top) + ", " + str(new_left) + ", " + str(new_right - new_left) + ", " + str(
            new_buttom - new_top)
        return new_pos

    def is_pos_close(self, pos1, pos2):
        dist = int(configer.program_param("POS_DIST"))
        list1 = pos1.split(",")
        list2 = pos2.split(",")

        if len(list1) != len(list2): return False

        top1 = int(list1[0])
        height1 = int(list1[3])
        top2 = int(list2[0])

        left1 = int(list1[1])
        width1 = int(list1[2])
        right1 = left1 + width1

        left2 = int(list2[1])
        width2 = int(list2[2])
        right2 = left2 + width2

        isallleft = (left1 <= left2) & (right1 <= left2)
        isallright = (right2 <= left1) & (right2 <= right1)

        is_close = ((abs(top1 + height1 - top2) < dist) & ((not isallleft) & (not isallright)))
        if is_close: return True
        return False

    def is_font_close(self, pos1, pos2, str1, str2):
        list1 = pos1.split(",")
        list2 = pos2.split(",")
        if len(list1) != len(list2): return False

        width1 = int(list1[2])
        width2 = int(list2[2])

        len1 = len(str1)
        len2 = len(str2)

        if (abs(width1 / len1 - width2 / len2) < 4): return True
        return False

    def max(self, a, b):
        return a if a > b else b

    def min(self, a, b):
        return a if a < b else b

    def is_odd(self, num):
        if (num % 2) == 0:
            return False
        else:
            return True

    def is_meta(self, path):
        file = os.path.splitext(path)
        filename, filetype = file
        if filetype == ".meta":
            return True
        else:
            return False

            # 按照数字顺序排序

    def list_num_sort(self, filelist):
        sorted_file = sorted(filelist, key=lambda x: int(x))
        return sorted_file

        # 单符号序列

    def list_single_sort(self, filelist, split):
        sorted_file = sorted(filelist, key=lambda x: int(x[:-4].split("_")[1]))
        return sorted_file

        # 前后两个序列 针对xx_yy_zz的格式

    def list_double_sort(self, filelist, split_word_pos):
        sort_num_first = []

        for file in filelist:
            if utils.is_meta(file): continue
            sort_list = file[:-4].split("_")
            sort_name = sort_list[split_word_pos]
            sort_idx = utilsWord.find_all_num(sort_name)
            if sort_idx:
                sort_num_first.append(sort_idx)  # 根据 _ 分割，转化为数字类型
        sort_num_first.sort()

        sorted_file = []
        for sort_num in sort_num_first:
            for read_file in filelist:
                if utils.is_meta(read_file): continue
                read_name_list = read_file[:-4].split("_")
                read_page_name = read_name_list[split_word_pos]

                read_name_idx = utilsWord.find_all_num(read_page_name)
                if read_name_idx and sort_num == int(read_name_idx):
                    sorted_file.append(read_file)
        return sorted_file

    def split_file_name(self, file):
        print("copy_and_rename file", file)
        arr = file.split('_', 2);
        unit_name = arr[0]
        page_name = arr[1]
        return unit_name, page_name

    def is_name_big(self, name1, name2):
        unit_name1, page_name1 = self.split_file_name(name1)
        unit_name2, page_name2 = self.split_file_name(name2)

        unit_name1_idx = unit_name1[:-1]
        page_name1_idx = page_name1[:-1]
        unit_name2_idx = unit_name2[:-1]
        page_name2_idx = page_name2[:-1]

        is_big = True
        if unit_name1_idx < unit_name2_idx:
            is_big = False
        elif unit_name1_idx == unit_name2_idx:
            is_big = page_name1_idx > page_name2_idx
        return is_big

    ###############################文件操作#########################################################

    def mkdir(self, path):
        folder = os.path.exists(path)
        if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径

    def delete_folder(self, filepath):
        if os.path.exists(filepath):
            shutil.rmtree(filepath)

    # 清空文件夹
    def clear_folder(self, path):
        for i in os.listdir(path):
            c_path = os.path.join(path, i)
            if os.path.isdir(c_path):
                self.clear_folder(c_path)
            else:
                if os.path.exists(c_path):
                    shutil.rmtree(path)

    def del_file(self, path):
        for i in os.listdir(path):
            path_file = os.path.join(path, i)  # 取文件绝对路径
            if os.path.isfile(path_file):
                os.remove(path_file)
            else:
                self.del_file(path_file)

    def recreate_folder(self, filepath):
        if os.path.exists(filepath):
            self.clear_folder(filepath)
        else:
            os.makedirs(filepath)

    def create_text_file(self, path, filed):
        file = open(path, 'w', encoding="utf-8")
        file.write(filed)
        file.close()

    def write_file(self, file_path, result):
        with open(file_path, "wb") as f:
            f.write(result)

    def copy_all_folder(self, source_path, target_path):

        if not os.path.exists(target_path):
            # 如果目标路径不存在原文件夹的话就创建
            os.makedirs(target_path)

        if os.path.exists(source_path):
            # 如果目标路径存在原文件夹的话就先删除
            shutil.rmtree(target_path)

        shutil.copytree(source_path, target_path)
        print('copy dir finished!', source_path, target_path)

    def get_special_file(self, path, fileType):
        sort_list = []
        ls = os.listdir(path)

        for item in ls:
            fileName, ft = os.path.splitext(item)
            if ft == fileType:
                sort_list.append(item)
        return sort_list

    def get_audio_db(self, path):
        input_music = AudioSegment.from_mp3(path)
        # print("get_audio_db",path, input_music.dBFS)
        return input_music.dBFS

    # 用于修改EnglishAudio文件的内容
    def modify_configs(self, origin_file, target_file, type):

        temp_dict = {}
        file_data = ""
        count = 0
        dest_texture_path = utilsFile.get("dest_texture_path")
        pic_w_h = self.read_pics(dest_texture_path)
        with open(origin_file, "r", encoding="utf-8") as f:
            for line in f:
                if count < 2:
                    new_line = line
                else:

                    line_contents = line.split("\t")
                    sound_name = line_contents[0]
                    chinese_content = line_contents[1]
                    sound_name_head = sound_name.rsplit("_", 1)[0]

                    if sound_name_head in temp_dict:
                        new_pos_index = temp_dict[sound_name_head]
                    else:
                        temp_dict[sound_name_head] = 0
                        new_pos_index = 0
                    new_x_y_w_h_num = self.calc_y_x_w_y_num_V2(chinese_content, sound_name_head, new_pos_index, pic_w_h,
                                                               type)
                    temp_dict[sound_name_head] = temp_dict[sound_name_head] + 1

                    new_line = sound_name + "\tEngTxtContent" + "\t" + chinese_content + "\t" + new_x_y_w_h_num

                file_data += new_line
                count = count + 1
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(file_data)

    # 用于修改EnglishAudio文件的内容  -1,-1,-1,-1 替换为1，2，3，4，5
    def modify_configs_v2(self, origin_file, target_file):
        file_data = ""
        count = 0
        dest_texture_path = utilsFile.get("dest_texture_path")
        # pic_w_h = self.read_pics(dest_texture_path)
        pic_w_h = 0
        with open(origin_file, "r", encoding="utf-8") as f:
            for line in f:
                if (len(line) == 0 or line == "\n"):
                    count = count + 1
                    continue
                if count < 2:
                    new_line = line
                else:
                    line_contents = line.split("\t")
                    sound_name = line_contents[0]
                    chinese_content = line_contents[1]
                    position = int(line_contents[2])
                    sound_name_head = sound_name.rsplit("_", 1)[0]

                    if position == 1:
                        new_line = sound_name + "\tEngTxtContent" + "\t" + chinese_content + "\t" + "-10,-10,-10,-10" + "\t" + self.calc_y_x_w_y_num_V2(
                            input=chinese_content, type=1)
                    elif position == 2:
                        new_line = sound_name + "\tEngTxtContent" + "\t" + chinese_content + "\t" + "-20,-20,-20,-20" + "\t" + self.calc_y_x_w_y_num_V2(
                            input=chinese_content, type=1)
                    # 情况为3、4、5的时候，position-3对应 0, 1, 2
                    else:
                        new_x_y_w_h_num = self.calc_y_x_w_y_num_V2(chinese_content,
                                                                   sound_name_head,
                                                                   position - 3,
                                                                   pic_w_h,
                                                                   type=0)
                        new_line = sound_name + "\tEngTxtContent" + "\t" + chinese_content + "\t" + new_x_y_w_h_num
                file_data += new_line
                count = count + 1
        file_data = file_data[: -1]
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(file_data)

    def modify_configs_v3(self, origin_file, target_file):
        file_data = ""
        count = 0
        dest_texture_path = utilsFile.get("dest_texture_path")
        pic_w_h = self.read_pics(dest_texture_path)
        with open(origin_file, "r", encoding="utf-8") as f:
            for line in f:
                if (len(line) == 0 or line == "\n"):
                    count = count + 1
                    continue
                if count < 2:
                    new_line = line
                else:
                    line_contents = line.split("\t")
                    sound_name = line_contents[0]
                    english_content = line_contents[1]
                    chinese_content = line_contents[2]
                    position = 1
                    if line_contents[3].isdigit():
                        position = int(line_contents[3])
                    sound_name_head = sound_name.rsplit("_", 1)[0]
                    pinyin = utils.pinyin(chinese_content)
                    if position == 1:
                        new_line = sound_name + '\t' + english_content + "\t" + chinese_content + "\t" + pinyin.rstrip() + "\t" + "-10,-10,-10,-10" + "\t" + self.calc_y_x_w_y_num_V2(
                            input=chinese_content, type=1)
                    elif position == 2:
                        new_line = sound_name + '\t' + english_content + "\t" + chinese_content + "\t" + pinyin.rstrip() + "\t" + "-20,-20,-20,-20" + "\t" + self.calc_y_x_w_y_num_V2(
                            input=chinese_content, type=1)
                    # 情况为3、4、5的时候，position-3对应 0, 1, 2
                    else:
                        new_x_y_w_h_num = self.calc_y_x_w_y_num_V2(chinese_content,
                                                                   sound_name_head,
                                                                   position - 3,
                                                                   pic_w_h,
                                                                   type=0)
                        new_line = sound_name + '\t' + english_content + "\t" + chinese_content + "\t" + pinyin.rstrip() + '\t' + new_x_y_w_h_num
                file_data += new_line
                count = count + 1
        file_data = file_data[: -1]
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(file_data)

    def calc_y_x_w_y_num(self, input="", pic_name="", new_pos_index=0, pic_w_h=0, type=0):
        '''
            :@param input: 输入的文本
            :@param pic_name: 背景图片名称
            :@param new_pos_index: 0 => 右上角，1 => 左下角，2 => 右下角
            :@param pic_w_h：所有图片的宽高字典
            :@param type：书的类型（1=>故事书）
        '''
        # 字符数量
        input_num = len(input)

        # 成语书
        if type == 1:
            # 成语书配置
            # 成语单个字符宽度设置
            # IDIOM_WORD_WIDTH = int(configer.word_param("IDIOM_WORD_WIDTH"))
            # 成语单个字符高度设置
            # IDIOM_WORD_HEIGHT = int(configer.word_param("IDIOM_WORD_HEIGHT"))
            # 成语书每行字符个数 (Math.ceil(图片宽度 * 0.9 / 每个字符宽度))
            idiom_num = int(configer.word_param("IDIOM_WORD_NUM"))
            # 成语书行数（Math.ceil(总字符数 /每行字符个数)）
            idiom_line_num = math.ceil(input_num / idiom_num)
            # 文本框位置：
            # 输入的字符数 < 规定的字符个数 => w = 输入字符数 * 字符字符宽度
            # w = input_num * IDIOM_WORD_WIDTH if input_num < idiom_num else idiom_num * IDIOM_WORD_WIDTH
            # # h = 行数 * 字符高度
            # h = idiom_line_num * IDIOM_WORD_HEIGHT
            # # x = Math.ceil(图片宽度 – w) / 2
            # x = math.ceil((pic_w_h[pic_name + "_w"] - w) / 2)
            # # y = 图片高度 –  h
            # y = pic_w_h[pic_name + "_h"] - h
            return str(idiom_line_num) + "\n"
        else:
            # 单个字符宽度
            WORD_WIDTH = int(configer.word_param("WORD_WIDTH"))
            # 单个字符高度
            WORD_HEIGHT = int(configer.word_param("WORD_HEIGHT"))
            # 每行字符个数
            WORD_NUM = int(configer.word_param("WORD_NUM"))
            # 文本框与图片间隔设置
            MARGIN = int(configer.word_param("MARGIN"))
            # 随机范围
            RANDOM = int(configer.word_param("RANDOM"))

            # 行数 = 字符数量 / 每行字符个数
            line_num = math.ceil(input_num / WORD_NUM)
            # 文本框宽度
            w = WORD_WIDTH * WORD_NUM
            # 文本框高度
            h = line_num * WORD_HEIGHT

            if new_pos_index == 0:
                # 文本框位置：x
                # x = pic_w_h[pic_name + "_w"] - MARGIN - w + random.randint(-RANDOM, RANDOM) - 250
                x = pic_w_h[pic_name + "_w"] - MARGIN - w + random.randint(-RANDOM, RANDOM)
                # 文本框位置：y
                y = MARGIN + random.randint(-RANDOM, RANDOM)
            elif new_pos_index == 1:
                x = MARGIN + random.randint(-RANDOM, RANDOM)
                y = pic_w_h[pic_name + "_h"] - MARGIN - h + random.randint(-RANDOM, RANDOM)
            else:
                # x = pic_w_h[pic_name + "_w"] - MARGIN - w + random.randint(-RANDOM, RANDOM) - 250
                x = pic_w_h[pic_name + "_w"] - MARGIN - w + random.randint(-RANDOM, RANDOM)
                y = pic_w_h[pic_name + "_h"] - MARGIN - h + random.randint(-RANDOM, RANDOM)

            if (self.condition_x_y_w_h(x, y, w, h, pic_w_h[pic_name + "_w"], pic_w_h[pic_name + "_h"])):
                return str(y) + "," + str(x) + "," + str(w) + "," + str(h) + "\t" + str(line_num) + "\n"
            else:
                return ""

    def calc_y_x_w_y_num_V2(self, input="", pic_name="", new_pos_index=0, pic_w_h=0, type=0):
        '''
            :@param input: 输入的文本
            :@param pic_name: 背景图片名称
            :@param new_pos_index: 0 => 右上角，1 => 左下角，2 => 右下角
            :@param pic_w_h：所有图片的宽高字典
            :@param type：书的类型（1=>故事书）
        '''
        # 字符数量
        input_num = len(input)

        pic_w = 2160
        pic_h = 1080

        # 成语书
        if type == 1:
            # 成语书配置
            # 成语单个字符宽度设置
            # IDIOM_WORD_WIDTH = int(configer.word_param("IDIOM_WORD_WIDTH"))
            # 成语单个字符高度设置
            # IDIOM_WORD_HEIGHT = int(configer.word_param("IDIOM_WORD_HEIGHT"))
            # 成语书每行字符个数 (Math.ceil(图片宽度 * 0.9 / 每个字符宽度))
            idiom_num = int(configer.word_param("IDIOM_WORD_NUM"))
            # 成语书行数（Math.ceil(总字符数 /每行字符个数)）
            idiom_line_num = math.ceil(input_num / idiom_num)
            # 文本框位置：
            # 输入的字符数 < 规定的字符个数 => w = 输入字符数 * 字符字符宽度
            # w = input_num * IDIOM_WORD_WIDTH if input_num < idiom_num else idiom_num * IDIOM_WORD_WIDTH
            # # h = 行数 * 字符高度
            # h = idiom_line_num * IDIOM_WORD_HEIGHT
            # # x = Math.ceil(图片宽度 – w) / 2
            # x = math.ceil((pic_w_h[pic_name + "_w"] - w) / 2)
            # # y = 图片高度 –  h
            # y = pic_w_h[pic_name + "_h"] - h
            return str(idiom_line_num) + "\n"
        else:
            # 单个字符宽度
            WORD_WIDTH = int(configer.word_param("WORD_WIDTH"))
            # 单个字符高度
            WORD_HEIGHT = int(configer.word_param("WORD_HEIGHT"))
            # 每行字符个数
            WORD_NUM = int(configer.word_param("WORD_NUM"))
            # 文本框与图片间隔设置
            MARGIN = int(configer.word_param("MARGIN"))
            # 随机范围
            RANDOM = int(configer.word_param("RANDOM"))

            # 行数 = 字符数量 / 每行字符个数
            line_num = math.ceil(input_num / WORD_NUM)
            # 文本框宽度
            w = WORD_WIDTH * WORD_NUM
            # 文本框高度
            h = line_num * WORD_HEIGHT

            if new_pos_index == 0:
                # 文本框位置：x
                # x = pic_w_h[pic_name + "_w"] - MARGIN - w + random.randint(-RANDOM, RANDOM) - 250
                x = pic_w - MARGIN - w + random.randint(-RANDOM, RANDOM)
                # 文本框位置：y
                y = MARGIN + random.randint(-RANDOM, RANDOM)
            elif new_pos_index == 1:
                x = MARGIN + random.randint(-RANDOM, RANDOM)
                y = pic_h - MARGIN - h + random.randint(-RANDOM, RANDOM)
            else:
                # x = pic_w_h[pic_name + "_w"] - MARGIN - w + random.randint(-RANDOM, RANDOM) - 250
                x = pic_w - MARGIN - w + random.randint(-RANDOM, RANDOM)
                y = pic_h - MARGIN - h + random.randint(-RANDOM, RANDOM)

            if (self.condition_x_y_w_h(x, y, w, h, pic_w, pic_h)):
                return str(y) + "," + str(x) + "," + str(w) + "," + str(h) + "\t" + str(line_num) + "\n"
            else:
                return ""

    def read_pics(self, directory_name):
        img_w_dict = {}
        for root, dirs, files in os.walk(directory_name):
            for filename in files:
                img_path = os.path.join(root, filename)
                # 读取图片
                img = cv2.imread(img_path)
                # 获取图片宽度
                w = img.shape[1]
                # 获取图片长度
                h = img.shape[0]
                # 获取图片名称（不包含后缀）
                file_name = filename.split(".")[0]
                img_w_dict[file_name + "_w"] = w
                img_w_dict[file_name + "_h"] = h
        return img_w_dict

    # 判断x,y,w,h是否符合要求
    def condition_x_y_w_h(self, x, y, w, h, img_w, img_h):
        MARGIN = int(configer.word_param("MARGIN"))
        if (x < 0):
            print("[x < 0] 不符合要求")
            return False
        if (y > img_h):
            print("[y > 图片高度] 不符合要求")
            return False
        if (w + MARGIN > img_w):
            print("[x + MARGIN > 图片宽度] 不符合要求")
            return False
        if (h + y > img_h):
            print("h + y > 图片高度不符合要求")
            return False
        return True

    # 不经过风格迁移直接复制图像
    def copy_pics(self, origin_path, target_path):
        self.mkdir(target_path)
        pics = os.listdir(origin_path)
        for pic in pics:
            unit_name = pic.split("_")[0]
            unit_path = target_path + "/" + unit_name
            self.mkdir(unit_path)
            origin_pic_path = origin_path + "/" + pic
            target_pic_path = unit_path + "/" + pic
            shutil.copyfile(origin_pic_path, target_pic_path)

    # 判断tab键个数是否合法
    def tab_valid(self, origin_file, error_book_output_path, id, title_word_num, content_word_num):
        count = 0
        msg = ""

        txtName = ""

        if title_word_num == 4:
            txtName = "BookUnit" + str(id)
        elif title_word_num == 5:
            txtName = "EnglishAudio_" + str(id)

        with open(origin_file, "r", encoding="utf-8") as f:
            flag = 0
            for line in f:
                if count < 2:
                    split_num = len(line.split("\t"))
                    if (split_num != title_word_num):
                        msg += "[" + origin_file + "]中的tab键个数出错：第" + str(count + 1) + "行tab键个数为" + str(
                            split_num - 1) + '\n'
                        print('\033[0;31;40m' + "[" + origin_file + "]中的tab键个数出错：第" + str(count + 1) + "行tab键个数为" + str(
                            split_num - 1) + '\033[0m')
                        flag = 1
                else:
                    line_contents = line.split("\t")
                    split_num = len(line_contents)
                    if (split_num != content_word_num):
                        msg += "[" + origin_file + "]中的tab键个数出错：第" + str(count + 1) + "行tab键个数为" + str(
                            split_num - 1) + '\n'
                        print('\033[0;31;40m' + "[" + origin_file + "]中的tab键个数出错：第" + str(count + 1) + "行tab键个数为" + str(
                            split_num - 1) + '\033[0m')
                        flag = 1
                count = count + 1
            # print("[" + origin_file + "]中的tab键没问题")
            if msg != "":
                if not os.path.exists(error_book_output_path):
                    # 如果目标路径不存在原文件夹的话就创建
                    os.makedirs(error_book_output_path)
                result_file = error_book_output_path + "book" + str(id) + "_" + txtName + ".txt"
                with open(result_file, "w", encoding="utf-8") as f:
                    f.write(msg)
            return flag == 0

    def pinyin(self, word):
        res = ''
        for i in pypinyin.pinyin(word, heteronym=False):
            res = res + ''.join(i) + " "
        return res

    def mov_files(self, source_path, target_path):
        ls = os.listdir(source_path)
        for item in ls:
            ls2 = os.listdir(source_path+item)
            if not os.path.exists(target_path + item):
                # 如果目标路径不存在原文件夹的话就创建
                os.makedirs(target_path + item)
            for sub_item in ls2:
                new_file_name = sub_item.replace('_en', '')
                if '_en' in sub_item:
                    shutil.copyfile(source_path+item+"/"+sub_item, target_path + item + "/" + new_file_name)
                    os.remove(source_path+item+"/"+sub_item)

    def genPhonetics(self, source_path, target_path):
        file_data = ""
        count = 0
        with open(source_path, "r", encoding="utf-8") as f:
            for line in f:
                if (len(line) == 0 or line == "\n"):
                    count = count + 1
                    continue
                if count < 2:
                    if(count == 0):
                        new_line = line[:-1] + "\t" + "美式音标\t" + "英式音标\n"
                    else:
                        new_line = line[:-1] + "\t" + "KkSymbol\t" + "IpaSymbol\n"
                else:
                    line_contents = line.split("\t")
                    word = line_contents[1]
                    #可能存在多个单词
                    words = word.split(" ")
                    US = ''
                    UK = ''
                    for w in words:
                        res, n = re.subn(r"[^a-zA-Z’]+", "", w)
                        [UK_temp, US_temp] = self.getPhonetic(res)
                        UK += UK_temp + " "
                        US += US_temp + " "
                    new_line = line[: -1] + "\t" + US[:-1] + '\t' + UK[:-1] + '\n'
                file_data += new_line
                count = count + 1
        file_data = file_data[: -1]
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(file_data)
        return True

    def getPhonetic(self, word):
        url = 'https://youdao.com/result?word=' + word +  '&lang=en'
        data = requests.get(url, proxies=random.choice(self.get_ips())).text
        soup = BeautifulSoup(data, 'lxml')
        data2 = soup.select('.phone_con > .per-phone > .phonetic')
        res = []
        for i in data2:
            res.append(i.text.replace(" ", ""))
        if len(res) != 2:
            return ['', '']
        return res

    def getPicture(self, index, chineseName, phraseOrWords, number, path):
        page = 0
        header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        url = 'https://image.baidu.com/search/acjson'
        params = {
            "tn": "resultjson_com",
            "logid": "11555092689241190059",
            "ipn": "rj",
            "ct": "201326592",
            "is": "",
            "fp": "result",
            "queryWord": phraseOrWords,
            "cl": "2",
            "lm": "-1",
            "ie": "utf-8",
            "oe": "utf-8",
            "adpicid": "",
            "st": "-1",
            "z": "",
            "ic": "0",
            "hd": "",
            "latest": "",
            "copyright": "",
            "word": phraseOrWords,
            "s": "",
            "se": "",
            "tab": "",
            "width": "",
            "height": "",
            "face": "0",
            "istype": "2",
            "qc": "",
            "nc": "1",
            "fr": "",
            "expermode": "",
            "force": "",
            "pn": str(60 * page),
            "rn": number,
            "gsm": "1e",
            "1617626956685": ""
        }
        # result = requests.get(url, headers=header, params=params).json()
        result = requests.get(url, headers=header, params=params,proxies=random.choice(self.get_ips())).text
        result = demjson.decode(result)
        url_list = []
        for data in result['data'][:-1]:
            url_list.append(data['thumbURL'])
        for i in range(len(url_list)):
            self.getImg(url_list[i], 60 * page + i, path + index + "_" + chineseName + "/")
            number -= 1
            if number == 0:
                break
        page += 1

    def getImg(self, url, idx, path):
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Safari/537.36'}
        img = requests.get(url, headers=header)
        if not os.path.exists(path):
            os.makedirs(path)
        file = open(path + str(idx) + '.jpg', 'wb')
        file.write(img.content)
        file.close()

    def getImgByWord(self, originPath, number, keyWord, outputPath):
        with open(originPath, 'r', encoding='utf-8') as f:
            for line in f:
                phraseOrWords = line.split('\t')[2].strip('\n')
                index = line.split('\t')[0]
                chineseName = line.split('\t')[3].strip('\n')
                utils.getPicture(index, chineseName, phraseOrWords + keyWord, number, outputPath)
                print(phraseOrWords + "抓取成功")
                time.sleep(2)


    def get_ips(self):
        ips1 = []
        url = configer.program_param("PC_URL")
        response = requests.get(url)
        ips = re.findall('\\d+\\.\\d+\\.\\d+\\.\\d*\\:\\d+', response.text, re.S)  ##正则表达式提取代理ip
        for i in range(len(ips)):
            ip = ips[i]
            proxies = {
                'http': "http://" + ip
            }  ##可选，http或者https
            try:
                test_ip_response = requests.get('https://www.baidu.com/', proxies=proxies)
            except Exception as e:
                print("代理异常")
            if test_ip_response.status_code == 200:
                ips1.append(proxies)
        return ips1

    def init_browser(self, url, chrome_driver):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        browser = webdriver.Chrome(executable_path=chrome_driver, chrome_options=chrome_options)
        # 浏览器访问指定的url
        browser.get(url)
        browser.maximize_window()
        return browser

    def get_google_pic(self, browser, num, sleep_time, output_path, idx, chineseName):
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        # 用于记录图片数量
        count = 0
        # 浏览器滚动条位置
        pos = 0
        while True:
            try:
                scroll_pos = 'let pos = document.documentElement.scrollTop=' + str(pos)
                pos += 300
                browser.execute_script(scroll_pos)
                time.sleep(0.5)
                img_elements = browser.find_elements_by_xpath('//a[@class="wXeWr islib nfEiy"]')
                try:
                    for img_element in img_elements:
                        img_element.click()
                        time.sleep(sleep_time)
                        try:
                            new_img_elements = browser.find_elements_by_xpath('//img[@class="n3VNCb KAlRDb"]')
                            if new_img_elements:
                                for new_img_element in new_img_elements:
                                    src = new_img_element.get_attribute('src')
                                    if src.startswith('http') and not src.startswith('https://encrypted-tbn0.gstatic.com'):
                                        print('Found' + str(count) + 'st image url')
                                        self.getImg(src, count, output_path + "/" + idx + "_" + chineseName + "/")
                                        count += 1
                                        if count >= num:
                                            return
                        except:
                            print("获取图片失败")
                    browser.back()
                    time.sleep(0.5)
                except:
                    print('获取页面失败')
            except:
                print("不能向下滑了")

    def run_get_google_pic(self, chrome_driver, origin_path, keyword_addition, num, sleep_time, output_path):
        with open(origin_path, 'r', encoding='utf-8') as f:
            for line in f:
                phrase_or_words = line.split('\t')[2].strip('\n')
                index = line.split('\t')[0]
                chineseName = line.split('\t')[3].strip('\n')
                url = 'https://www.google.com.hk/search?q=' + phrase_or_words + ' ' + keyword_addition + '&source=lnms&tbm=isch'
                browser = self.init_browser(url, chrome_driver)
                self.get_google_pic(browser, num, sleep_time, output_path, index, chineseName)
                browser.close()

    def get_word_code(self, file_path):
        word_code_dict = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line == '\n' or len(line) == 0:
                    continue
                line_contents = line.split("\t")
                code = line_contents[0]
                word = line_contents[1]
                word_code_dict[word] = code
        f.close()
        return word_code_dict

    def findFilesWithoutNPic(self, path, n):
        # 首先遍历当前目录所有文件及文件夹
        file_list = os.listdir(path)
        # 计算图片个数
        count = 0
        # 判断是不是文件夹
        flag = 0
        # 循环判断每个元素是否是文件夹还是文件，是文件夹的话，递归
        for file in file_list:
            # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
            cur_path = os.path.join(path, file)
            # 判断是否是文件夹
            if os.path.isdir(cur_path):
                flag = 1
                self.findFilesWithoutNPic(cur_path, n)
            else:
                # 判断是否是特定文件名称
                if re.match(r"^[0-9]*(\.png|\.jpg|\.jpeg)$", file, flags=0) != None:
                    count += 1
        if flag == 0 and count != n:
            self.in_valid_files.append(path)

    def pdf_to_image(self, pdf_path, img_path, x, y, rotation_angle):
        pdf = fitz.open(pdf_path)
        # 逐页读取PDF
        for pg in range(0, pdf.pageCount):
            page = pdf[pg]
            # 设置缩放和旋转系数
            trans = fitz.Matrix(x, y).preRotate(rotation_angle)
            pm = page.getPixmap(matrix=trans, alpha=False)
            # 开始写图像
            pm.writePNG(img_path + str(pg) + ".png")
        pdf.close()

    def findFiles(self, path, pattern):
        # 首先遍历当前目录所有文件及文件夹
        file_list = os.listdir(path)
        # 循环判断每个元素是否是文件夹还是文件，是文件夹的话，递归
        for file in file_list:
            # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
            cur_path = os.path.join(path, file)
            # 判断是否是文件夹
            if os.path.isdir(cur_path):
                self.findFiles(cur_path, pattern)
            else:
                # 判断是否是特定文件名称
                if re.match(pattern, file, flags=0)  != None:
                    self.resFileList.append(cur_path)

    # 将图片切成两份
    def img_split(self, img_path):
        img = Image.open(img_path)
        img_size = img.size
        # 图片高度
        h = img_size[1]
        # 图片宽度
        w = img_size[0]
        # 图片左边
        left_img = img.crop((0, 0, int(w/2), h))
        right_img = img.crop((int(w/2), 0, w, h))
        return [left_img, right_img]

    def append_phonetic(self, file_path, file_name, index):
        '''
        在文件每行的某个位置追加音标
        @param file_path: 需要追加的文件
        @param index: 所在位置
        @return:
        '''

        # 先找到slice文件
        self.resFileList = []
        self.findFiles(file_path, r"slice[0-9]*.txt")
        pattern = re.compile(r'\d+')
        # 用来存最后的slice文件号
        max_number = -1
        for slice_file in self.resFileList:
            numbers = pattern.findall(slice_file)
            number = int(numbers[0])
            if number >= max_number:
                max_number = number

        start_line = (max_number + 1) * 200

        # 当前行
        now_line = -1
        with open(file_path + file_name, 'r', encoding='utf-8') as f:
            result = ""
            # 每隔200个保存一次
            slice_count = 0
            slice_num = max_number + 1
            for line in f:
                now_line += 1
                if now_line < start_line:
                    continue
                word_contents = line.split("\t")[index]
                # 存在多个单词的情况
                words = word_contents.split(" ")
                US = ''
                UK = ''
                for w in words:
                    res, n = re.subn(r"[^a-zA-Z’]+", "", w)
                    time.sleep(2)
                    [UK_temp, US_temp] = self.getPhonetic(res)
                    UK += UK_temp + " "
                    US += US_temp + " "
                result += line[:-1] + "\t" + UK + "\t" + US + "\n"
                slice_count += 1
                if slice_count == 200:
                    with open(file_path + "slice" + str(slice_num) + ".txt", 'w', encoding='utf-8') as fi:
                        fi.write(result)
                        fi.close()
                    slice_count = 0
                    slice_num += 1
                    time.sleep(20)
                print(line[:-1] + "\t" + UK + "\t" + US + "\n")
            f.close()

    def merge_baidu_google_files(self, baidu_file_path, google_file_path, out_put_path):
        '''
        合并谷歌百度两个文件夹下的图片
        @param baidu_file_path: 百度图片根路径
        @param google_file_path: 谷歌图片根路径
        @param out_put_path: 合并后所在的根路径
        @return:
        '''

        if os.path.exists(out_put_path):
            shutil.rmtree(out_put_path)
        os.makedirs(out_put_path)

        files = os.listdir(baidu_file_path)
        for file in files:
            # 获取到某个单词文件夹路径
            cur_baidu_path = os.path.join(baidu_file_path, file)
            cur_google_path = os.path.join(google_file_path, file)
            try:
                cur_baidu_pic_paths = os.listdir(cur_baidu_path)
            except:
                print("找不到文件" + cur_baidu_pic_paths)
                continue

            try:
                cur_google_pic_paths = os.listdir(cur_google_path)
            except:
                print("找不到文件" + cur_google_pic_paths)
                continue

            dest_path = os.path.join(out_put_path, file)
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            os.makedirs(dest_path)

            index = 0
            for cur_pic_name in cur_baidu_pic_paths:
                try:
                    cur_pic_path = os.path.join(cur_baidu_path, cur_pic_name)
                    shutil.copy(cur_pic_path, dest_path + "/" + str(index) + ".png")
                except:
                    print("找不到文件" + cur_pic_path)
                    continue
                index += 1


            for cur_pic_name in cur_google_pic_paths:
                try:
                    cur_pic_path = os.path.join(cur_google_path, cur_pic_name)
                    shutil.copy(cur_pic_path, dest_path + "/" + str(index) + ".png")
                except:
                    print("找不到文件" + cur_pic_path)
                    continue
                index += 1

utils = Utils()
