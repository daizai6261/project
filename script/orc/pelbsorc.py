import os
import re
import time
import math
from PIL import Image


from script.base.configer import configer
from script.utils.utils import utils
from script.utils.utilsword import utilsWord
from script.utils.utilsfile import utilsFile

from script.orc.bdorc import bdORCApi
from script.orc.alyorc import alyORCApi
from script.xlsxopt.pxlsx import pXlsx
from script.xlsxopt.basexlsx import bXlsx
from script.contentmgr import contentMgr

class PelbsORC:

    def orc2xls(self, restart = True): #整理上下文
        if restart :
            temp_texture_path = utilsFile.get("temp_texture_path")
            res_texture_path = utilsFile.get("res_texture_path")
            utils.copy_all_folder(res_texture_path, temp_texture_path)
            pXlsx.create_audio_excel(res_texture_path)      #创建xls文件

        temp_texture_path = utilsFile.get("temp_texture_path")
        unitList = os.listdir(temp_texture_path)

        for unit_folder in unitList:
            #print("for orc_single_pic", unit_folder)
            ismeta = utils.is_meta(temp_texture_path +  unit_folder)
            if ismeta: continue
            unitType =  contentMgr.get_unit_type(unit_folder)
            #if unitType == "WORD" or unitType == "RECYCLE" : continue         #单词单元不识别
            if unitType == "WORD" : continue         #单词单元不识别
            fileList = os.listdir(temp_texture_path + unit_folder)
            sortFileList = utils.list_double_sort(fileList, 1)
            self.orc_single_pic(unit_folder, sortFileList)


    def orc_single_pic(self, unit_folder, fileList):
        print("orc_single_pic", unit_folder)
        for item_file in fileList:
            time.sleep(1)
            temp_texture_path = utilsFile.get("temp_texture_path")
            image_path = temp_texture_path + unit_folder + "/" + item_file
            print("orc_single_pic", image_path)
            ismeta = utils.is_meta(image_path)
            if ismeta: continue

            result = alyORCApi.orc_generate(image_path)
            rate = self.get_img_rate(image_path)

            for word in result:
                self.orc_write_xls(item_file, word, rate['x'], rate['y'])

            os.remove(image_path)      #文字识别过了就把原来的删除

    def orc_write_xls(self, item_file, word, rate_x, rate_y):
        unit_page_name = item_file[:-4] + "_audio"
        unit, page = utils.split_file_name(unit_page_name)

        pos_top = math.ceil( word['Pos']['Top'] * rate_y)
        pos_left = math.ceil( word['Pos']['Left'] *rate_x )
        pos_width = math.ceil( word['Pos']['Width'] * rate_x )
        pos_height =  math.ceil( word['Pos']['Height'] * rate_y )
        pos = str(pos_top) + "," + str(pos_left) + "," + str(pos_width)  + "," + str(pos_height)
        txt = word['Txt']

        txt = self.format_english_txt(unit, txt)
        is_digit = txt.isdigit()
        is_empty = ( txt == "") | ( txt.isspace())
        is_all_punctuation = utilsWord.is_all_punctuation(txt)

        if (not is_digit) & ( not is_empty ) & ( not is_all_punctuation ):
            body = 1
            value = [unit_page_name, txt, pos, body]
            bXlsx.append_xls_value(unit, value)

    def get_img_rate(self, image_path):
        rate = {}
        img = Image.open(image_path)
        rate['x'] = float(format( 1080/img.size[0], '.3f'))
        rate['y'] = float(format( 1700/img.size[1], '.3f'))
        return rate

    def format_english_txt(self, name, txt):
        unit_type = contentMgr.get_unit_type(name)
        format_type = contentMgr.get_english_format_type(unit_type)

        if format_type == "LESSON_FORMAT" :
            txt = utilsWord.filter_special_symbol(txt)
            txt = utilsWord.replace_error_word(txt)
            txt = utilsWord.delete_contain_cn(txt)
        elif format_type == "WORD_FORMAT":
            txt = utilsWord.filter_special_word(txt)
            txt = utilsWord.filter_phonetic_symbol(txt)
            txt = utilsWord.replace_error_word(txt)

        elif format_type ==  "EXPRESSION_FORMAT":
            txt = utilsWord.filter_special_word(txt)
            txt = utilsWord.filter_phonetic_symbol(txt)

        return txt

    def orccn2xls(self, restart = True): #整理上下文
        self.is_en = True
        self.orc2xls(restart)

pORC = PelbsORC()


