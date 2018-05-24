from lib.mongo import Mongo
from .qiniu_fetch import qiniufetch
import re
import yaml
from lib.log import LogHandler


setting = yaml.load(open('config_local.yaml'))
mongo = Mongo(setting['mongo']['host'],setting['mongo']['port'],setting['mongo']['db_name'],setting['mongo']['coll_comm'])
coll = mongo.get_collection_object()
log = LogHandler("img_replace")

class ImageReplace():
    def __init__(self,):
        self.coll = coll


    def image_download(self,article):
        # article_list = self.coll.find({'replace_status':{"$nin":[1]}})        #已注释部分为直接操作数据库替换的代码
        # for article in article_list:
            # article_id = article['article_id']
            # body = article['body']
        if re.findall('data-src="(.*?)"',article):
            image_url_list = re.findall('data-src="(.*?)"',article)
            if len(image_url_list) == 0:
                log.info('无图片可更换！')
                return article
            else:
                new_body = re.sub('data-src="(.*?)"', self.replace, article)
                return new_body
        else:
            image_url_list = re.findall('src="(.*?)"',article)
            if len(image_url_list) == 0:
                log.info('无图片可更换！')
                return article
            else:
                new_body = re.sub('src="(.*?)"',self.replace,article)
                return new_body
                # self.coll.update_one({"article_id":article_id},{'$set':{'body':new_body,'replace_status':1}})

    @staticmethod
    def replace(matchobj):
        # image_key = image_url_list.index(article_img)
        file_name = matchobj.group(1)

        image_new_url = qiniufetch(file_name, file_name)
        rep = 'src="' + image_new_url + '"'
        if image_new_url == None:
            rep = 'src="' + file_name + '"'
        return rep


