import yaml
import requests
from article import Article
import json
from lxml import etree
import datetime
import re
from  article_img.image_replace import ImageReplace
from proxy_connection import Proxy_contact
import random
import time
import pika
from lib.log import LogHandler

log = LogHandler("fenghuang")
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

class Consumer:

    def consume_connect(self):
        connect = pika.BlockingConnection(pika.ConnectionParameters(host=setting['rabbitmq_host'],
                                                                    port=setting['rabbitmq_port'],heartbeat=10))
        self.channel = connect.channel()
        self.channel.queue_declare(queue='fenghuang_article', durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.callback,
                              queue='fenghuang_article',
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


    def callback(self,ch, method, properties, body):
        bod = json.loads(body.decode())
        article = Article(bod['source'])
        article.dict_to_attr(bod)
        # print(article.dict_to_attr(body))
        url = article.url

        while True:
            try:
                res = requests.get(url=url, headers=headers, proxies=proxies[random.randint(0, 9)])
                con = res.content.decode()
                break
            except Exception as e:
                log.error('网络请求错误{}'.format(url))
        try:
            article_ready = self.html_parse(con, bod)
        except Exception as e:
            log.error(e)
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        ch.basic_ack(delivery_tag=method.delivery_tag)
        article_ready.insert_db()
        log.info('消费一篇文章')
        # article_web = Proxy_contact(app_name='fenghuang',method='get',url=url,headers=headers)
        # con = article_web.contact()
        # if con == False:
        #     ch.basic_ack(delivery_tag=method.delivery_tag)
        #     print('文章请求失败，跳过此文章！')
        # else:
        #     self.html_parse(con,bod)
        #     ch.basic_ack(delivery_tag=method.delivery_tag)

    def html_parse(self,con,bod):
        title = re.search('<div class="title">.*?<h2>(.*?)</h2',con,re.S|re.M).group(1)
        post_time = re.search('<div class="marb-5"><span>(.*?)</span>',con).group(1)
        source_detail = re.search('来源：(.*?)</span',con).group(1)
        readable_article = re.search('<div class="article">.*?</div>',con,re.S|re.M).group(0)

        img_change = ImageReplace()
        readable_article = img_change.image_download(readable_article)

        article = Article(bod['source'])
        article.dict_to_attr(bod)

        article.title = title
        article.post_time = post_time
        article.source_detail = source_detail
        article.body = readable_article
        article.crawler_time = datetime.datetime.now()
        return article
        # article.insert_db()
        # print('一篇文张入库成功')

