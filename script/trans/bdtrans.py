import json
import random
import hashlib
from urllib import parse
import http.client


class BaiduTranslate:
    def __init__(self, fromLang, toLang):
        self.url = "/api/trans/vip/translate"
        self.appid = "20201208000641563"  # 申请的账号
        self.secretkey = 'i3TTFiIh63JOSrxyP0e8'  # 账号密码
        self.fromlang = fromLang
        self.tolang = toLang
        self.salt = random.randint(32768, 65536)

    def trans(self, text):
        sign = self.appid + text + str(self.salt) + self.secretkey
        md = hashlib.md5()
        md.update(sign.encode(encoding='utf-8'))
        sign = md.hexdigest()
        myurl = self.url + \
                '?appid=' + self.appid + \
                '&q=' + parse.quote(text) + \
                '&from=' + self.fromlang + \
                '&to=' + self.tolang + \
                '&salt=' + str(self.salt) + \
                '&sign=' + sign
        try:
            httpClient = http.client.HTTPConnection('api.fanyi.baidu.com')
            httpClient.request('GET', myurl)
            response = httpClient.getresponse()
            html = response.read().decode('utf-8')
            html = json.loads(html)
            dst = html["trans_result"][0]["dst"]
            return True, dst
        except Exception as e:
            return False, e


bdTransApi = BaiduTranslate('en', 'zh')
