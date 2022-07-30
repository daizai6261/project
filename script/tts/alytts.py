import time
import re
import json
import random

import requests
import http.client
from script.utils.utils import utils
from script.utils.utilsword import utilsWord
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from script.base.configer import configer

import urllib
#import urllib.request


class AlyTTS:
    def __init__(self):
        self.speaker = configer.program_param("CURRENT_SPEAKER")
        self.long_text_speaker = configer.program_param("LONG_TEXT_SPEAKER")
        self.appkey = '92Ku216CcAT4IwHp'  
        self.token_expireTime = 1551513046
        self.access_token = 'dbf06e8481574a6ea9f2508a5160fe05'
        self.url = 'https://nls-gateway.cn-shanghai.aliyuncs.com/stream/v1/tts' #短文本合成地址

        self.special_word = [ ["Li Mei", "LeeMei"],  ["Andy's", "Andy is"], ["°C", " degree celsius"],["Hmm", "en"],["119", "One One Nine"],
        ["110", "One One Zero"],["120", "One Two Zero"],["122", "One Two Two"],["911", "Nine One One"],["Chang'e", "Chang er"],["Shh", "she"],["metres", "miters"],
         ["lives", "leafs"], ["who's", "whose"], ["Who's", "whose"], 
         
         #专有名词直接替换成中文发音
          ["jiaozi", "饺子"],["Bingmayong", "兵马俑"],["taijiquan", "太极拳"], ["erhu", "二胡"],["BeiHai", "北海"],[ "TianShan", "天山"], [ "TianChi", "天池"], [ "XinJiang", "新疆"], 
         ["Yinchuan", "银川"],  ["Nihao", "你好"], ["Luoyang", "洛阳"], ] 
    
    def set_speaker(self):
        speakerList = configer.program_param("CURRENT_SPEAKER_LIST")
        speaker_idx = 6
        while self.speaker != speakerList[speaker_idx]:
            speaker_idx = random.randint(0, len(speakerList))
            self.speaker = speakerList[speaker_idx]

    def tts(self, text, path):
        

        text = self.optimize_time_sound(text)
        text = self.replace_operational_sound(text) #优先处理
        text = self.optimize_full_stop(text)
        text = self.optimize_special_word_sound(text)
        text = text.lower()

        '''
        if utilsWord.is_contain_zh(text): 
            self.speaker = configer.program_param("CN_TEXT_SPEAKER")
            self.long_text_speaker = configer.program_param("LONG_CN_TEXT_SPEAKER")
        else : 
            self.speaker = configer.program_param("CURRENT_SPEAKER")
            self.long_text_speaker = configer.program_param("LONG_TEXT_SPEAKER")
        '''


        if len(text) < 250 : 
            self.short_tts(text, path) 
        else:
            self.long_tts(text, path)

    def short_tts(self, text, path):
        # 当前的时间戳 和 token有效期对比，如果过期则重新生成
        local_time = int(time.time())
        if local_time > self.token_expireTime:
            self.access_token, self.token_expireTime = self.get_token()

        
            
        headers = { "Content-Type": "application/json;charset=UTF-8", "X-NLS-Token":self.access_token, }
        audio_format = "mp3"
        data_info = {
            "appkey":self.appkey,
            "text":text,
            "token":self.access_token,
            "format":audio_format,
            #"sample_rate":"8000",  #音频采样率，默认是16000
            "volume":"100", #音量，范围是0~100，默认50
            "voice":self.speaker, #发言人，
            "speech_rate":"-350", #语速，范围是-500~500，默认是0 : lay: -400
            "pitch_rate":"0", #语调，范围是-500~500，默认是0
        }

        data = json.dumps(data_info)
        ret = requests.post(self.url, headers = headers, data = data, timeout = 20)
        #print("short_tts", text, ret)
        utils.write_file(path + "." + audio_format, ret.content)

    def long_tts(self, text, path):
        self.path = path
        local_time = int(time.time())
        if local_time > self.token_expireTime:
            self.access_token, self.token_expireTime = self.get_token()

        # 拼接HTTP Post请求的消息体内容。
        th = TtsHeader(self.appkey, self.access_token)
        tc = TtsContext("mydevice")
        tr = TtsRequest(self.long_text_speaker, 16000, "mp3", False, text, -500, 100)
        tp = TtsPayload(True, "http://134.com", tr)
        tb = TtsBody(th, tc, tp)
        body = json.dumps(tb, default = tb.tojson)
        self.requestLongTts4Post(str(body), self.appkey, self.access_token)

    # 长文本语音合成restful接口，支持post调用，不支持get请求。发出请求后，可以轮询状态或者等待服务端合成后自动回调（如果设置了回调参数）。
    def requestLongTts4Post(self, tts_body, appkey, token):
        host = 'nls-gateway.cn-shanghai.aliyuncs.com'
        url = 'https://' + host + '/rest/v1/tts/async'
        # 设置HTTP Headers
        http_headers = {'Content-Type': 'application/json'}
        conn = http.client.HTTPConnection(host)
        conn.request(method='POST', url=url, body=tts_body, headers=http_headers)
        response = conn.getresponse()
        body = response.read()
        if response.status == 200:
            jsonData = json.loads(body)
            task_id = jsonData['data']['task_id']
            request_id = jsonData['request_id']
            # 说明：轮询检查服务端的合成状态，轮询操作非必须。如果设置了回调url，则服务端会在合成完成后主动回调。
            self.waitLoop4Complete(url, appkey, token, task_id, request_id)
        else:
            print('The request failed: ' + str(body))

    # 根据特定信息轮询检查某个请求在服务端的合成状态，轮询操作非必须，如果设置了回调url，则服务端会在合成完成后主动回调。
    def waitLoop4Complete(self, url, appkey, token, task_id, request_id):
        fullUrl = url + "?appkey=" + appkey + "&task_id=" + task_id + "&token=" + token + "&request_id=" + request_id
        while True:
            req = urllib.request.Request(url=fullUrl)
            result = urllib.request.urlopen(req).read()
            jsonData = json.loads(result)

            if ("data" in jsonData) and ("audio_address" in jsonData["data"] and jsonData["data"]["audio_address"] != None):
                address = jsonData["data"]["audio_address"]
                response = requests.get(address)
                utils.write_file(self.path + ".mp3", response.content)
                break
            else:
                print("Tts Running...")
                time.sleep(2)
