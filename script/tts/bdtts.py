from aip import AipSpeech


class BaiduTTS:
    def __init__(self):
 
        self.appid = "23111070" #申请的账号
        self.appkey = "gmGBUNzsIirvFUwReBLecP0Y" #申请的账号
        self.secretkey = 'fDdV49H3K6cS1KCZT3YBjiqQDKDtfNzM'  #账号密码
        self.client = AipSpeech(self.appid, self.appkey, self.secretkey)
        
    def write_file(self, file_path, result):
        with open(file_path + ".mp3","wb") as f:
            f.write(result)

    def tts(self, txt, file_path):
        print("tts", file_path, txt)
        param = { "vol": 9, "spd": 4, "pit": 5, "per": 1 }
 
        result = self.client.synthesis(txt,'en','1', param)
        #result = self.client.synthesis(txt,'zh', 1, param)
        if not isinstance(result, dict):
            self.write_file(file_path + ".mp3", result)
        else:
            print(result)
          
bdTTSApi = BaiduTTS()

