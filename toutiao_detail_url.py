from selenium import webdriver
import time
from lib.bloom_filter import BloomFilter
from lib.rabbitmq import Rabbit
import yaml

setting = yaml.load(open('config_local.yaml'))


class Toutiao:
    def __init__(self):
        self.start_url = 'https://www.toutiao.com/ch/news_house/'
        self.driver = webdriver.Chrome()
        self.bf = BloomFilter(host=setting['redies_host'],
                              port=setting['redis_port'],
                              key='article_toutiao_test',
                              blockNum=1,
                              db=0, )
        self.rabbit = Rabbit(host=setting['rabbitmq_host'], port=setting['rabbitmq_port'], )

    def get_detail_url(self):
        self.driver.get(self.start_url)
        channel = self.rabbit.get_channel()
        channel.queue_declare(queue='article_test')
        while True:
            time.sleep(3)
            self.find_title_url(channel)
            self.driver.refresh()

    def find_title_url(self, channel):
        title_list = self.driver.find_elements_by_xpath(
            '/html/body/div/div[4]/div[2]/div[2]/div/div/div/ul/li/div/div/div/div/a')
        for i in title_list:
            url = i.get_attribute('href')
            print(i.text)
            print(url)
            # 文章进入布隆过滤器
            if self.bf.is_contains(url):
                print('bloom_filter已经存在!')
                continue
            else:
                print('bloom_filter不存在，插入url!')
                self.bf.insert(url)

                # 没有在过滤器的文章加入rabbitmq
                channel.basic_publish(exchange='',
                                      routing_key='article_test',
                                      body=url)
                print('已经放入队列')


if __name__ == '__main__':
    t = Toutiao()
    t.get_detail_url()