################################优化#############################################################
    #停顿优化
    def optimize_full_stop(self, line):     
        #先处理词语
        line = line.replace(",please", " please")       #please 不用停顿
        line = line.replace(",too", " too")       #please 不用停顿

        line = line.replace(",", ",  ")
        line = line.replace(".", ",   ")
        line = line.replace("。", ",   ")

        line = line.replace("?", ",   ")
    
        line = line.replace("!", ",   ")  #感叹号号替换
        line = line.replace("！", ",   ")  #中文感叹号替换
        line = line.replace("/", ",   ")  #分隔符号替换
        
        return line

    #时间读音
    def optimize_time_sound(self, line): 
        line = line.replace("：", ":")
        line = line.replace("a.m", "AM") 
        line = line.replace("p.m", "PM") 

        line = re.sub('\s+:', ':', line).strip()        
        line = re.sub(':\s+', ':', line).strip()
        list_pos = [i.start() for i in re.finditer(':', line)]
       
        for idx in list_pos:
            
            if idx < 1:continue
            if idx+ 1 >= len(line):continue
            
            first_num = line[idx - 1]
            second_num = line[idx + 1]
            if (not utilsWord.is_number(first_num)) or ( not utilsWord.is_number(second_num)):
                line = line[:idx] + "," + line[idx+1:]
        return line

    #运算符读音
    def replace_operational_sound(self, line): 
        symbol_list = [["+", " plus ", ],["-", "minus" ],  ["×", " times ", ], ["÷", " divided by ", ],[".", " point ", ],]
        for symbol in symbol_list:
            line = re.sub('\s+\\' + symbol[0], symbol[0], line).strip()
            line = re.sub('\\'+ symbol[0] + '\s+', symbol[0], line).strip()
            list_pos = [i.start() for i in re.finditer('\\'+ symbol[0], line)]

            operational_pos = []
            for idx in list_pos:
                if idx < 1:continue
                if idx+ 1 >= len(line):continue
                first_num = line[idx - 1]
                second_num = line[idx + 1]
                if ( utilsWord.is_number(first_num)) and (  utilsWord.is_number(second_num)):
                    operational_pos.append(idx)

            line = utilsWord.multi_replace(line, operational_pos, symbol[1])  

        return line

    #特殊词发音优化(名字)
    def optimize_special_word_sound(self, line): 
        for word in self.special_word:
            line = line.replace(word[0], word[1])  #替换api发音不正确的文字
        return line

    
    def get_token(self):
        # 创建AcsClient实例
        client = AcsClient('LTAI4G8pLKGSzgCT7RCfUMjW', "favuQgzb4zJGUHO2PBcLvTZ6vLTfnT", "cn-shanghai" )
        # 创建request，并设置参数
        request = CommonRequest()
        request.set_method('POST')
        request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
        request.set_version('2019-02-28')
        request.set_action_name('CreateToken')
        response = client.do_action_with_exception(request)
        token_result = eval(response.decode('utf-8'))
        
        return  token_result['Token']['Id'],  token_result['Token']['ExpireTime']
            

alyTTSApi = AlyTTS()

##################################################################################
class TtsHeader:
    def __init__(self, appkey, token):
        self.appkey = appkey
        self.token = token
    def tojson(self, e):
        return {'appkey': e.appkey, 'token': e.token}
        
class TtsContext:
    def __init__(self, device_id):
        self.device_id = device_id
    #将序列化函数定义到类中。
    def tojson(self, e):
        return {'device_id': e.device_id}

class TtsRequest:
    def __init__(self, voice, sample_rate, format, enable_subtitle, text, speech_rate, volume):
        self.voice = voice
        self.sample_rate = sample_rate
        self.format = format
        self.enable_subtitle = enable_subtitle
        self.text = text
        self.speech_rate = speech_rate
        self.volume = volume
        
    def tojson(self, e):
        return {'voice': e.voice, 'sample_rate': e.sample_rate, 'format': e.format, 'enable_subtitle': e.enable_subtitle, 'text': e.text, 'speech_rate' :e.speech_rate}

class TtsPayload:
    def __init__(self, enable_notify, notify_url, tts_request):
        self.enable_notify = enable_notify
        self.notify_url = notify_url
        self.tts_request = tts_request
    def tojson(self, e):
        return {'enable_notify': e.enable_notify, 'notify_url': e.notify_url, 'tts_request': e.tts_request.tojson(e.tts_request)}

class TtsBody:
    def __init__(self, tts_header, tts_context, tts_payload):
        self.tts_header = tts_header
        self.tts_context = tts_context
        self.tts_payload = tts_payload
    def tojson(self, e):
        return {'header': e.tts_header.tojson(e.tts_header), 'context': e.tts_context.tojson(e.tts_context), 'payload': e.tts_payload.tojson(e.tts_payload)}


