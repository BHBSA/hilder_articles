from article_list_page.page_url_config import page_list
from lib.bloom_filter import BloomFilter
from lib.log import LogHandler
from lib.rabbitmq import Rabbit
from pymongo import MongoClient
from article import Article
from lxml import etree
import requests
import json

m = MongoClient(host='192.168.0.235', port=27017)
collection = m['test']['list_config']
log = LogHandler(__name__)
bf = BloomFilter()
r = Rabbit('192.168.0.192', 5673)


class CrawlerArticleListUrl:
    def __init__(self):
        self.url_list = page_list

    def crawler_url(self):
        for source_dict in collection.find():
            html = requests.get(source_dict['url'])
            self.new_article(html.content.decode(html.encoding), source_dict)

    def new_article(self, html, source):
        if source['analyzer_rule'] == 'xpath':
            page = etree.HTML(html)
            for single_article in page.xpath(source['single_article_rule']):
                title = single_article.xpath(source['title'])
                detail_url = single_article.xpath(source['detail_url'])
                detail  =  single_article.xpath(None)
