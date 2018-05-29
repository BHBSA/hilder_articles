import yaml
import pika
import requests
from readability.readability import Document
from article import Article
import json
from lxml import etree
import datetime
import re
from  article_img.image_replace import ImageReplace
from proxy_connection import Proxy_contact
from multiprocessing import Process
from gevent import monkey
import gevent
import random
from lib.log import LogHandler

log = LogHandler("wangyi")
setting = yaml.load(open('config_local.yaml'))

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36",
}

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

class WangyiConsumer:

    def consume_connect(self):
        connect = pika.BlockingConnection(pika.ConnectionParameters(host=setting['rabbitmq_host'],
                                                                    port=setting['rabbitmq_port'],heartbeat=10))
        self.channel = connect.channel()
        self.channel.queue_declare(queue='wangyi_article', durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback,
                              queue='wangyi_article',
                              no_ack=False)
    def start_consume(self):
        disconnected = True
        while disconnected:
            try:
                disconnected = False
                self.channel.start_consuming()
            except Exception as e:
                log.error(e)
                disconnected = True
                self.consume_connect()

    def callback(self, ch, method, properties, body):
        bod = json.loads(body.decode())
        article = Article(bod['source'])
        article.dict_to_attr(bod)
        url = article.url

        while True:
            try:
                res = requests.get(url=url, headers=headers, proxies=proxies[random.randint(0, 9)])
                res.encoding ='gbk'
                con = res.text
                break
            except Exception as e:
                log.error('网络请求错误')
        try:
            article_ready = self.html_parse(con, bod)
        except Exception as e:
            log.error(e)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        ch.basic_ack(delivery_tag=method.delivery_tag)
        article_ready.insert_db()
        log.info('消费一篇文章')

    def html_parse(self, con, bod):
        html = etree.HTML(con)
        title = re.search('<h1>(.*?)</h1>',con).group(1)
        post_time = re.search('post_time_source">(.*?)　来源',con,re.S|re.M).group(1)
        source_detail = re.search('来源:.*?>(.*?)</',con).group(1)
        try:
            author = re.search('作者：(.*?)</',con).group(1)
        except:
            author = None
        news_html = html.xpath("//div[@class='post_text']")[0]
        readable_article = etree.tounicode(news_html)

        img_change = ImageReplace()
        readable_article = img_change.image_download(readable_article)
        article = Article(bod['source'])
        article.dict_to_attr(bod)
        article.title = title
        article.post_time = post_time
        article.source_detail = source_detail
        article.body = readable_article
        article.author = author
        article.crawler_time = datetime.datetime.now()
        return article
