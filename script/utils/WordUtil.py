import os
import re

class WordUtil:
    # 用于存储文件名字（^(EnglishFollowup)_[0-9]*(\.txt)$）的数组
    resFileList = []
    # 用于存储去重后的单词
    resList = []
    resChineseList = []

    # 用于存储映射关系
    resMapList = []

    # 根据文件位置读取文件，输出每行内容
    def readFile(self, filePath):
        # todo:将每行的第英文内容存储在这个list中，并且返回
        with open(filePath, "r", encoding="utf-8") as f:
            count = 0
            # line表示内容的每一行（按行读取）
            for line in f:
                count += 1
                if count > 2:
                    if line == "" or len(line) <= 0:
                        continue
                    words = line.split("\t")
                    if len(words) < 3:
                        continue
                    if words[1] not in self.resList:
                        self.resList.append(words[1])
                        self.resChineseList.append(words[2])

    # 将结果（result）输出到指定文件（filePath）
    def writeFile(self, filePath, fileName, result):
        if not os.path.exists(filePath):
            # 如果目标路径不存在原文件夹的话就创建
            os.makedirs(filePath)
        with open(filePath + "/" + fileName, "w", encoding="utf-8") as f:
            # 把result写出到txt文件
            f.write(result)

    # 单词去重
    def wordClearRepeat(self, fileInputPath, fileOutPath, fileOutName):
        # 1、获取文件夹下的所有文件
        self.findFiles(fileInputPath)
        # 调用book_num_map，先读取第四张图里面的，按行读取，存一个对应关系[{bookNum:276,code:11},{...},{}]

        bookNo = ''
        bookGrade = ''
        # 2、读取txt
        for file in self.resFileList:
            bookNo = file.split('.')[0]
            self.readFile(file)
        res = ""
        for index in range(len(self.resList)):
            if '\n' not in self.resChineseList[index]:
                self.resChineseList[index] = self.resChineseList[index] + "\n"
            res += str(index) + "\t" + bookGrade + '\t' + self.resList[index] + "\t" +self.resChineseList[index]

        # 3、输出txt
        self.writeFile(fileOutPath, fileOutName, res)


    def book_num_map(self, path):
        # TODO :先读取第四张图里面的，按行读取，存一个对应关系[{bookNum:276,code:11},{...},{}]
        self.resMapList = []
        pass

    def findFiles(self, path):
        # 首先遍历当前目录所有文件及文件夹
        file_list = os.listdir(path)
        # 循环判断每个元素是否是文件夹还是文件，是文件夹的话，递归
        for file in file_list:
            # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
            cur_path = os.path.join(path, file)
            # 判断是否是文件夹
            if os.path.isdir(cur_path):
                self.findFiles(cur_path)
            else:
                # 判断是否是特定文件名称
                if re.match(r"^(EnglishFollowup)_[0-9]*(\.txt)$", file, flags=0)  != None:
                    self.resFileList.append(cur_path)


wordUtil = WordUtil()

# if __name__ == '__main__':
#     # 创建对象
#     wordUtil = WordUtil()
#     # 调用方法
#     wordUtil.wordClearRepeat()
#     wordUtil.findFiles("./resource")
