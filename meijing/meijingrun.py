#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2018/5/17 11:45
# @Author  : Alex
# @Email   : zhangjinxiao@fangjia.com
# @File    : meijingrun.py
# @Software: PyCharm

import requests
from bs4 import BeautifulSoup
from lib.bloom_filter import BloomFilter
from article import Article
from article_img.qiniu_fetch import qiniufetch
import yaml
import datetime
import re
import random
from article_img.image_replace import ImageReplace

setting = yaml.load(open('config_local.yaml'))
article = Article('每经')

class Meijing(object):
    def __init__(self):
        self.bf = BloomFilter(host=setting['redies_host'], port=setting['redis_port'], key='article_toutiao_test', blockNum=1, db=0,)

    def meijingstart(self):
        try:
            headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept - Encoding': 'gzip, deflate',
                        'Accept - Language': 'zh-CN,zh;q=0.9',
                        'Cache - Control': 'max-age=0',
                        'Connection': 'keep - alive',
                        'User - Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
                        'Upgrade - Insecure - Requests': '1',
                        'Host': 'www.nbd.com.cn',
                        }
            url = 'http://www.nbd.com.cn/fangchan'
            response = requests.get(url=url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')

            piece = soup.select('.m-columnnews-list')[0]
            eachpiece = piece.select('li')
            for i in eachpiece:
                    read_num = i.select('.f-source > span')[2].text.strip().strip('阅读')               #阅读量
                    link = i.select('.f-title')[0].get('href')                                          #链接
                    if self.bf.is_contains(link):
                        print('bloom_filter已经存在{}'.format(link))
                    else:
                        self.bf.insert(link)
                        print('bloom_filter不存在，插入新的url:{}'.format(link))
                        proxies = [{"http": "http://192.168.0.96:3234"},
                                   {"http": "http://192.168.0.93:3234"},
                                   {"http": "http://192.168.0.90:3234"},
                                   {"http": "http://192.168.0.94:3234"},
                                   {"http": "http://192.168.0.98:3234"},
                                   {"http": "http://192.168.0.99:3234"},
                                   {"http": "http://192.168.0.100:3234"},
                                   {"http": "http://192.168.0.101:3234"},
                                   {"http": "http://192.168.0.102:3234"},
                                   {"http": "http://192.168.0.103:3234"}, ]
                        headers = {
                            'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
                            'Accept - Encoding': 'gzip, deflate',
                            'Accept - Language': 'zh - CN, zh;q = 0.9',
                            'Cache - Control': 'max - age = 0',
                            'Connection': 'keep - alive'
                        }
                        response = requests.get(url=link, headers=headers, proxies=proxies[random.randint(0, 9)])
                        soup1 = BeautifulSoup(response.text, 'lxml')


                        title = soup1.select('.g-article-top > h1')[0].text.strip()
                        source = soup1.select('.source')[0].text.strip()
                        time = soup1.select('.time')[0].text.strip()
                        content = soup1.select('.g-articl-text')[0]
                        content = content.prettify()
                        img_replace = ImageReplace()
                        con = img_replace.image_download(content)
                        tag = soup1.select('.u-aticle-tag > span')
                        category = soup1.select('.u-column')[0].text
                        L = []
                        for j in tag:
                            tagList = j.text
                            L.append(tagList)

                        try:
                            desc = soup1.select('.g-article-abstract > p')[0].text
                            article.desc = desc
                            imglink = i.select('.u-columnnews-img > img')[0].get('data-aload')  # 图片链接
                            file_name = imglink
                            imglink = qiniufetch(imglink, file_name)
                            article.title_img = imglink
                        except:
                            article.desc = None
                            article.title_img = None
                        article.title = title
                        article.source_detail = source
                        article.post_time = time
                        article.body = con
                        article.tag = L
                        article.category = category
                        article.read_num = read_num
                        article.url = link
                        article.crawler_time = datetime.datetime.now()
                        article.insert_db()

            more = soup.select('#more')[0].get('href')
            return more
        except Exception as e:
            print(e)



    def more(self,url):
        headers = {
                'Accept':'*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript',
                'Accept-Encoding':'gzip, deflate',
                'Accept-Language':'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Host':'www.nbd.com.cn',
                'If-None-Match':'06df643755a61c9c13a31fb74d27437b',
                'Referer':'http://www.nbd.com.cn/fangchan',
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36',
                'X-CSRF-Token':'+qYhSliyi8ZV2tLBI+HES72WeuOwOkp1yIP6A+8SgLk=',
                'X-Requested-With':'XMLHttpRequest'
                }

        response = requests.get(url=url, headers=headers)
        info = response.text.replace(' ', '')
        link = re.search('href="(http://www\.nbd\.com\.cn/columns/298\?last_article=\d+&version_column=v5)', info).group(1)

        re_link = re.compile('(http://www\.nbd\.com\.cn/articles/\d+-\d+-\d+/\d+.html)')
        articlelink = re_link.findall(info)
        articlelinks = set(articlelink)

        re_imglink = re.compile('(http://image\.nbd\.com\.cn/uploads/articles/thumbnails/.*?\.jpg)')
        re_imglinks = re_imglink.findall(info)

        re_read = re.compile('(\d+?)阅读')
        re_reads = re_read.findall(info)

        for i,j,k in zip(articlelinks, re_imglinks, re_reads):
            if self.bf.is_contains(i):
                print('bloom_filter已经存在{}'.format(i))
            else:
                self.bf.insert(i)
                print('bloom_filter不存在，插入新的url:{}'.format(i))
                proxies = [{"http": "http://192.168.0.96:3234"},
                           {"http": "http://192.168.0.93:3234"},
                           {"http": "http://192.168.0.90:3234"},
                           {"http": "http://192.168.0.94:3234"},
                           {"http": "http://192.168.0.98:3234"},
                           {"http": "http://192.168.0.99:3234"},
                           {"http": "http://192.168.0.100:3234"},
                           {"http": "http://192.168.0.101:3234"},
                           {"http": "http://192.168.0.102:3234"},
                           {"http": "http://192.168.0.103:3234"}, ]
                headers = {
                    'Accept': 'text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, image / apng, * / *;q = 0.8',
                    'Accept - Encoding': 'gzip, deflate',
                    'Accept - Language': 'zh - CN, zh;q = 0.9',
                    'Cache - Control': 'max - age = 0',
                    'Connection': 'keep - alive'
                }
                response = requests.get(url=i, headers=headers, proxies=proxies[random.randint(0, 9)])
                soup = BeautifulSoup(response.text, 'lxml')

                title = soup.select('.g-article-top > h1')[0].text.strip()
                source = soup.select('.source')[0].text.strip()
                time = soup.select('.time')[0].text.strip()
                content = soup.select('.g-articl-text')[0]
                content = content.prettify()
                img_replace = ImageReplace()
                con = img_replace.image_download(content)
                tag = soup.select('.u-aticle-tag > span')
                category = soup.select('.u-column')[0].text
                L = []
                for a in tag:
                    tagList = a.text
                    L.append(tagList)
                try:
                    desc = soup.select('.g-article-abstract > p')[0].text
                    article.desc = desc
                    file_name = j
                    j = qiniufetch(j, file_name)
                    article.title_img = j
                except:
                    article.desc = None
                    article.title_img = None
                article.title = title
                article.source_detail = source
                article.post_time = time
                article.body = con
                article.tag = L
                article.category = category
                article.read_num = k
                article.url = i
                article.crawler_time = datetime.datetime.now()
                article.insert_db()

        return link


def start():
    meijing = Meijing()
    morelink = meijing.meijingstart()
    try:
        while True:
            link = meijing.more(morelink)
            meijing.more(link)
    except Exception as e:
        print(e)





