import configparser
import os
from script.utils.utilsword import utilsWord


class FileFinder(configparser.ConfigParser):
    """定义一个读取配置文件的类"""

    def __init__(self, defaults=None):
        self.result = []

    # 将查询结果直接输出
    def find_file(self, path, filename):
        self.max_file_size = 0
        self.sortList = []

        editionList = os.listdir(path)
        for editionName in editionList:
            booksPath = path + editionName
            booksList = os.listdir(booksPath)
            for bookName in booksList:
                book_word_path = path + editionName + "/" + bookName + "/Words/"
                if not os.path.isdir(book_word_path): continue

                item = self.find_file_from_book(filename, book_word_path)
                if item: self.sortList.append(item)

        if len(self.sortList) == 0: return
        # print("sortList", self.sortList)
        list_by_szie = sorted(self.sortList, key=lambda r: r['size'])
        # print("sortList[0]['filepath']", sortL, list_by_szie[0]['filepath'])
        return list_by_szie[0]['filepath']

    # 将查询结果直接输出
    def find_file_from_book(self, filename, book_word_path):

        for root, lists, files in os.walk(book_word_path):
            for file in files:
                strfile = file[:-4]
                strfilename = utilsWord.filter_punctuation(filename).strip().lower()
                strfile = utilsWord.filter_punctuation(strfile).strip().lower()
                # print("filename",filename, strfilename,  strfile, (strfilename == strfile))
                if strfilename == strfile:
                    filepath = os.path.join(root, file)
                    # print("strfilename == strfile", strfilename, strfile, filepath)
                    fsize = int(os.path.getsize(filepath))
                    item = {"size": fsize, "filepath": filepath}
                    return item

    # 将查询结果直接输出
    def find_all_file(self, path, filename):
        i = 0
        for root, lists, files in os.walk(path):
            for file in files:
                if filename in file:
                    i = i + 1
                    write = os.path.join(root, file)
                    print('%d %s' % (i, write))
                    self.result.append(write)
        return self.result


pFFinder = FileFinder()
