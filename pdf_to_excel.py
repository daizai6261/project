from script.orc.pelbsorc import pORC
from script.utils.utils import utils
from script.utils.utilsfile import utilsFile
from script.tts.pelbstts import pTTS
from script.base.configer import configer
import os
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

def pdf_to_excel():
    for index, id_ in enumerate(book_idx_list):
        utilsFile.set_book_idx(index, id_)
        pORC.orc2xls(True)





if __name__ == '__main__':
    pdf_to_excel();
