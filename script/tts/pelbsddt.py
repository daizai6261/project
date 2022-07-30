import os
import re
import shutil
import linecache
import math
from PIL import Image

from script.utils.utils import utils
from script.utils.utilsfile import utilsFile
from script.utils.utilsword import utilsWord
from script.contentmgr import contentMgr


class PelbsDDT:
    def __init__(self):
        self.unit_page_idx = 0
        self.page_dir_list = []

    def trans_ddt_book(self):
        self.create_book_pic()
        self.create_book_res()
        self.create_audio_txt()

        self.create_word_hz_res()

    def create_book_pic(self):
        ddt_cover_file = utilsFile.get("ddt_cover_file")
        dest_cover_file =  utilsFile.get("dest_cover_file")
        shutil.copyfile(ddt_cover_file, dest_cover_file)

    def create_book_res(self):
        book_unit_file = utilsFile.get("book_unit_file")
        dest_path = utilsFile.get("dest_path")
        osd_texture_path = utilsFile.get("osd_texture_path")
        osd_book_unit_file = utilsFile.get("osd_book_unit_file")
        
        osd_sound_path = utilsFile.get("osd_sound_path")
        osd_config_path = utilsFile.get("osd_config_path")

        utils.delete_folder(dest_path)
        utils.recreate_folder(dest_path)
        utils.recreate_folder(osd_texture_path)
        utils.recreate_folder(osd_sound_path)
        utils.recreate_folder(osd_config_path)

        shutil.copyfile(book_unit_file, osd_book_unit_file)
        self.reset_page_dir_list()
        self.unit_page_idx = 0
        self.tran_page_num = 0
        for num, line in enumerate(open(book_unit_file, 'r',  encoding="utf-8")):
            
            if num < 2 : continue
            print("create_book_res line:" + str(num) + line)
            unit_name = line.split("\t")[1]
            page_num = int(line.split("\t")[3])
            self.tran_page_num = self.tran_page_num + int(page_num)
            #if "WORD" != contentMgr.get_unit_type(unit_name):
            self.copy_and_rename( unit_name, page_num)

        print(str(book_unit_file) + "转换页数：" + str(self.tran_page_num) + "。完整页数：" + str(len(self.page_dir_list))  )
        assert self.tran_page_num == len(self.page_dir_list), "页数转换错误"

    def copy_and_rename(self, unit_name, page_num): 
        osd_texture_path = utilsFile.get("osd_texture_path") 
        osd_sound_path = utilsFile.get("osd_sound_path") 
        unit_textur_path = osd_texture_path + unit_name + "/"
        unit_sound_path = osd_sound_path + unit_name + "/"
        utils.recreate_folder(unit_textur_path)
        utils.recreate_folder(unit_sound_path)

        ddt_book_path = utilsFile.get("ddt_book_path")
        
        for idx in range(0, page_num): 
            list_idx = self.unit_page_idx + idx
            #print("copy_and_rename list_idx", list_idx, self.page_dir_list, len(self.page_dir_list))
            #print("copy_and_rename page_idx", list_idx, self.page_dir_list[list_idx])
            ddt_page_path = ddt_book_path  + self.page_dir_list[list_idx] + "/"
            #图片
            source_jpg_path = ddt_page_path + "pic.jpg"
            target_jpg_path = unit_textur_path  + unit_name + "_page" + str(idx + 1) + ".jpg"
            shutil.copyfile(source_jpg_path, target_jpg_path)

            #音频
            audio_list = utils.get_special_file(ddt_page_path, ".mp3")
            for audio in audio_list: 
                source_audio_path = ddt_page_path + audio
                target_audio_path = unit_sound_path  + unit_name + "_page" + str(idx + 1) +  "_audio" + audio
                shutil.copyfile(source_audio_path, target_audio_path)

            if idx == page_num - 1:
                self.unit_page_idx = self.unit_page_idx + page_num

    def reset_txt(self):
        osd_en_audio_file = utilsFile.get("osd_en_audio_file") 
        filed = "音乐标示\t英文内容\t中文翻译\t位置\t行数\nSoundName\tContent\tChinese\tPos\tLine\n" 
        utils.create_text_file(osd_en_audio_file, filed)
        self.reset_page_dir_list()
        self.unit_page_idx = 0


    def create_audio_txt(self):
        self.reset_txt()

        book_unit_file = utilsFile.get("book_unit_file")
        osd_en_audio_file = utilsFile.get("osd_en_audio_file")
        ddt_book_path = utilsFile.get("ddt_book_path")

        faudio = open(osd_en_audio_file, "a+",  encoding="utf-8")
        
        for num, line in enumerate(open(book_unit_file, 'r',  encoding="utf-8")):
            if num < 2 : continue
            unit_name = line.split("\t")[1]
            page_num = int(line.split("\t")[3])

            for page_idx in range(0, page_num):
                
                list_idx = self.unit_page_idx + page_idx
                ddt_page_path = ddt_book_path  + self.page_dir_list[list_idx] + "/"
                txt = self.create_lesson_txt(unit_name, page_idx, ddt_page_path)
               
                if txt != "": faudio.write(txt)

                if page_idx == page_num - 1:
                    self.unit_page_idx = self.unit_page_idx + page_num
                

    def create_lesson_txt(self, unit_name, page_idx, ddt_page_path):
        ddt_book_path = utilsFile.get("ddt_book_path")
        list_idx = self.unit_page_idx + page_idx
        ddt_page_path = ddt_book_path  + self.page_dir_list[list_idx] + "/"
        ddt_char_file = ddt_page_path + "Char.txt"
        ddt_xy_file = ddt_page_path + "XY.txt"
        ddt_pic_file = ddt_page_path + "pic.jpg"
        page_txt = ""

        if not os.path.isfile(ddt_xy_file) : return page_txt
        
        for num, line in enumerate(open(ddt_xy_file, 'r',  encoding="utf-8")):
            if num < 1 : continue
            audio_name = unit_name + "_page" + str(page_idx + 1) + "_audio" + str(num)
            english = "EngTxtContent"
            chinese = linecache.getline(ddt_char_file, num + 1).rstrip("\n")
            pos = self.trans_ddt_coordinate(line, ddt_pic_file)
            book_dir = utilsFile.get_book_dir()
           # if book_dir == "HB":        #横屏
               # pos = self.trans_ddt_coordinate_ls(line, ddt_pic_file)
            ln = "1"
            print("create_lesson_txt",audio_name, chinese, pos, ln)
            page_txt = page_txt + audio_name + "\t" + english + "\t" + chinese + "\t" + pos + "\t" + str(ln) + "\n"
        return page_txt
            

    def trans_ddt_coordinate(self, line, ddt_pic_file):
        im = Image.open(ddt_pic_file)
        pos_list = line.rstrip("\n").split(",")
        x,y = im.size
        nex_x = 1080
        new_y = math.ceil(y * (1080/x)) 
        new_y = 1700

        l = math.floor((float("0" + pos_list[0]) * nex_x))
        t = math.floor((float("0" + pos_list[1]) * new_y))
        r = math.floor((float("0" + pos_list[2]) * nex_x))
        b = math.floor((float("0" + pos_list[3]) * new_y))
        w = r - l
        h = b - t

        pos_line = str(t) + "," +  str(l) +"," + str(w)  +","+ str(h)
        return pos_line

    #横屏显示图片
    def trans_ddt_coordinate_ls(self, line, ddt_pic_file):
        im = Image.open(ddt_pic_file)
        pos_list = line.rstrip("\n").split(",")
        x,y = im.size
        nex_x = 2160
        new_y = math.ceil(y * (2160/x)) 
        new_y = 1080

        l = math.floor((float("0" + pos_list[0]) * nex_x))
        t = math.floor((float("0" + pos_list[1]) * new_y))
        r = math.floor((float("0" + pos_list[2]) * nex_x))
        b = math.floor((float("0" + pos_list[3]) * new_y))
        w = r - l
        h = b - t

        pos_line = str(t) + "," +  str(l) +"," + str(w)  +","+ str(h)
        return pos_line

    def create_word_hz_res(self): 
        ddt_hanzi_file = utilsFile.get("ddt_hanzi_file")
     
        if os.path.exists(ddt_hanzi_file):
            self.create_hanzi_res()
        else :
            self.create_word_res()
            
   

    def create_word_res(self):  
        print("create_word_res")
        osd_en_word_file = utilsFile.get("osd_en_word_file")
        ddt_book_path = utilsFile.get("ddt_book_path")
        ddt_words_file = utilsFile.get("ddt_words_file") 

        filed_word = "音乐标示\t英文内容\t中文翻译\nSoundName\tContent\tChinese\n" 
        utils.create_text_file(osd_en_word_file, filed_word)
        followup_file = open(osd_en_word_file, "a+",  encoding="utf-8")

        if not os.path.exists(ddt_words_file): 
            return

        for num, line in enumerate(open(ddt_words_file, 'r',  encoding="utf-8")):
            word_txt = line.rstrip("\n").lower()
            if num < 1 : continue
            print("ddt_followup_file word_txt",line, word_txt, contentMgr.get_unit_type(word_txt))
           
            if "LESSON" == contentMgr.get_unit_type(word_txt) : 
                self.word_unit = word_txt.replace(" ", "").strip()
                self.word_idx = 1
            else :
                word_txt= utilsWord.delete_between_symbol(word_txt, "/")
                print(" delete_between_symbol", word_txt,)
                english = word_txt.split("//")[0]
                chinese = word_txt.split("//")[1]
                
                audio_name = self.word_unit + "_followup_audio" + str(self.word_idx)
                word_line = audio_name + "\t" + english + "\t" + chinese +"\n"
                followup_file.write(word_line)
                
                #同时拷贝一下音频资源
                filter_english = english.rstrip("?") 
                source_word_path = ddt_book_path + "Words/" + filter_english + ".mp3"
                target_word_path = utilsFile.get("osd_sound_path")   + self.word_unit  + "/"+ audio_name   + ".mp3"
                print("copyfile write", self.word_unit, source_word_path, target_word_path)
                shutil.copyfile(source_word_path, target_word_path)

                self.word_idx = self.word_idx + 1

        followup_file.close()

    def create_hanzi_res(self):  
        osd_chnword_file = utilsFile.get("osd_chnword_file")
        ddt_hanzi_file = utilsFile.get("ddt_hanzi_file")
        ddt_book_path = utilsFile.get("ddt_book_path")
        osd_cnsound_path = utilsFile.get("osd_cnsound_path")
        utils.recreate_folder(osd_cnsound_path)

        filed_word = "音乐标示\t字\t拼音\t词语\t是否标题\nSoundName\tZi\tPinyin\tWord\tIsTitle\n" 
        utils.create_text_file(osd_chnword_file, filed_word)
        chnword_file = open(osd_chnword_file, "a+",  encoding="utf-8")
        self.chnword_idx = 0
        self.chnword_unit = 0
        for num, line in enumerate(open(ddt_hanzi_file, 'r',  encoding="utf-8")):
            if num < 1 : continue
            hanzi_txt = line.rstrip("\n")
            if not re.search(":", hanzi_txt):
                self.chnword_idx = 0
                self.chnword_unit = self.chnword_unit + 1
                audio_name = "chnunit" + str(self.chnword_unit)  + "_chnword_audio" + str(self.chnword_idx)
                word_line = audio_name + "\t"  + hanzi_txt + "\t拼音" + "\t词组" + "\t1" + "\n"
            
            else:
                
                list = hanzi_txt.split("/")
                print("create_hanzi_res match", hanzi_txt, self.chnword_idx, self.chnword_unit, list)
                audio_name = "chnunit" + str(self.chnword_unit)  + "_chnword_audio" + str(self.chnword_idx)
                zi = list[0]
                pinyin = list[1]
                word = list[2]
                pathList = list[3].split(":")
                source_path = ddt_book_path + pathList[0] + "/" + pathList[1] + ".mp3"
                path = osd_cnsound_path + audio_name + ".mp3"
           
                word_line = audio_name + "\t" + zi + "\t" + pinyin + "\t" + word + "\t0"  +"\n"
                
                print("create_hanzi_res", path)
                shutil.copyfile(source_path, path)
                

            chnword_file.write(word_line)
            self.chnword_idx = self.chnword_idx + 1

        chnword_file.close()

    def reset_page_dir_list(self):
        self.page_dir_list = []        
        ddt_book_path = utilsFile.get("ddt_book_path")
        ls = os.listdir(ddt_book_path)
        for item in ls: 
            if os.path.isdir(ddt_book_path +  item) and item != "Words":  
                self.page_dir_list.append(item) 

        #print("page_dir_list", self.page_dir_list)
        self.page_dir_list = utils.list_num_sort(self.page_dir_list )

    
   

      

pddt = PelbsDDT()