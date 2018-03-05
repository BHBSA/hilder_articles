import yaml
from lib.rabbitmq import Rabbit
import requests
from readability.readability import Document

setting = yaml.load(open('config_local.yaml'))

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119Safari/537.36",
    'Cache-Control': "no-cache",
    'Postman-Token': "e9b36b12-5a36-a9a3-8cb9-468a08e028a7"
}


class Consumer:
    def __init__(self):
        self.rabbit = Rabbit(host=setting['rabbitmq_host'], port=setting['rabbitmq_port'], )

    @staticmethod
    def callback(ch, method, properties, body):
        url = body.decode()
        print(url)
        url = 'http://m.haiwainet.cn/ttc/3541093/2018/0305/content_31270748_1.html?tt_group_id=6529362026471358979'
        res = requests.get(url=url, headers=headers)

        readable_article = Document(res.content).summary()
        readable_title = Document(res.content).short_title()

        print(readable_article)
        # print(readable_title)

        # 消费一条消息成功
        # ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consume(self):
        channel = self.rabbit.get_channel()
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback,
                              queue='article_test',
                              no_ack=False)
        channel.start_consuming()


if __name__ == '__main__':
    c = Consumer()
    c.start_consume()
