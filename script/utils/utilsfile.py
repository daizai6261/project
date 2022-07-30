from script.base.configer import configer
import xlrd

class UtilsFile():
    def __init__(self):
        self.init_book()

    def get_book_dir(self):
        return self.book[self.book_idx]["dir"]

    def set_book_idx(self, book_index, book_idx):
        self.book_idx = book_idx
        self.book_series = str(int(self.book[book_index]["series"]))
        self.str_book_idx = str(book_idx)
        self.speaker = configer.program_param("CURRENT_SPEAKER").lower()

        self.paths["work_path"]  = "D:/Workship/Pelbs/Gen/"
        self.paths["temp_path"]  = self.paths["work_path"] + "temp/"
        self.paths["temp_texture_path"]  = self.paths["temp_path"] + "texture/"
        self.paths["temp_sound_path"]  = self.paths["temp_path"] + "sound/"
        self.paths["tts_idx_path"]  = self.paths["work_path"] + "data/tts_idx.txt"          #顺序控制文件


        self.paths["org_pic_path"] = self.paths["work_path"] + "org/"
        self.paths["pdf_book_path"] = self.paths["org_pic_path"] + "pdf/book" + self.str_book_idx + "/"
        self.paths["jpg_book_texture_path"] = self.paths["org_pic_path"] + "jpg/book" + self.str_book_idx + "/texture/"
        self.paths["jpg_book_sound_path"] = self.paths["org_pic_path"] + "jpg/book" + self.str_book_idx + "/sound"

        self.paths["res_path"] = self.paths["work_path"] + "res/org/series"+ self.book_series +"/book" + self.str_book_idx + "/"
        self.paths["res_sound_path"] = self.paths["res_path"] + "sound/"
        self.paths["res_osd_texture_path"] = self.paths["res_path"] + "osd_texture/"
        self.paths["dest_path"]  = self.paths["work_path"] + "dest/series"+ self.book_series +"/book" + self.str_book_idx + "/"
        # self.paths["dest_texture_path"] = self.paths["dest_path"] + self.speaker + "_texture/"
        self.paths["dest_texture_path"] = self.paths["dest_path"] + "osd_texture/"
        # self.paths["dest_config_path"] = self.paths["dest_path"] + self.speaker + "_configs/"
        self.paths["dest_config_path"] = self.paths["dest_path"] + "osd_configs/"
        # self.paths["dest_sound_path"] = self.paths["dest_path"] + self.speaker + "_sound/"
        self.paths["dest_sound_path"] = self.paths["dest_path"] + "osd_sound/"
        self.paths["dest_en_audio_file"] = self.paths["dest_config_path"] + "EnglishAudio_" + self.str_book_idx + ".txt"



        self.paths["temp_follow_file"] = self.paths["temp_path"] + "configs/"+ "EnglishFollowup_" + self.str_book_idx + ".txt"
        self.paths["txt_folder_path"] = self.paths["work_path"] + "dest/bookCfg/"
        self.paths["book_unit_file"] = self.paths["txt_folder_path"] + "BookUnit_" + self.str_book_idx + ".txt"


        self.paths["spk_config_path"] = self.paths["res_path"] + self.speaker + "_configs/"
        self.paths["spk_book_unit_file"] = self.paths["spk_config_path"] + "BookUnit_" + self.str_book_idx + ".txt"
        self.paths["spk_en_audio_file"] = self.paths["spk_config_path"] + "EnglishAudio_" + self.str_book_idx + ".txt"
        self.paths["spk_en_followup_file"] = self.paths["spk_config_path"] + "EnglishFollowup_" + self.str_book_idx + ".txt"


        self.paths["osd_texture_path"] = self.paths["dest_path"] + "osd_texture/"
        self.paths["osd_sound_path"] = self.paths["dest_path"] + "osd_sound/"
        # self.paths["osd_config_path"] = self.paths["dest_path"] + "osd_configs/"
        self.paths["osd_config_path"] = self.paths["res_path"] + "osd_configs/"
        self.paths["osd_book_unit_file"] = self.paths["osd_config_path"]  + "BookUnit_" + self.str_book_idx + ".txt"
        self.paths["osd_en_audio_file"] = self.paths["osd_config_path"]  + "EnglishAudio_" + self.str_book_idx + ".txt"
        self.paths["osd_en_word_file"] = self.paths["osd_config_path"] +  "EnglishFollowup_" + self.str_book_idx + ".txt"
        self.paths["osd_chnword_file"] = self.paths["osd_config_path"] +  "CHNWord_" + self.str_book_idx + ".txt"
        self.paths["osd_cnsound_path"] = self.paths["dest_path"] + "osd_chnword/"







    def get(self, key):
        value = self.paths[key]
        return value

    def get_book_type(self, index):
        return self.book[index]["type"]


    def init_book(self):
        self.paths = {}
        self.book = [] #复习单元
        data = xlrd.open_workbook("D:/Workship/Pelbs/Gen/data/系列书名.xlsx")
        data_sheet1 = data.sheets()[0]
        rows = data_sheet1.nrows
        book_idxs = data_sheet1.col_values(0)[1:]
        book_names = data_sheet1.col_values(1)[1:]
        book_series = data_sheet1.col_values(5)[1:]
        book_type = data_sheet1.col_values(6)[1:]

        for i in range(rows - 1):
            self.book.insert(int(book_idxs[i]), {'name':book_names[i],"type":"Renrendoukuatanglaoya", "series": book_series[i],"idx":int(book_idxs[i]), "dir":"HB",'type': int(book_type[i])})

utilsFile = UtilsFile()

# if __name__ == '__main__':
#     utilsFile = UtilsFile()
