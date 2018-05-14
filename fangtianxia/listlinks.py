#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/5/11 10:15
# @Author  : Alex
# @Email   : zhangjinxiao@fangjia.com
# @File    : listlinks.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
from fangtian.articletwo import Get_Article2
from fangtian.articleone import Get_Article1
import time

#列表页链接
def Getlinks(url):
    try:
        page = 0
        while page >= 0:
        #url = 'http://news.hengyang.fang.com/gdxw/2018-5-11/'+str(page)+'.html'
        #url = 'http://news.sh.fang.com/gdxw/2018-5-11/'+str(page)+'.html'
            page = page + 1
            time1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            url1 = url.replace('.html', '') + '/' + time1 + '/' + str(page) + '.html'
            headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive'
                    }
            response = requests.get(url=url1, headers=headers)

            response.encoding = 'GBK'
            soup = BeautifulSoup(response.text,'lxml')

            links1 = soup.select('.infoBox-txt > h3 > a')
            for i1 in links1:
                link1 = i1.get('href')
                if 'open' in link1:
                    print(Get_Article2(link1))        #调用方法，获取字段
                elif 'open' not in link1:
                    print(Get_Article1(link1))
                else:
                    return None
            links2 = soup.select('.infoBox-item > h3 > a')
            for i2 in links2:
                link2 = i2.get('href')
                if 'open' in link2:
                    print(Get_Article2(link2))
                elif 'open' not in link2:
                    print(Get_Article1(link2))
                else:
                    return None

            # #构造新的URL 自动进入下一页
            # page = 1
            # time1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            # newurl = url.replace(".html", '/') + time1 + '/' + str(page) + '.html'
            # Getlinks(newurl)
            # while newurl:
            #     page = page + 1
            #     newurl = newurl.strip(time1).strip('/')
            #     Getlinks(newurl)
            # else:
            #     return None
    except Exception as e:
        print(e)

# url = 'http://news.cs.fang.com/gdxw.html'
# Getlinks(url)
# page = 1
# while page >= 1:
#     page = page+1
#     Getlinks(page)


# def GetNextpage(url):
#     #url = 'http://news.sh.fang.com/gdxw/2018-5-11/1.html'
#     headers = {
#             'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#             'Accept-Encoding': 'gzip, deflate',
#             'Accept-Language': 'zh-CN,zh;q=0.9',
#             'Cache-Control': 'max-age=0',
#             'Connection': 'keep-alive'
#             }
#     response = requests.get(url=url, headers=headers)
#
#     response.encoding = 'GBK'
#     soup = BeautifulSoup(response.text,'lxml')
#     links = soup.find_all('a',href = re.compile('http://news.(\w+).fang.com/gdxw/(\d+)?.*'))
#     for i in links:
#         link = i.get('href')
#         Getlinks(link)
#         # GetNextpage(link)
# url = 'http://news.sh.fang.com/gdxw.html'
# GetNextpage(url)





