from article_list_page.page_url_config import page_list
from lib.bloom_filter import BloomFilter
from lib.log import LogHandler
from lib.rabbitmq import Rabbit
from pymongo import MongoClient
from lib.proxy_iterator import Proxy
from article import Article
from lxml import etree
import requests
import json
import pika
import yaml
from itertools import cycle


setting = yaml.load(open('config_local.yaml'))

m = MongoClient(setting['mongo_235']['config_host'], setting['mongo_235']['port'])
collection = m[setting['mongo_235']['config_db']][setting['mongo_235']['coll_list']]

bf = BloomFilter(host=setting['redies_host'],
                port=setting['redis_port'],
                key='article_test',
                blockNum=1,
                db=0, )

r = Rabbit(setting['rabbitmq_host'],setting['rabbitmq_port'])
connect = r.get_connection()
channel = connect.channel()
channel.exchange_declare('article', 'direct', durable=True)
channel.queue_declare('usual_article', durable=True)
channel.queue_bind(exchange='article',
                   queue='usual_article',
                   routing_key='usual')

log = LogHandler(__name__)

class CrawlerArticleListUrl:
    def __init__(self):
        self.url_list = page_list
        self.proxy = Proxy()


    def crawler_url(self):
        all_dict = collection.find({})
        for source_dict in cycle(all_dict):
            for info in source_dict['url']:
                url = info[1]
                city = info[0]
                for i in range(10):
                    try:
                        html = requests.get(url,proxies=next(self.proxy),timeout=10)   #代理
                        if html.status_code == 200:
                            break
                        elif i == 10 and html.status_code != 200:
                            log.error("{}列表页访问失败".format(url))
                    except Exception as e:
                        log.error(e)
                self.new_article(html.content.decode(source_dict['decode']), source_dict, city)

    @staticmethod
    def new_article(html, source, city):
        if source['analyzer_rule'] == 'xpath':
            page = etree.HTML(html)
            for single_article in page.xpath(source['single_article_rule']):
                article = Article(source['source'])
                article.title = single_article.xpath(source['title'])[0].strip()
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
                    if source['post_time'] is not None:
                        try:
                            article.post_time = single_article.xpath(source['post_time'])[0].strip()
                        except:
                            log.error('post_time解析失败')
                            article.post_time =  None

                    article_dict = article.to_dict()
                    article_dict['detail_url'] = single_article.xpath(source['detail_url'])[0]

                    # 放入rabbitmq
                    message = json.dumps(article_dict)
                    # {"city": null, "author": null, "source": "\u7f51\u6613\u65b0\u95fb", "desc": null, "organization_author": null, "body": null, "tag": null, "comment_count": null, "category": null, "source_detail": null, "status": 0, "title": "\u4e0a\u6d77\u4e94\u516d\u5341\u5e74\u4ee3\u53a8\u536b\u5408\u7528\u8001\u516c\u623f \u6539\u9020\u6210\u9ad8\u989c\u503c\u7535\u68af\u623f", "title_img": null, "detail_url": "http://sh.house.163.com/18/0324/09/DDLDHQC90007871Q.html", "read_num": null, "url": null, "crawler_time": null, "post_time": null, "like_count": null, "article_id": null}
                    channel.basic_publish(exchange='article',
                                               routing_key='usual',
                                               body=message,
                                               properties=pika.BasicProperties(delivery_mode=2))
                    log.info('已经放入队列')

