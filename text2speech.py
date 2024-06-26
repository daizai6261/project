#!C:\pythonCode
# -*- coding: utf-8 -*-
# @Time : 2023-06-16 20:43
# @Author : 陈德宏
# @File : text2speech.py
# @Python: 3.7.7
# @Software: PyCharm 2024.1.3
import os

from script.base.configer import configer
from script.tts.alyttsV2 import AlyTTS
from script.utils.utils import utils
import shutil


def get_file_from_folder(folder_path):
    """从文件夹中获取需要的txt文件
    :param folder_path: 文件夹路径
    :return: txt文件路径列表
    """
    txt_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.txt')]
    return txt_files


def read_file(txt_path, start_line=1):
    """读取文件夹中需要的txt文件
    :param txt_path: txt文件路径
    :param start_line: 从第几行开始读取内容
    :return: 文件内容，每行作为一个元素的列表
    """
    with open(txt_path, 'r', encoding='utf-8') as f:
        lines = [line.rstrip('\n') for line in f.readlines()[start_line - 1:]]
    return lines


def get_text_needed(line, file_name_index=0, word_contents_ranges=None):
    """处理单行文本
    :param line: 文件中的单行文本
    :param file_name_index: 文件名字段的下标
    :param word_contents_ranges: 需要生成音频的字段下标范围
    :return: 文件名和处理后的文本内容
    """
    if word_contents_ranges is None:
        word_contents_ranges = [(1,)]
    line_contents = line.strip().split("\t")
    try:
        file_name = line_contents[file_name_index]
        word_contents_list = []
        for word_range in word_contents_ranges:
            start, end = word_range
            word_contents_list.extend(line_contents[start:end + 1])
        word_contents = " ".join(word_contents_list)
        return file_name, word_contents
    except IndexError:
        raise ValueError(f"Invalid line format: {line}")


def call_api(word_contents, out_put_path, file_name):
    """调用文字转语音API
    :param word_contents: 需要转换为语音的文本内容
    :param out_put_path: 输出路径
    :param file_name: 输出文件名
    """
    speaker_en = configer.program_param("CURRENT_SPEAKER_EN")
    long_text_speaker_en = configer.program_param("LONG_TEXT_SPEAKER_EN")
    altts_en = AlyTTS(speaker_en, long_text_speaker_en)
    altts_en.tts(word_contents, os.path.join(out_put_path, file_name))


def audio_to_folder(input_folder_path, out_put_path, start_line=1, file_name_index=0, word_contents_ranges=None):
    """调用之前的函数，将音频按照文件名生成到对应的子文件夹中
    :param input_folder_path: 输入文件夹路径，包含txt文件
    :param out_put_path: 输出文件夹路径
    :param start_line: 从第几行开始读取内容
    :param file_name_index: 文件名字段的下标
    :param word_contents_ranges: 需要生成音频的字段下标范围
    """
    if word_contents_ranges is None:
        word_contents_ranges = [(1,)]
    if not os.path.exists(out_put_path):
        utils.mkdir(out_put_path)
    else:
        raise ValueError(f"输出目标文件夹 {out_put_path} 已存在，请检查")

    txt_files = get_file_from_folder(input_folder_path)

    for txt_file in txt_files:
        base_name = os.path.splitext(os.path.basename(txt_file))[0]
        sub_dir_path = os.path.join(out_put_path, base_name)

        if not os.path.exists(sub_dir_path):
            utils.mkdir(sub_dir_path)

        lines = read_file(txt_file, start_line)
        for line in lines:
            try:
                file_name, word_contents = get_text_needed(line, file_name_index, word_contents_ranges)
                call_api(word_contents, sub_dir_path, file_name)
            except ValueError as e:
                print(f"Skipping line due to error: {e}")


