from article_list_page.page_url_list import page_list
from lib.bloom_filter import BloomFilter
import requests
import re
from lib.log import LogHandler

log = LogHandler(__name__)

bf = BloomFilter()


class CrawlerArticleListUrl:
    def __init__(self):
        self.url_list = page_list

    def crawler_url(self):
        for source_dict in self.url_list:
            html = requests.get(source_dict['url'])
            self.new_article(html, source_dict['source'])

    @staticmethod
    def new_article(html, source):
        # todo 获取配置文件
        title = re.findall('', html, re.S | re.M)

        if bf.is_contains(title):
            log.info('文章已经存在，文章title={}'.format(title))
        else:
            log.info('文章不存在，文章title={}'.format(title))
            # todo 文章url, 放入消息队列

            # 放入消息队列成功加入布隆过滤器
            log.info('文章title已经加入布隆过滤器,title={}'.format(title))
            bf.insert(title)
