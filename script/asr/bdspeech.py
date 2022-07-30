import os
import re
from aip import AipSpeech



class BaiduSpeech:

    def __init__(self):
        APP_ID = '23111070'
        API_KEY = 'gmGBUNzsIirvFUwReBLecP0Y'
        SECRET_KEY = 'fDdV49H3K6cS1KCZT3YBjiqQDKDtfNzM'
        self.client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    # 语音识别
    def speech_result(self, pcmFilePath):
        # cuid    String  用户唯一标识，用来区分用户，填写机器 MAC 地址或 IMEI 码，长度为60以内
        # dev_pid String  语言类型(见下表), 默认1537(普通话 输入法模型)
        with open(pcmFilePath, 'rb') as fp:
            pcmFile = fp.read()
        result = self.client.asr(pcmFile, 'pcm', 16000, {'dev_pid': 1737 })
        # 如果err_msg字段为"success."表示识别成功, 直接从result字段中提取识别结果, 否则表示识别失败
        if result["err_msg"] == "success.": 
        
            return result["result"][0]
        else:
            print(result["err_msg"])
            return ""
