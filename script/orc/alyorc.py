import urllib.request
import urllib.parse
import json
import math
from viapi.fileutils import FileUtils
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkocr.request.v20191230.RecognizeCharacterRequest import RecognizeCharacterRequest
from script.base.configer import configer


# 本地图片


class AlyORC:
    def __init__(self):

        self.AccessKeyId = configer.program_param("ACCESS_KEY")
        self.AccessKeySecret = configer.program_param("ACCESS_KEY_1")

    def get_oss_url(self, path):
        file_utils = FileUtils(configer.program_param("ACCESS_KEY"), configer.program_param("ACCESS_KEY_1"))
        oss_url = file_utils.get_oss_url(path, "jpg", True)
        return oss_url

    def format_result(self, result):

        format_res = []
        for word in result['Data']['Results']:
            format_item = {}
            format_item['Txt'] = word['Text']
            format_item['Pos'] = {}

            Angle = word['TextRectangles']['Angle']

            top = word['TextRectangles']['Top']
            left = word['TextRectangles']['Left']
            width = word['TextRectangles']['Width']
            height = word['TextRectangles']['Height']

            if int(Angle) > -20:
                format_item['Pos']['Top'] = top
                format_item['Pos']['Left'] = left
                format_item['Pos']['Width'] = width
                format_item['Pos']['Height'] = height
            else:
                format_item['Pos']['Top'] = top + math.ceil((height - width) / 2)
                format_item['Pos']['Left'] = left - math.floor((height - width) / 2)
                format_item['Pos']['Width'] = height
                format_item['Pos']['Height'] = width
                # print("format_result ",format_item['Txt'], left, top, height, width, math.ceil( (height + width)/2), math.ceil((height - width)/2))
            format_res.append(format_item)

        return format_res

    def orc_generate(self, file_path):
        client = AcsClient(self.AccessKeyId, self.AccessKeySecret, "cn-shanghai")

        ulr = self.get_oss_url(file_path)
        request = RecognizeCharacterRequest()
        request.set_accept_format('json')

        request.set_MinHeight("10")
        request.set_OutputProbability("true")
        request.set_ImageURL(ulr)

        response = client.do_action_with_exception(request)
        strdata = response.decode('utf-8')
        jdata = json.loads(strdata)
        format_res = self.format_result(jdata)

        return format_res


alyORCApi = AlyORC()
