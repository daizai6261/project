import urllib.request
import urllib.parse
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalimt.request.v20181012 import TranslateRequest
from aliyunsdkcore.request import CommonRequest


import sys
import uuid
import requests
import hashlib
import time
from imp import reload
#reload(sys)


class YdTrans:
    def __init__(self, fromLang, toLang):
        self.APP_KEY = '3940f026d776b3e7'
        self.APP_SECRET = 'AyzsN8uRqOMEBAt2bd2seSjpbEyXSfVH'
        self.fromlang = fromLang
        self.tolang = toLang

    def httptrans(self, text):
        # 翻译地址
        request_url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        # data参数
        data = {'i': text,
                'from': 'AUTO',
                'to': 'AUTO',
                'smartresult': 'dict',
                'client': 'fanyideskweb',
                'salt': '15944508027607',
                'sign': '598c09b218f668874be4524f19e0be37',
                'ts': '1594450802760',
                'bv': '02a6ad4308a3443b3732d855273259bf',
                'doctype': 'json',
                'version': '2.1',
                'keyfrom': 'fanyi.web',
                'action': 'FY_BY_REALTlME',
                }
        # headers参数
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        data = urllib.parse.urlencode(data)
        data = bytes(data, 'utf-8')
        request = urllib.request.Request(request_url, data, headers=headers)

        #try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        print('翻译html：', html)
        html = json.loads(html)

        translateResult = html['translateResult'][0]
        chinese = ""
        for i in range(0, len(translateResult)):
            print('translateResult：', translateResult[i]['tgt'])
            chinese = chinese + translateResult[i]['tgt']
        print('翻译chinese：', chinese)
        return  True, chinese
       # except Exception as e:
           # return False , e

    def encrypt(self, signStr):
        hash_algorithm = hashlib.sha256()
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()


    def truncate(self, q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]


    def do_request(self, data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        YOUDAO_URL = 'https://openapi.youdao.com/api'
        return requests.post(YOUDAO_URL, data=data, headers=headers)


    def trans(self, text):
        data = {}
        data['from'] = self.fromlang
        data['to'] = self.tolang
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(text) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = self.APP_KEY
        data['q'] = text
        data['salt'] = salt
        data['sign'] = sign
        #data['vocabId'] = "您的用户词表ID"

        response = self.do_request(data)
        result = json.loads(response.content)

        chinese = ""
        if result['errorCode'] == "0" :
            chinese = result['translation'][0]
            return  True, chinese
        else :
            return  False, chinese


ydTransApi = YdTrans('en','zh-CHS')