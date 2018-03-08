import datetime
from lib.mongo import Mongo
import yaml

setting = yaml.load(open('config_local.yaml'))


def serialization_info(info):
    """

    :param info:
    :return: data:
    """
    data = {}
    for key, value in vars(info).items():
        if key is 'coll':
            continue
        data[key] = value
    return data


class Article:
    def __init__(self, source, url=None, title=None, body=None, article_id=None, post_time=None, title_img=None,
                 comment_count=None, like_count=None, author=None, read_num=None, crawler_time=None):
        self.source = source  # 文章来源
        self.url = url  # 链接
        self.title = title  # 标题 数组
        self.body = body  # 正文
        self.article_id = article_id  # 文章id
        self.title_img = title_img  # 列表页的图片/封面
        self.comment_count = comment_count  # 评论数 num
        self.like_count = like_count  # 点赞数 num
        self.read_num = read_num  # 阅读量 num
        self.author = author  # 作者
        self.post_time = post_time  # 文章发布时间 str
        self.crawler_time = crawler_time
        self.status = 0
        # self.crawler_time = datetime.datetime.now()  # 抓取时间

        self.coll = Mongo(setting['mongo']['host'], setting['mongo']['port'], setting['mongo']['db_name'],
                          setting['mongo']['coll_comm']).get_collection_object()

    def insert_db(self):
        data = serialization_info(self)
        self.coll.insert_one(data)
        print('插入一条数据', data)

    def to_dict(self):
        data = serialization_info(self)
        return data

    def dict_to_attr(self, dict_data):
        """
        传递字典返回文章对象
        :param dict_data:
        :return:
        """
        for key, value in dict_data.items():
            if not hasattr(self, key):
                print('not has key:', key)
                continue
            setattr(self, key, value)
        return self


if __name__ == '__main__':
    # print(setting['mongo']['host'],
    #       setting['mongo']['port'],
    #       setting['mongo']['db_name'],
    #       setting['mongo']['coll_comm'])
    a = Article(source='toutiao')
    a.insert_db()
