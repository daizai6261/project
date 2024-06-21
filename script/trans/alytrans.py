
import json
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalimt.request.v20181012 import TranslateRequest
from aliyunsdkcore.request import CommonRequest

class AlyTrans:
    def __init__(self, fromLang, toLang):
        self.AccessKeyId = 'LTAI4G8pLKGSzgCT7RCfUMjW'
        self.AccessKeySecret = 'favuQgzb4zJGUHO2PBcLvTZ6vLTfnT'
        self.fromlang = fromLang
        self.tolang = toLang

    def trans(self, text):
        
        # 创建AcsClient实例
        client = AcsClient(
            self.AccessKeyId,  # 阿里云账号的AccessKey ID
            self.AccessKeySecret, # 阿里云账号Access Key Secret
            "cn-hangzhou"  # 地域ID
        )
        
        # 创建request，并设置参数
        request = TranslateRequest.TranslateRequest()
        request.set_SourceLanguage(self.fromlang) #源语言
        request.set_TargetLanguage(self.tolang)  #目标语言
        request.set_Scene("title")   #设置场景，商品标题:title，商品描述:description，商品沟通:communication
        request.set_SourceText(text)  #原文
        request.set_FormatType("text")  #翻译文本的格式
        request.set_method("POST")  
   
        ''''''
        try:
            response = client.do_action_with_exception(request)
            jsondata = json.loads(response)
            dst = jsondata["Data"]["Translated"]
            #print("AlyTrans Translated", dst)
            return  True , dst
        except Exception as e:
            return False , e

    

    def mttrans(self, text):

        # 创建AcsClient实例
        client = AcsClient(
            self.AccessKeyId,  # 阿里云账号的AccessKey ID
            self.AccessKeySecret, # 阿里云账号Access Key Secret
            "cn-hangzhou"  # 地域ID
        )

        request = CommonRequest()
        request.set_accept_format('json')
        request.set_domain('automl.cn-hangzhou.aliyuncs.com')
        request.set_method('POST')
        request.set_protocol_type('https') # https | http
        request.set_version('2019-11-11')
        request.set_action_name('PredictMTModel')

        request.add_query_param('RegionId', "cn-hangzhou")
        request.add_query_param('ModelId', "6809")
        request.add_query_param('Content', text)
        request.add_query_param('ModelVersion', "V1")

        response = client.do_action(request)
        # python2:  print(response) 
       # print(str(response, encoding = 'utf-8'))

alyTransApi = AlyTrans('en','zh')