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
bf = BloomFilter('192.168.0.235', 6699)
r = Rabbit('192.168.0.192', 5673)


class CrawlerArticleListUrl:
    def __init__(self):
        self.url_list = page_list

    def crawler_url(self):
        for source_dict in collection.find():
            html = requests.get(source_dict['url'])
            self.new_article(html.content.decode(html.encoding), source_dict)

    @staticmethod
    def new_article(html, source):
        if source['analyzer_rule'] == 'xpath':
            page = etree.HTML(html)
            for single_article in page.xpath(source['single_article_rule']):
                article = Article(source['source'])
                article.title = single_article.xpath(source['title'])[0].strip()
                # bf
                if bf.is_contains(article.title):
                    log.info('文章已经在redis存在,标题={}'.format(article.title))
                    continue
                else:
                    log.info('新文章，解析文章,标题={}'.format(article.title))
                    if source['comment_count'] is not None:
                        article.comment_count = single_article.xpath(source['comment_count'])[0].strip()
                    if source['like_count'] is not None:
                        article.like_count = single_article.xpath(source['like_count'])[0].strip()
                    if source['read_num'] is not None:
                        article.read_num = single_article.xpath(source['read_num'])[0].strip()
                    if source['post_time'] is not None:
                        article.post_time = single_article.xpath(source['post_time'])[0].strip()

                    article_dict = article.to_dict()
                    article_dict['detail_url'] = single_article.xpath(source['detail_url'])[0]

                    # todo 放入rabbitmq
                    json.dumps(article_dict)
                    # {"city": null, "author": null, "source": "\u7f51\u6613\u65b0\u95fb", "desc": null, "organization_author": null, "body": null, "tag": null, "comment_count": null, "category": null, "source_detail": null, "status": 0, "title": "\u4e0a\u6d77\u4e94\u516d\u5341\u5e74\u4ee3\u53a8\u536b\u5408\u7528\u8001\u516c\u623f \u6539\u9020\u6210\u9ad8\u989c\u503c\u7535\u68af\u623f", "title_img": null, "detail_url": "http://sh.house.163.com/18/0324/09/DDLDHQC90007871Q.html", "read_num": null, "url": null, "crawler_time": null, "post_time": null, "like_count": null, "article_id": null}

                    # todo 加入布隆过滤器
