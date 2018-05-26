# -*- coding: utf-8 -*-
import requests
from urllib.parse import urlencode
import json
import re
from bs4 import BeautifulSoup
import pymongo
from config import *

client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print(result)
        return True
    return False

def get_page_index(offset,keyword):
    data={
            'offset':offset,
            'format':'json',
            'keyword':keyword,
            'autoload':'true',
            'count':'20',
            'cur_tab':3
            }
    url='http://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response=requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except Exception:
        return None
    
def get_page_detail(url):
    headers = {
            'User-Agent': 'User-Agent  Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN'
        }
    try:
        response=requests.get(url,headers=headers)
        if response.status_code==200:
            return response.text
        return None
    except Exception:
        return None
    
def parse_page_index(html):
    data=json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def parse_page_detail(html,url):
    soup=BeautifulSoup(html,'lxml')
    result = soup.select('title')
    title = result[0].get_text() if result else ''
    images_pattern = re.compile('gallery: JSON.parse\("(.*)"\)', re.S)
    result = re.search(images_pattern, html)
    if result:
        data = json.loads(result.group(1).replace('\\', ''))
        if data and 'sub_images' in data.keys():
            sub_images=data.get('sub_images')
            images=[item.get('url') for item in sub_images]
            return {
                    'title':title,
                    'url':url,
                    'images':images                    
                    }

def main():
    html=get_page_index(0,'街拍')
    for url in parse_page_index(html):
        html=get_page_detail(url)
       # print(html)
        if html:            
            result=parse_page_detail(html,url)
            if result:
                save_to_mongo(result)
    
if __name__ == '__main__':
    main()

