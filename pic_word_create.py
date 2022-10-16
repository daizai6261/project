from script.utils.WordUtil import wordUtil
from script.base.configer import configer
if __name__ == '__main__':
    PROJECT_PATH = configer.run_param("PROJECT_PATH")
    # 调用方法
    wordUtil.wordClearRepeat(PROJECT_PATH + "/res/org/resource", PROJECT_PATH + "dest/pic_word/", "result.txt")
    # wordUtil.findFiles("../../res/org/resource")