import os
import re


class WordUtil:
    resFileList = []
    resList = []
    resChineseList = []
    resCodeList = []

    resMapList = []

    # 根据文件位置读取文件，输出每行内容
    def readFile(self, filePath, code):
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
                        self.resCodeList.append(code)

    # 将结果（result）输出到指定文件（filePath）
    def writeFile(self, filePath, fileName, result):
        if not os.path.exists(filePath):
            # 如果目标路径不存在原文件夹的话就创建
            os.makedirs(filePath)
        with open(filePath + "/" + fileName, "w", encoding="utf-8") as f:
            # 把result写出到txt文件
            f.write(result)

    # 单词去重
    def wordClearRepeat(self, fileInputPath, fileOutPath, fileOutName, mapFile):
        # 1、获取文件夹下的所有文件
        self.findFiles(fileInputPath)
        pattern = re.compile(r'\d+')
        self.book_num_map(mapFile)
        # 2、读取txt
        for file in self.resFileList:
            bookNum = pattern.findall(file)[-1]
            code = ""
            for bookObj in self.resMapList:
                if bookNum == bookObj["bookNum"]:
                    code = bookObj["code"]
            self.readFile(file, code)
        res = ""

        for index in range(len(self.resList)):
            if '\n' not in self.resChineseList[index]:
                self.resChineseList[index] = self.resChineseList[index] + "\n"
            res += str(index) + "\t" + self.resCodeList[index] + "\t" + self.resList[index] + "\t" + \
                   self.resChineseList[index]

        # 3、输出txt
        self.writeFile(fileOutPath, fileOutName, res)

    def book_num_map(self, path):
        pattern = re.compile(r'\d+')
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if len(line) <= 0 or "Book" not in line:
                    continue
                numbers = pattern.findall(line)
                self.resMapList.append({
                    "bookNum": numbers[0],
                    "code": numbers[2] + numbers[3]
                })

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
                if re.match(r"^(EnglishFollowup)_[0-9]*(\.txt)$", file, flags=0) != None:
                    self.resFileList.append(cur_path)

    def append_word(self, file_path, file_input_path_list, map_file):
        # 1、获取文件夹下的所有文件
        for file_input_path in file_input_path_list:
            self.findFiles(file_input_path)
        pattern = re.compile(r'\d+')
        self.book_num_map(map_file)
        # 2、获取已经去重好的单词列表并返回已经存在的单词数量
        exist_count = (self.read_single_words(file_path) + 1)
        # 3、读取txt
        for file in self.resFileList:
            bookNum = pattern.findall(file)[-1]
            code = ""
            for bookObj in self.resMapList:
                if bookNum == bookObj["bookNum"]:
                    code = bookObj["code"]
            self.readFile(file, code)
        res = ""

        for index in range(len(self.resList) - exist_count):
            if '\n' not in self.resChineseList[index]:
                self.resChineseList[index] = self.resChineseList[index] + "\n"
            res += str(index + exist_count) + "\t" + self.resCodeList[index] + "\t" + self.resList[
                index + exist_count] + "\t" + \
                   self.resChineseList[index]

        # 3、输出txt
        self.append_file(file_path)

    # 获取已经去重的单词并返回最后一个单词序号
    def read_single_words(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            index = 0
            for line in f:
                if len(line) > 0:
                    index = line[0]
                    word = line[2]
                    self.resList.append(word)
            f.close()
            return index

    # 文件追加
    def append_file(self, file_path, append_content):
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(append_content)
            f.close()


wordUtil = WordUtil()

# if __name__ == '__main__':
#     # 创建对象
#     wordUtil = WordUtil()
#     # 调用方法
#     wordUtil.wordClearRepeat()
#     wordUtil.findFiles("./resource")
