from .qiniu_fetch import qiniufetch
import re
import yaml
from lib.log import LogHandler
from lib.rabbitmq import Rabbit
import json
from article import Article

setting = yaml.load(open('config_local.yaml'))
log = LogHandler("img_replace")

rabbit = Rabbit(setting['rabbitmq_host'], setting['rabbitmq_port'])
connection = rabbit.connection


class ReplaceException(Exception):
    def __init__(self, err):
        self.err = err

    def __str__(self):
        return '文章图像替换错误'


class CleanUp:
    def start_consume(self):
        channel = connection.channel()
        channel.queue_declare(queue='article_body')
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.image_download,
                              queue='article_body',
                              no_ack=False)

        channel.start_consuming()

    def image_check(self, image_url_list, message, method, ch, article, pattern): # 图片替换检查
        if len(image_url_list) == 0:
            detail_url = message.pop('detail_url')
            self.news_confirm(ch,message,method)
            log.info('{}无图片可更换！'.format(detail_url))
        else:
            detail_url = message.pop('detail_url')
            try:
                new_body = re.sub(pattern, self.replace, article)
            except ReplaceException as e:
                log.error('图片替换失败{}'.format(e))
                ch.basic_ack(delivery_tag=method.delivery_tag)
                return
            message['body'] = new_body
            self.news_confirm(ch, message, method)
            log.info('{}已入库'.format(detail_url))

    def news_confirm(self,ch,message,method): # 入库确认
        news = Article(message['source'])
        news.dict_to_attr(message)
        news.insert_db()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def image_download(self, ch, method, properties, body):
        message = json.loads(body.decode())
        article = message['body']
        try:
            if re.findall('data-src="(.*?)"', article):
                pattern = 'data-src="(.*?)"'
                image_url_list = re.findall('data-src="(.*?)"', article)
                self.image_check(image_url_list, message, method, ch, article, pattern)
            else:
                image_url_list = re.findall('src="(.*?)"', article)
                pattern = 'src="(.*?)"'
                self.image_check(image_url_list, message, method, ch, article, pattern)
        except Exception as e:
            log.error("{}文章文本提取有误{}".format(message['detail_url'], e))
            ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def replace(match_object):
        image_url = match_object.group(1)
        connection.process_data_events()
        image_new_url = qiniufetch(image_url, image_url)
        connection.process_data_events()
        if image_new_url is False:
            raise ReplaceException
        else:
            return 'src="' + image_new_url + '"'
