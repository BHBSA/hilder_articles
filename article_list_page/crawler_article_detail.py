from lib.rabbitmq import Rabbit
import requests
import re


class CrawlerDetail:
    def __init__(self):
        pass

    def consume_article_detail_url(self):
        # todo 从queue获取url
        html = requests.get('url')
        # todo 获取详情页的解析方式
        title = ''
        body = ''

