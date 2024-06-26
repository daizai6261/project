import requests


def getPhonetics(word):
    url = f'https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}'
    response = requests.get(url)
    try:
        UK = ''
        US = ''
        res = response.json()
        for phonetics in response.json():
            if ("phonetic" in phonetics):
                for phonetic in phonetics["phonetics"]:
                    if "audio" in phonetic or len(phonetic["audio"]) >= 0:
                        if 'uk' in phonetic["audio"] and phonetic["text"] != "":
                            UK = phonetic["text"]
                        elif 'us' in phonetic["audio"] and phonetic["text"] != "":
                            US = phonetic["text"]
                        else:
                            US = phonetic["text"]
                if UK == '' and US != '':
                    UK = US
                if US == '' and UK != '':
                    US = UK
                return [US, UK]
    except:
        print("没有音标")
        return ['', '']


print(getPhonetics("none"))
