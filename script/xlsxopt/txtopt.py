
import os
import shutil
from script.base.configer import configer
from script.utils.utils import utils
from script.utils.utilsfile import utilsFile
from script.contentmgr import contentMgr
from script.utils.utilsword import utilsWord

class TxtOpt:
    def __init__(self):
        self.word_unit = ""
        self.recycles = [] #复习单元

    def reload(self):
        self.word_unit = ""
        self.recycles = [] #复习单元

    
    def recreate_config_folder(self):
        book_unit_file = utilsFile.get("book_unit_file")
        spk_config_path = utilsFile.get("spk_config_path")
        spk_book_unit_file = utilsFile.get("spk_book_unit_file")

        utils.recreate_folder(spk_config_path)
        shutil.copyfile(book_unit_file, spk_book_unit_file)

    def create_word_txt(self):  
        self.reload()
        self.recreate_config_folder()
        self.fix_audio_idx()

        audio_txt = utilsFile.get("spk_en_audio_file") 
        spk_en_followup_file = utilsFile.get("spk_en_followup_file")

        filed_word = "音乐标示\t音频路径\nSoundName\tPath\n" 
        utils.create_text_file(spk_en_followup_file, filed_word)
        
        for num, line in enumerate(open(audio_txt, 'r',  encoding="utf-8")):
            if num < 3 : continue
            audio_file_name = line.split("\t")[0]
            english_txt = line.split("\t")[1]
            unit_name, page_name = utils.split_file_name(audio_file_name)
            unit_type = contentMgr.get_unit_type(unit_name)
            
            if unit_type == "WORD" :  
                 
                followup_file = open(spk_en_followup_file, "a+",  encoding="utf-8")
                word_line = self.create_word_line(english_txt, audio_file_name)
                
                if word_line != "": 
                    print("followup_file write", word_line)
                    followup_file.write(word_line)
                followup_file.close()
            elif unit_type == "RECYCLE" :
                if unit_name not in self.recycles:  
                    self.recycles.append(unit_name)
              

        self.create_recycle()
        self.fix_word_idx()

        
        

    def create_recycle(self) :
        spk_en_followup_file = utilsFile.get("spk_en_followup_file")
        followup_file = open(spk_en_followup_file, "a+",  encoding="utf-8")
       
        for num, line in enumerate(open(spk_en_followup_file, 'r',  encoding="utf-8")):
            if num < 2 : continue
            audio_file_name = line.split("\t")[0]
            tag_file_name = line.split("\t")[1]
            unit_name, page_name = utils.split_file_name(audio_file_name)
            for recycle_name in self.recycles:
                recycle_idx = utilsWord.find_all_num(recycle_name) 
                unit_idx = utilsWord.find_all_num(unit_name)
                if  (unit_idx == 1 and recycle_idx == 1) or (unit_idx == 4 and recycle_idx == 2) or(unit_idx == 1 and recycle_idx == None) :
                    recycle_audio_name = recycle_name + "_followup_audio"
                    recycle_line = recycle_audio_name + "\t" + tag_file_name 
                    followup_file.write(recycle_line)
                    break
               
        followup_file.close()
    def create_word_line(self, english_txt, tag_audio_name):
        word_txt = english_txt.replace(" ", "").lower()

        if "LESSON" ==  contentMgr.get_unit_type(word_txt):
            self.word_unit = word_txt
        else :
            if self.word_unit == "" :return ""
        
        audio_name = self.word_unit + "_followup_audio"
        word_line = audio_name + "\t" + tag_audio_name  +"\n"
        
        return word_line
    
   
      
    def fix_audio_idx(self):
        temp_txt = utilsFile.get("osd_en_audio_file") 
        self.fix_idx(temp_txt)
        
    def fix_word_idx(self):
        word_txt = utilsFile.get("osd_en_word_file") 
        self.fix_idx(word_txt)


    def fix_idx(self, txt_file):  
        print("txt_file", txt_file)
        bak_file = "%s.bak" % txt_file[:-4]
        faudio = open(bak_file, "w", encoding="utf-8")

        idx = 1
        cur_unit_name = ""
        for num, line in enumerate(open(txt_file, 'r',  encoding="utf-8")):
            if num > 1:
                print("fix_idx", num, line.rstrip("\n"))
                sound_file = line.split("\t")[0]
                unit_name = sound_file.split("_")[0]
                page_name = sound_file.split("_")[1]
                unit_page_name = unit_name + "_" + page_name

                if cur_unit_name != unit_page_name:
                    cur_unit_name = unit_page_name
                    idx = 1
                else:
                    idx = idx + 1

                new_unit_name = unit_page_name + "_audio" + str(idx)
                new_line = line.replace(sound_file, new_unit_name)
                #print("fix_audio_idx",sound_file, new_unit_name)
            else:
                new_line = line
            
            faudio.write(new_line)

        faudio.close()
        os.remove(txt_file)
        os.rename(bak_file, txt_file)

    def create_ddt_word_txt(self):  

        osd_en_word_file = utilsFile.get("osd_en_word_file")
        filed_word = "音乐标示\t英文内容\t中文翻译\nSoundName\tContent\tChinese\n" 
        utils.create_text_file(osd_en_word_file, filed_word)
        word_file = open(osd_en_word_file, "a+",  encoding="utf-8")
        audio_file = utilsFile.get("spk_en_audio_file") 
        
        for num, line in enumerate(open(audio_file, 'r',  encoding="utf-8")):
            if num < 3 : continue
            audio_file_name = line.split("\t")[0]
            english_txt = line.split("\t")[1]
            unit_name, page_name = utils.split_file_name(audio_file_name)
            unit_type = contentMgr.get_unit_type(unit_name)
            
            if unit_type == "WORD" :  
                print("word_file write", line)
                word_file.write(line)
                word_file.close()
            
        self.fix_word_idx()


    def text_cover_file(self, file, text):   
        file.seek(0)
        file.truncate()
        file.write(str(text))
            

tOpt = TxtOpt()