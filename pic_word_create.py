from script.utils.WordUtil import wordUtil
from script.utils.utils import utils
from script.base.configer import configer
if __name__ == '__main__':
    PROJECT_PATH = configer.run_param("PROJECT_PATH")
    # 调用方法
    # wordUtil.wordClearRepeat(PROJECT_PATH + "/res/org/resource", PROJECT_PATH + "dest/pic_word/", "result.txt", PROJECT_PATH + "/res/org/bookCode/书本编号.txt")
    # wordUtil.wordClearRepeat("D:\Workship\Pelbs\Books\教材\初中英语", PROJECT_PATH + "dest/pic_word/", "result-小学英语(含年级).txt", PROJECT_PATH + "/res/org/bookCode/书本编号.txt")
    # wordUtil.append_word(PROJECT_PATH + "dest/pic_word/result-小学英语(含年级)1.txt", ["D:/Workship/Pelbs/Books/教材/小学英语/冀教",
    #                                                                                  "D:/Workship/Pelbs/Books/教材/小学英语/湘少",
    #                                                                                  "D:/Workship/Pelbs/Books/教材/小学英语/闽教" ], PROJECT_PATH + "/res/org/bookCode/书本编号.txt")

    # 读取result.txt中去重后的单词
    # utils.getImgByWord(PROJECT_PATH + "dest/pic_word/result-初中英语.txt", 5, " 卡通图像",   PROJECT_PATH + "dest/pic_word/初中英语-百度/")

    # utils.run_get_google_pic("C:\Program Files\Google\Chrome\Application\chromedriver.exe", PROJECT_PATH + "dest/pic_word/result-小学英语.txt", "cartoon image", 5, 5, PROJECT_PATH + "dest/pic_word/小学英语-谷歌/")

    # 判断生成的图片是否是5张
    # utils.findFilesWithoutNPic("D:\Workship\Pelbs\Gen\dest\pic_word", 5)
    #
    # print(utils.in_valid_files)

    # pdf转图片
    # utils.pdf_to_image("C:\\Users\\40198\\Desktop\\新版PEP小学英语三年级上册电子课本.pdf", "C:\\Users\\40198\\Desktop\\pics-2\\", 5, 5, 0)

    # 追加音标
    utils.append_phonetic(PROJECT_PATH + "dest/pic_word/", "result-小学英语(含湘少，冀教一起，闽教).txt" , 2)
    # 合并文件夹
    utils.merge_baidu_google_files("D:/Workship/Pelbs/Gen/dest/pic_word/小学英语-谷歌-重新抓", "D:/Workship/Pelbs/Gen/dest/pic_word/小学英语-百度-重新抓", "D:/Workship/Pelbs/Gen/dest/pic_word/小学英语-合并-重新抓")