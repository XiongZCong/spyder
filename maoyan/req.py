# -*- coding: utf-8 -*-
import requests
import re
import json
from multiprocessing import Pool

#from requests.exceptions import RequestException

def get_on_page(url):
     headers = {
            'Host': 'maoyan.com',
            'User-Agent': 'User-Agent  Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN'
        }
     try:
         response = requests.get(url,headers=headers)
         if response.status_code==200:
             return response.text
         return None
     except Exception:
         return None
     
def writeToFile(content):
    with open("maoyan.txt",'a',encoding='utf-8') as f:
        f.write(json.dumps(content,ensure_ascii=False) + "\n")
        f.close()

def parse_one_page(html):
    pattern=re.compile('<dd>.*?board-index.*?>(\d*)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">'
                         +'(.*?)</p>.*?releasetime">(.*?)</p>'
                         +'.*?integer">(.*?)</i>.*?fraction">(.*?)</i></p>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    for item in items:
        print(item)
        yield {
            'index':item[0],
            'image':item[1],
            'title':item[2],
            'actor':item[3].strip()[4:],
            'time':item[4].strip()[5:],
            'score':item[5]+item[6]
        }
 
 
def main(offset):
     url='http://maoyan.com/board/4?offset='+str(offset)
     print(2)
     html=get_on_page(url)
     parse_one_page(html)
     for item in parse_one_page(html):
         print(item)
         writeToFile(item)

     
if __name__ == '__main__':
    print(1)
    pool = Pool()
    pool.map(main,[i*10 for i in range(10)])
#    for i in range(10):
#        main(i*10)

