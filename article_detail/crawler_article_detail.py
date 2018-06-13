import requests
from lxml import etree
from pymongo import MongoClient
from lib.rabbitmq import Rabbit
from lib.log import LogHandler
from lib.proxy_iterator import Proxy
import yaml
import json
import pika
import re


setting = yaml.load(open('config_local.yaml'))
log = LogHandler('article_consumer')
m = MongoClient(setting['mongo_235']['config_host'], setting['mongo_235']['port'])
collection = m[setting['mongo_235']['config_db']][setting['mongo_235']['coll_detail']]

rabbit = Rabbit(setting['rabbitmq_host'],setting['rabbitmq_port'])


class CrawlerDetail:
    def __init__(self):
        self.proxy = Proxy()

    def connect(self):
        self.connection = rabbit.connection
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='usual_article', durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.consume_article_detail_url,
                              queue='usual_article',
                              no_ack=False)

    def start_consume(self):
        disconnected = True
        while disconnected:
            try:
                disconnected = False
                self.channel.start_consuming()
            except Exception as e:
                disconnected = True
                self.connect()

    def clean(self,message):        #作者,发表时间,详细来源字段清洗
        clean_coll = m[setting['mongo_235']['config_db']][setting['mongo_235']['clean']]
        clean = clean_coll.find_one({'source': message['source']})
        if clean['post_time'] is not None:
            try:
                post_time = re.search(clean['post_time'],message['post_time']).group(1)
                message['post_time'] = post_time
            except:
                log.error("发表时间正则匹配失败{}".format(message['post_time']))
                message['post_time'] = None
        if clean['author'] is not None:
            try:
                author = re.search(clean['author'],message['author']).group(1)
                message['author'] = author
            except:
                log.error("作者正则匹配失败{}".format(message['author']))
                message['author'] = None

        if clean['source_detail'] is not None:
            try:
                source_detail = re.search(clean['source_detail'],message['source_detail']).group(1)
                message['source_detail'] = source_detail
            except:
                log.error("详细来源正则匹配失败{}".format(message['source_detail']))
                message['source_detail'] = None

        return message


    def consume_article_detail_url(self,ch, method, properties, body):
        # 从queue获取url , source

        # message = {"city": None, "author": None, "source": "\u7f51\u6613\u65b0\u95fb", "desc": None,
        #            "organization_author": None, "body": None, "tag": None, "comment_count": None, "category": None,
        #            "source_detail": None, "status": 0,
        #            "title": "\u4e0a\u6d77\u4e94\u516d\u5341\u5e74\u4ee3\u53a8\u536b\u5408\u7528\u8001\u516c\u623f \u6539\u9020\u6210\u9ad8\u989c\u503c\u7535\u68af\u623f",
        #            "title_img": None, "detail_url": "http://sh.house.163.com/18/0324/09/DDLDHQC90007871Q.html",
        #            "read_num": None, "url": None, "crawler_time": None, "post_time": None, "like_count": None,
        #            "article_id": None}
        message = json.loads(body.decode())
        for i in range(10):
            try:
                html = requests.get(message['detail_url'],proxies=next(self.proxy),timeout=10)
                self.connection.process_data_events()
                if html.status_code == 200:
                    break
            except Exception as e:
                if i == 10:
                    log.error("请求文章详情页{}失败".format(message['detail_url']))
                    ch.basic_ack(delivery_tag=method.delivery_tag)
        try:
            con = html.content.decode()
        except:
            con = html.content.decode('gbk')
        page = etree.HTML(con)

        # 获取详情页的解析方式
        detail_config_dict = collection.find_one({'source': message['source']})
        try:
            if detail_config_dict['body'] is not None:
                try:
                    for pattern in detail_config_dict['body']:
                        if page.xpath(pattern):
                            article_text = page.xpath(pattern)[0]
                            message['body'] = etree.tounicode(article_text)
                            break
                except:
                    log.error('xpath语句未能解析body')
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
            if detail_config_dict['source_detail'] is not None:
                message['source_detail'] = page.xpath(detail_config_dict['source_detail'])[0]
        except Exception as e:
            log.error("{}文章解析错误{}".format(message['detail_url'],e))

        self.clean(message)

        # 放入消息队列做正文替换清洗
        produce_channel = self.connection.channel()
        produce_channel.exchange_declare('article', 'direct', durable=True)
        produce_channel.queue_declare('article_body', durable=True)
        produce_channel.queue_bind(exchange='article',
                                    queue='article_body',
                                    routing_key='body')
        article_text = json.dumps(message)
        produce_channel.basic_publish(exchange='article',
                              routing_key='body',
                              body=article_text,
                              properties=pika.BasicProperties(delivery_mode=2))
        log.info('已经放入清洗队列')
        ch.basic_ack(delivery_tag=method.delivery_tag)