from article_list_page.page_url_config import page_list
from lib.bloom_filter import BloomFilter
from lib.log import LogHandler
from pymongo import MongoClient
from lib.proxy_iterator import Proxy
from article import Article
from lxml import etree
import requests
import json
import pika
import yaml
import re
from itertools import cycle
from article_img.qiniu_fetch import qiniufetch


setting = yaml.load(open('config_local.yaml'))

m = MongoClient(setting['mongo_235']['config_host'], setting['mongo_235']['port'])
collection = m[setting['mongo_235']['config_db']][setting['mongo_235']['coll_list']]

bf = BloomFilter(host=setting['redies_host'],
                port=setting['redis_port'],
                key='article_test',
                blockNum=1,
                db=0, )

log = LogHandler(__name__)

class CrawlerArticleListUrl:
    def __init__(self):
        self.url_list = page_list
        self.proxy = Proxy()

    def produce_connect(self):
        connect = pika.BlockingConnection(pika.ConnectionParameters(host=setting['rabbitmq_host'],
                                                                    port=setting['rabbitmq_port'],heartbeat=10))
        self.channel = connect.channel()
        self.channel.exchange_declare('article', 'direct', durable=True)
        self.channel.queue_declare('usual_article', durable=True)
        self.channel.queue_bind(exchange='article',
                           queue='usual_article',
                           routing_key='usual')

    def crawler_url(self):
        all_dict = collection.find({})
        for source_dict in cycle(all_dict):
            if source_dict['method'] == 'get':
                for info in source_dict['url']:
                    url = info[1]
                    city = info[0]
                    for i in range(10):
                        try:
                            html = requests.get(url,proxies=next(self.proxy),timeout=10)   #代理
                            if html.status_code == 200:
                                break
                        except Exception as e:
                                log.error("{}列表页访问失败".format(url))
                    self.new_article(html.content.decode(source_dict['decode']), source_dict, city=city)

            if source_dict['method'] == 'post':
                url = source_dict['url']
                for data in source_dict['formdata']:   #formdata需要构造
                    for i in range(10):
                        try:
                            html = requests.get(url,data=data,proxies=next(self.proxy),timeout=10)   #代理
                            if html.status_code == 200:
                                break
                        except Exception as e:
                            log.error(e)
                    self.new_article(html.content.decode(source_dict['decode']), source_dict,)

    def new_article(self,html, source, city=None):
        if source['analyzer_rule'] == 'xpath':
            page = etree.HTML(html)
            for single_article in page.xpath(source['single_article_rule']):
                article = Article(source['source'])
                try:
                    article.title = single_article.xpath(source['title'])[0].strip()
                except:
                    log.error('{}标题不符合xpath规则'.format(source['source']))
                article.city = city
                # bf
                if bf.is_contains(article.title):
                    log.info('文章已经在redis存在,标题={}'.format(article.title))
                    continue
                else:
                    bf.insert(article.title)
                    log.info('新文章，解析文章,标题={}'.format(article.title))
                    if source['comment_count'] is not None:
                        article.comment_count = single_article.xpath(source['comment_count'])[0].strip()
                    if source['like_count'] is not None:
                        article.like_count = single_article.xpath(source['like_count'])[0].strip()
                    if source['read_num'] is not None:
                        article.read_num = single_article.xpath(source['read_num'])[0].strip()
                    if source['title_img'] is not None:
                        try:
                            title_img = single_article.xpath(source['title_img'])[0].strip()
                            article.title_img = qiniufetch(title_img,title_img)
                        except Exception as e:
                            log.error("{}封面图片提取失败".format(article.title))
                    if source['post_time'] is not None:
                        try:
                            article.post_time = single_article.xpath(source['post_time'])[0].strip()
                        except:
                            log.error('post_time解析失败')
                            article.post_time =  None

                    article_dict = article.to_dict()
                    article_dict['detail_url'] = single_article.xpath(source['detail_url'])[0]
                    self.rabbit(article_dict)

        elif source['analyzer_rule'] == 'regex':
            for single_article in re.findall(source['single_article_rule'],html,re.S|re.M):
                article = Article(source['source'])
                article.title = re.search(source['title'],single_article).group(1)
                article.city = city
                if bf.is_contains(article.title):
                    log.info('文章已经在redis存在,标题={}'.format(article.title))
                    continue
                else:
                    bf.insert(article.title)
                    log.info('新文章，解析文章,标题={}'.format(article.title))
                    if source['comment_count'] is not None:
                        article.comment_count = re.search(source['comment_count'],single_article).group(1)
                    if source['like_count'] is not None:
                        article.like_count = re.search(source['like_count'],single_article).group(1)
                    if source['read_num'] is not None:
                        article.read_num = re.search(source['read_num'],single_article).group(1)
                    if source['post_time'] is not None:
                        article.post_time = re.search(source['post_time'],single_article).group(1)
                    if source['title_img'] is not None:
                        title_img = re.search(source['title_img'],single_article).group(1)
                        article.title_img = qiniufetch(title_img, title_img)
                    article_dict = article.to_dict()
                    article_dict['detail_url'] = re.search(source['detail_url'],single_article).group(1)
                    self.rabbit(article_dict)



    def rabbit(self,article_dict):
        # 放入rabbitmq
        disconnected = True
        while disconnected:
            try:
                disconnected = False
                message = json.dumps(article_dict)
                # {"city": null, "author": null, "source": "\u7f51\u6613\u65b0\u95fb", "desc": null, "organization_author": null, "body": null, "tag": null, "comment_count": null, "category": null, "source_detail": null, "status": 0, "title": "\u4e0a\u6d77\u4e94\u516d\u5341\u5e74\u4ee3\u53a8\u536b\u5408\u7528\u8001\u516c\u623f \u6539\u9020\u6210\u9ad8\u989c\u503c\u7535\u68af\u623f", "title_img": null, "detail_url": "http://sh.house.163.com/18/0324/09/DDLDHQC90007871Q.html", "read_num": null, "url": null, "crawler_time": null, "post_time": null, "like_count": null, "article_id": null}
                self.channel.basic_publish(exchange='article',
                                           routing_key='usual',
                                           body=message,
                                           properties=pika.BasicProperties(delivery_mode=2))
                log.info('已经放入队列')

            except Exception as e:
                disconnected = True
                self.produce_connect()

