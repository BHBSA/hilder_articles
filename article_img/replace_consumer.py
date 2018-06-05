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


class CleanUp:

    def reborn(self):
        connection = rabbit.get_connection()
        self.channel = connection.channel()
        self.channel.queue_declare(queue='article_body', durable=True)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.image_download,
                              queue='article_body',
                              no_ack=False)

    def start_consume(self):
        disconnected = True
        while disconnected:
            try:
                disconnected = False
                self.channel.start_consuming()
            except Exception as e:
                disconnected = True
                self.reborn()

    def image_download(self,ch, method, properties, body):
        message = json.loads(body.decode())
        article = message['body']
        try:
            if re.findall('data-src="(.*?)"', article):
                image_url_list = re.findall('data-src="(.*?)"', article)
                if len(image_url_list) == 0:
                    detail_url = message.pop('detail_url')
                    news = Article(message['source'])#删除消息中detail_url字段
                    news.dict_to_attr(message)
                    news.insert_db()
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    log.info('{}无图片可更换！'.format(detail_url))
                else:
                    detail_url = message.pop('detail_url')
                    new_body = re.sub('data-src="(.*?)"', self.replace, article)
                    message['body'] = new_body
                    news = Article(message['source'])
                    news.dict_to_attr(message)
                    news.insert_db()
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    log.info('{}已入库'.format(detail_url))
            else:
                image_url_list = re.findall('src="(.*?)"', article)
                if len(image_url_list) == 0:
                    detail_url = message.pop('detail_url')
                    news = Article(message['source'])
                    news.dict_to_attr(message)
                    news.insert_db()
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    log.info('{}无图片可更换！'.format(detail_url))
                else:
                    detail_url = message.pop("detail_url")
                    new_body = re.sub('src="(.*?)"', self.replace, article)
                    message['body'] = new_body
                    news = Article(message['source'])
                    news.dict_to_attr(message)
                    news.insert_db()
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                    log.info('{}已入库'.format(detail_url))
        except Exception as e:
            log.error("{}文章文本提取有误{}".format(message['detail_url'],e))
            ch.basic_ack(delivery_tag=method.delivery_tag)

    @staticmethod
    def replace(matchobj):
        image_url = matchobj.group(1)
        image_new_url = qiniufetch(image_url, image_url)
        rep = 'src="' + image_new_url + '"'
        if image_new_url is False:
            rep = '图片替换失败！'
        return rep





