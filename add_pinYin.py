from script.utils.utils import utils
from script.base.configer import configer


def transformPinyin(fileRoot, errorFile):
    '''
    @param fileRoot: 需要转化的文件路径
    @param errorFile: 输出的错误文件路径
    @return:
    '''
    errorFileData = ''
    for file in fileRoot:
        count = 0
        with open(file, "r", encoding="utf-8") as f:
            file_data = ''
            for line in f:
                count = count + 1
                if len(line.split('\t')) != 5:
                    new_error = file + '下的第' + str(count) + '行tab键有误' + '\n'
                    errorFileData += new_error
                    new_line = line
                else:
                    if count == 1:
                        line_content = line.split('\t')
                        line_content.insert(4, '词语拼音')
                        new_line = '\t'.join(line_content)
                    elif count == 2:
                        line_content = line.split('\t')
                        line_content.insert(4, 'CiYuPinyin')
                        new_line = '\t'.join(line_content)
                    else:
                        if line[-2] == '1':
                            new_line = line
                        else:
                            line_content = line.split('\t')
                            line_content.insert(4, utils.pinyin(line_content[3]))
                            new_line = '\t'.join(line_content)
                file_data += new_line
            with open(file, "w", encoding="utf-8") as fi:
                fi.write(file_data)
    if errorFileData != '':
        with open(errorFile, "w", encoding="utf-8") as fe:
            fe.write(errorFileData)


if __name__ == '__main__':
    PROJECT_PATH = configer.run_param("PROJECT_PATH")
    utils.resFileList = []
    utils.findFiles(PROJECT_PATH + "/res/org/小学语文/", r"ChnWriteZi_[0-9]*.txt$")
    utils.findFiles(PROJECT_PATH + "/res/org/小学语文/", r"CHNWord_[0-9]*.txt$")
    errFile = PROJECT_PATH + "/res/org/小学语文/error.txt"

    transformPinyin(utils.resFileList, errFile)

    # print(res)