def txt_to_speech(txt_file_path, out_put_path, start_line=1, file_name_index=0, word_contents_ranges=None):
    """将单个txt文件的内容转换为音频并保存到指定的文件夹中
    :param txt_file_path: 单个txt文件路径
    :param out_put_path: 输出文件夹路径
    :param start_line: 从第几行开始读取内容，从1开始
    :param file_name_index: 文件名字段的下标，从0开始
    :param word_contents_ranges: 需要生成音频的字段下标范围，从0开始
    """
    if word_contents_ranges is None:
        word_contents_ranges = [(1,)]
    if not os.path.exists(out_put_path):
        utils.mkdir(out_put_path)
    else:
        raise ValueError(f"输出目标文件夹 {out_put_path} 已存在，请检查")

    base_name = os.path.splitext(os.path.basename(txt_file_path))[0]
    sub_dir_path = os.path.join(out_put_path, base_name)
    if not os.path.exists(sub_dir_path):
        utils.mkdir(sub_dir_path)

    lines = read_file(txt_file_path, start_line)
    for line in lines:
        try:
            file_name, word_contents = get_text_needed(line, file_name_index, word_contents_ranges)
            call_api(word_contents, out_put_path, file_name)
        except ValueError as e:
            print(f"Skipping line due to error: {e}")


def explain_text_to_audio(txt_file_path, out_put_path, start_line=1, file_name_index=0, word_contents_ranges=None):
    """将单个解释txt文件的内容转换为音频并保存到指定的文件夹中
    :param txt_file_path: 单个txt文件路径
    :param out_put_path: 输出文件夹路径
    :param start_line: 从第几行开始读取内容，从1开始
    :param file_name_index: 文件名字段的下标，从0开始
    :param word_contents_ranges: 需要生成音频的字段下标范围，从0开始
    """
    if word_contents_ranges is None:
        word_contents_ranges = [(1,)]
    if not os.path.exists(out_put_path):
        os.makedirs(out_put_path)
    else:
        for filename in os.listdir(out_put_path):
            file_path = os.path.join(out_put_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                raise ValueError(f"删除文件 {file_path} 失败: {e}")

    base_name = os.path.splitext(os.path.basename(txt_file_path))[0]
    sub_dir_path = os.path.join(out_put_path, base_name)
    if not os.path.exists(sub_dir_path):
        os.makedirs(sub_dir_path)

    lines = read_file(txt_file_path, start_line)
    for line in lines:
        try:
            file_name, word_contents = get_text_needed(line, file_name_index, word_contents_ranges)
            unit_number = file_name.split('_')[0]
            unit_dir_path = os.path.join(str(sub_dir_path), unit_number)
            if not os.path.exists(unit_dir_path):
                os.makedirs(unit_dir_path)

            audio_file_name = '_'.join(file_name.split('_')[0:])

            call_api(word_contents, unit_dir_path, audio_file_name)
            print(f"生成音频文件 '{audio_file_name}' 并保存到 '{unit_dir_path}'")

        except ValueError as e:
            print(f"Skipping line due to error: {e}")


def add_prefix_by_postfix(prefix: str, postfix: str, folder_path: str):
    """根据后缀名为文件夹中的文件命名添加前缀名（递归处理子文件夹）
    Params:
        prefix: 需要添加的前缀
        postfix: 需要添加前缀的文件的后缀名，如：.mp3
        folder_path: 需要执行此操作的文件夹路径
    Example usage:
        add_prefix_by_postfix('explain_', '.mp3', '/path/to/folder')
    """
    if not os.path.isdir(folder_path):
        print(f"文件夹路径 '{folder_path}' 不存在，无法为文件名添加前缀")
        return

    for root, _, files in os.walk(folder_path):
        for filename in files:
            if filename.endswith(postfix):
                old_file_path = os.path.join(root, filename)
                new_filename = prefix + filename
                new_file_path = os.path.join(root, new_filename)
                os.rename(old_file_path, new_file_path)
                print(f"重命名 '{filename}' 为 '{new_filename}'")

# Example usage:
# add_prefix_by_postfix('explain_', '.mp3', '/path/to/folder')


if __name__ == '__main__':
    PROJECT_PATH = configer.run_param("PROJECT_PATH")
    OUT_PATH = PROJECT_PATH + "dest/output/"
    # 调用方法参考函数doc
    # 提供两种方法，第一种是将文件夹中所有txt文件按照相同处理方式输出，第二种是处理单个txt文件

    audio_to_folder(input_folder_path=r"D:\Workship\Pelbs\Books\教材\小学英语\人教小学英语\PEP\book16\osd_configs",
                    out_put_path=OUT_PATH, start_line=3, file_name_index=0, word_contents_ranges=[(1, 2)])

    txt_to_speech(r'D:\Workship\Pelbs\Books\教材\小学英语\人教小学英语\PEP\book16\osd_configs\Analys_16.txt',
                  OUT_PATH, start_line=3, file_name_index=0,
                  word_contents_ranges=[(1, 2)])
