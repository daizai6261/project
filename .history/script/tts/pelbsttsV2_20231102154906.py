# 音频生成
import os
import re
import time
import math
import shutil
from script.utils.utils import utils
from pydub import AudioSegment
from pydub.silence import split_on_silence
from script.base.configer import configer
from script.utils.utilsfile import utilsFile
from script.contentmgr import contentMgr
from script.base.filefinder import pFFinder

# from script.tts.bdtts import bdTTSApi
from script.tts.alyttsV2 import AlyTTS


class PelbsTTS:
    def __init__(self):
        self.cur_audio_path = ""

    def txt2audio(self):

        self.tts()
        #self.optimize_audio()
        self.copy_res_word()

    def tts(self):
        temp_sound_path = utilsFile.get("temp_sound_path")
        utils.recreate_folder(temp_sound_path)

        osd_all_audio_file = utilsFile.get("osd_all_audio_file")
        tts_idx_path = utilsFile.get("tts_idx_path")

        fdata = open(tts_idx_path, "r+", encoding="utf-8")
        fpage_txt = open(osd_all_audio_file, 'r', encoding="utf-8")

        cur_idx = fdata.readline()
        if not cur_idx: cur_idx = 1
        for num, line in enumerate(fpage_txt):
            if (num > 1) & (num > int(cur_idx)):
                # time.sleep(1)
                line_content = line.split("\t")

                sound_file = line_content[0]
                englishWord = line_content[1]
                chineseWord = line_content[2]
                unit_folder = sound_file.split("_")[0]
                # 生成语音
                sound_path_en = temp_sound_path + unit_folder + "/" + sound_file 
                sound_path_ch = temp_sound_path + unit_folder + "/" + sound_file+ "_cn"
                utils.mkdir(temp_sound_path + unit_folder)
                print("txt2audio", sound_path_en)
                #print("txt2audio", sound_path_ch)

                speaker_en = configer.program_param("CURRENT_SPEAKER_EN")
                speaker_ch = configer.program_param("CURRENT_SPEAKER_CN")
                long_text_speaker_en = configer.program_param("LONG_TEXT_SPEAKER_EN")
                long_text_speaker_ch = configer.program_param("LONG_TEXT_SPEAKER_CN")

                altts_en = AlyTTS(speaker_en, long_text_speaker_en)
                altts_ch = AlyTTS(speaker_ch, long_text_speaker_ch)
                altts_en.tts(englishWord, sound_path_en)
                altts_ch.tts(chineseWord, sound_path_ch)
                # bdTTSApi.tts(englishWord, sound_path)

    # 音频切割
    def optimize_audio(self):
        temp_sound_path = utilsFile.get("temp_sound_path")
        self.temp_split_path = temp_sound_path + "split_audios/"
        unitList = os.listdir(temp_sound_path)
        for unit in unitList:
            if unit == "split_audios": continue
            unit_type = contentMgr.get_unit_type(unit)
            if contentMgr.get_audio_split_type(unit_type) == "NOT_SPLIT": continue
            unit_folder_path = temp_sound_path + unit
            self.split_folder_audios(unit_folder_path)

        utils.delete_folder(temp_sound_path + "split_audios/")

    def split_folder_audios(self, unit_folder_path):
        fileList = os.listdir(unit_folder_path)
        for item_name in fileList:
            temp_sound_path = utilsFile.get("temp_sound_path")
            unit, page = utils.split_file_name(item_name)
            temp_audio_file = temp_sound_path + "/" + unit + "/" + item_name

            if utils.is_meta(temp_audio_file): continue
            if not re.match("page", page): continue

            print("optimize audio ", temp_audio_file)
            self.split_audio(unit, item_name)

    def split_audio(self, unit_name, item_name):
        utils.delete_folder(self.temp_split_path)
        os.makedirs(self.temp_split_path)

        temp_sound_path = utilsFile.get("temp_sound_path")
        org_audio_file = temp_sound_path + unit_name + "/" + item_name
        tag_sound = AudioSegment.from_mp3(org_audio_file)  # 加载mp3音频

        speaker = configer.program_param("CURRENT_SPEAKER")
        slience = configer.speaker_slience(speaker)

        chunks = split_on_silence(tag_sound,
                                  min_silence_len=int(slience[0]),  # 静默超过x毫秒则拆分
                                  silence_thresh=int(slience[1]),  # 小于xdBFS以下的为静默
                                  keep_silence=200  # 为每个音频添加多少ms无声
                                  )

        if len(chunks) > 0:
            silence = AudioSegment.silent(duration=700, frame_rate=44100)
            adjust_chunks = []

            ''''''
            for chunk in chunks:
                temp = chunk + silence
                adjust_chunks.append(temp)

            for i, chunk in enumerate(adjust_chunks):
                export_format_path = self.temp_split_path + "chunk_page1_audio{0}.mp3"
                export_audio_name = export_format_path.format(i + 1)
                chunk.export(export_audio_name, format="mp3")
                self.boost_volume(export_audio_name)

            self.merge_all_audio(org_audio_file)

        else:
            self.boost_volume(org_audio_file)

    # 放大音量
    def boost_volume(self, file):
        song = AudioSegment.from_mp3(file)
        cur_db_num = utils.get_audio_db(file)

        average_volume = int(configer.program_param("AVERAGE_VOLUME"))

        louder_db_num = average_volume - cur_db_num
        louder_song = song + louder_db_num
        louder_song.export(file, format='mp3')

    # 拼合音频
    def merge_all_audio(self, org_audio_file):

        self.tag_audio_path = self.temp_split_path + "chunk_page1_audio1.mp3"
        audio_file_list = os.listdir(self.temp_split_path)
        sortFileList = utils.list_double_sort(audio_file_list, 2)

        for audio_file in sortFileList:
            file_path = self.temp_split_path + audio_file
            if self.tag_audio_path == file_path: continue
            self.merge_audio(self.tag_audio_path, file_path)

        os.remove(org_audio_file)
        os.rename(self.tag_audio_path, org_audio_file)

    def merge_audio(self, path1, path2):
        input_music_1 = AudioSegment.from_mp3(path1)
        input_music_2 = AudioSegment.from_mp3(path2)

        _music1_db = input_music_1.dBFS
        _music2_db = input_music_2.dBFS
        dbplus = _music1_db - _music2_db
        if dbplus < 0:
            input_music_1 += abs(dbplus)
        elif dbplus > 0:
            input_music_2 += abs(dbplus)

        output_music = input_music_1 + input_music_2

        os.remove(path1)
        output_music.export(path1, format="mp3")  # 前面是保存路径，后面是保存格式

    def copy_res_word(self):

        # res_sound_path = utilsFile.get("res_sound_path")
        temp_sound_path = utilsFile.get("temp_sound_path")
        dest_sound_path = utilsFile.get("dest_sound_path")
        dest_all_sound_path = utilsFile.get("dest_all_sound_path")
        osd_config_path = utilsFile.get("osd_config_path")
        dest_config_path = utilsFile.get("dest_config_path")

        utils.delete_folder(dest_sound_path)
        utils.delete_folder(dest_sound_en_path)

        unitList = os.listdir(temp_sound_path)
        for unit in unitList:
            res_floder_path = temp_sound_path + unit
            if utils.is_meta(res_floder_path): continue
            print("9", res_floder_path)
            fileList = os.listdir(res_floder_path)
            temp_unit_folder = temp_sound_path + unit + "/"
            if not os.path.exists(temp_unit_folder):
                utils.mkdir(temp_unit_folder)
            for item_name in fileList:
                unit_name, page_name = utils.split_file_name(item_name);
                res_sound_file = temp_sound_path + "/" + unit + "/" + item_name
                if utils.is_meta(res_sound_file): continue
                ispage = re.match("page", page_name)
                if not ispage:
                    print("copy word file :", res_sound_file)
                    shutil.copy(res_sound_file, temp_unit_folder)

        utils.mov_files(temp_sound_path, dest_all_sound_path)
        utils.copy_all_folder(temp_sound_path, dest_sound_path)
        utils.copy_all_folder(osd_config_path, dest_config_path)


pTTS = PelbsTTS()