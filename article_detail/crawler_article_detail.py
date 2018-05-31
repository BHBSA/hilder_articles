from lib.rabbitmq import Rabbit
import requests
import re
from pymongo import MongoClient

m = MongoClient(host='192.168.0.235', port=27017)
collection = m['test']['detail_config']


class CrawlerDetail:
    def __init__(self):
        pass

    def consume_article_detail_url(self):
        # todo 从queue获取url , source
        url = 'test'
        source = 'test'

        html = requests.get(url)

        # todo 获取详情页的解析方式
        detail_config_dict = collection.find_one({'source': source})

        title = re.search(detail_config_dict['title'], html.text, re.S | re.M)
        body = re.search(detail_config_dict['body'], html.text, re.S | re.M)
        comment_count = re.search(detail_config_dict['comment_count'], html.text, re.S | re.M)
        like_count = re.search(detail_config_dict['like_count'], html.text, re.S | re.M)
        read_num = re.search(detail_config_dict['read_num'], html.text, re.S | re.M)
        author = re.search(detail_config_dict['author'], html.text, re.S | re.M)
        post_time = re.search(detail_config_dict['post_time'], html.text, re.S | re.M)
        tag = re.search(detail_config_dict['tag'], html.text, re.S | re.M)

        # todo 放入消息队列做正文清洗
