import requests
from bs4 import BeautifulSoup
import re


def getPhonetic(word):
    url = 'https://youdao.com/result?word=' + word + '&lang=en'
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'lxml')
    data2 = soup.select('.phone_con > .per-phone > .phonetic')
    res = []
    for i in data2:
        res.append(i.text.replace(" ", ""))
    return res


print(getPhonetic("That’s"))

pattern = re.compile(r'[=\s]+')
res1 = pattern.split("test=mm --")
print(res1)
