# 图片处理

import os
import shutil
from PIL import Image

from script.utils.utils import utils
from script.utils.utilsfile import utilsFile
from script.base.configer import configer


class PicCompress:
    def create_book(self, restart):
        book_unit_file = utilsFile.get("book_unit_file")
        jpg_book_texture_path = utilsFile.get("jpg_book_texture_path")
        jpg_book_sound_path = utilsFile.get("jpg_book_sound_path")
        pdf_book_path = utilsFile.get("pdf_book_path")

        ls = os.listdir(pdf_book_path)
        self.sort_list = utils.list_single_sort(ls, "_")

        if restart:
            utils.recreate_folder(jpg_book_texture_path)
            utils.recreate_folder(jpg_book_sound_path)

        for num, line in enumerate(open(book_unit_file, 'r', encoding="utf-8")):
            if num < 2: continue
            unit_name = line.split("\t")[1]
            page_num = int(line.split("\t")[3])
            unit_dir_path = jpg_book_texture_path + unit_name + "/"
            utils.mkdir(unit_dir_path)
            print("unit_name", unit_name)
            self.rename_unit_texture(unit_name, page_num, unit_dir_path)
            # print( "rename_unit_texture ",  self.sort_list)

    def rename_unit_texture(self, unit_name, page_num, tag_dir):

        pdf_book_path = utilsFile.get("pdf_book_path")
        for idx in range(0, page_num):

            source_path = pdf_book_path + self.sort_list[idx]
            target_path = tag_dir + self.sort_list[idx]

            shutil.copyfile(source_path, target_path)
            new_path = tag_dir + unit_name + "_page" + str(idx + 1) + ".jpg"
            os.rename(target_path, new_path)
            os.remove(source_path)

            if idx == page_num - 1:
                for i in range(0, page_num):
                    self.sort_list.pop(0)

        self.compress_texture()

    def compress_texture(self):
        jpg_book_texture_path = utilsFile.get("jpg_book_texture_path")
        for unit_folder in os.listdir(jpg_book_texture_path):
            unit_path = jpg_book_texture_path + unit_folder + "/"
            fileList = os.listdir(unit_path)

            idx = 1
            for item_file in fileList:
                page_name = "page" + str(idx)
                idx = idx + 1
                new_file_name = unit_folder + "_" + page_name + ".jpg"

                self.resize_image(unit_path + item_file)
                self.compress_image(unit_path + item_file)

    # 获取图片文件的大小:KB
    def get_size(self, file):
        size = os.path.getsize(file)
        return size / 1024

    # 压缩文件到指定大小，我期望的是150KB,step和quality可以修改到最合适的数值
    def compress_image(self, infile, step=10, quality=80):
        """不改变图片尺寸压缩到指定大小
        :param infile: 压缩源文件
        :param mb: 压缩目标，KB
        :param step: 每次调整的压缩比率
        :param quality: 初始压缩比率
        :return: 压缩文件地址，压缩文件大小
        """

        mb = int(configer.program_param("COMPRESS_MB"))
        o_size = self.get_size(infile)
        if o_size <= mb:
            return infile
        while o_size > mb:
            im = Image.open(infile)
            # 出现 OSError: cannot write mode RGBA as JPEG 错误时加入下方语句
            # im = im.convert("RGB")
            im.save(infile, quality=quality)
            if quality - step < 0:
                break
            quality -= step
            o_size = self.get_size(infile)
        return infile

    # 修改图片尺寸，如果同时有修改尺寸和大小的需要，可以先修改尺寸，再压缩大小
    def resize_image(self, infile, x_s=1080):
        """修改图片尺寸
        :param infile: 图片源文件
        :param x_s: 设置的宽度
        """
        im = Image.open(infile)
        x, y = im.size
        y_s = int(y * x_s / x)
        out = im.resize((x_s, y_s), Image.ANTIALIAS)
        out.save(infile)


picCompress = PicCompress()
