from lib.rabbitmq import Rabbit
import requests
import re
from pymongo import MongoClient
from lxml import etree

m = MongoClient(host='192.168.0.235', port=27017)
collection = m['test']['detail_config']


class CrawlerDetail:
    def __init__(self):
        pass

    def consume_article_detail_url(self):
        # todo 从queue获取url , source
        message = {"city": None, "author": None, "source": "\u7f51\u6613\u65b0\u95fb", "desc": None,
                   "organization_author": None, "body": None, "tag": None, "comment_count": None, "category": None,
                   "source_detail": None, "status": 0,
                   "title": "\u4e0a\u6d77\u4e94\u516d\u5341\u5e74\u4ee3\u53a8\u536b\u5408\u7528\u8001\u516c\u623f \u6539\u9020\u6210\u9ad8\u989c\u503c\u7535\u68af\u623f",
                   "title_img": None, "detail_url": "http://sh.house.163.com/18/0324/09/DDLDHQC90007871Q.html",
                   "read_num": None, "url": None, "crawler_time": None, "post_time": None, "like_count": None,
                   "article_id": None}

        html = requests.get(message['detail_url'])
        html.content.decode(html.encoding)
        page = etree.HTML(html)

        # 获取详情页的解析方式
        detail_config_dict = collection.find_one({'source': message['source']})

        if detail_config_dict['body'] is not None:
            message['body'] = page.xpath(detail_config_dict['body'])[0]
        if detail_config_dict['comment_count'] is not None:
            message['comment_count'] = page.xpath(detail_config_dict['comment_count'])[0]
        if detail_config_dict['like_count'] is not None:
            message['like_count'] = page.xpath(detail_config_dict['like_count'])[0]
        if detail_config_dict['read_num'] is not None:
            message['read_num'] = page.xpath(detail_config_dict['read_num'])[0]
        if detail_config_dict['author'] is not None:
            message['author'] = page.xpath(detail_config_dict['author'])[0]
        if detail_config_dict['post_time'] is not None:
            message['post_time'] = page.xpath(detail_config_dict['post_time'])[0]
        if detail_config_dict['tag'] is not None:
            message['tag'] = page.xpath(detail_config_dict['tag'])[0]

        # todo 放入消息队列做正文替换清洗