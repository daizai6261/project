from script.utils.WordUtil import wordUtil
from script.utils.utils import utils
from script.base.configer import configer
if __name__ == '__main__':
    PROJECT_PATH = configer.run_param("PROJECT_PATH")
    # 调用方法
    wordUtil.wordClearRepeat(PROJECT_PATH + "/res/org/resource", PROJECT_PATH + "dest/pic_word/", "result.txt")
    # 读取result.txt中去重后的单词
    utils.getImgByWord(PROJECT_PATH + "dest/pic_word/result.txt", 10,  PROJECT_PATH + "dest/pic_word/")