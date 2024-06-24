from aip import AipOcr


class BaiduORC:
    def __init__(self):
        '''
        self.appid = "14544448" #申请的账号
        self.appkey = "yRZGUXAlCd0c9vQj1kAjBEfY" #申请的账号
        self.secretkey = 'sc0DKGy7wZ9MeWFGZnbscbRyoDB2IQlj'  #账号密码
       '''

        self.appid = "23136072"  # 申请的账号
        self.appkey = "UMe9pFFLeqR8QqzUmSCG7qsf"  # 申请的账号
        self.secretkey = '82aMneWmWLhjF6PuO8UbTNpIGK5KC9nu'  # 账号密码
        self.client = AipOcr(self.appid, self.appkey, self.secretkey)

    def orc_generate(self, image_path):
        with open(image_path, 'rb') as fp:
            image = fp.read()
            options = {}
            options["vertexes_location"] = "true"
            result = self.client.general(image)
            # result = self.client.accurate(image)
            format_res = self.format_result(result)
            return format_res

    def format_result(self, result):
        format_res = []
        for word in result['words_result']:
            format_item = {}
            format_item['Txt'] = word['words']
            format_item['Pos'] = word['location']
            format_item['Pos']['Top'] = word['location']['top']
            format_item['Pos']['Left'] = word['location']['left']
            format_item['Pos']['Width'] = word['location']['width']
            format_item['Pos']['Height'] = word['location']['height']
            format_res.append(format_item)
        return format_res


bdORCApi = BaiduORC()
