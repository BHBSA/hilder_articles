import requests
import yaml
import json
from lib.mongo import Mongo
from toutiao.comments import Comments
setting = yaml.load(open('./config_local.yaml'))
import time

class Comments_crawler():
    def __init__(self):
        self.headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36"
        }
        self.temp_coll = Mongo(setting['mongo']['host'], setting['mongo']['port'], setting['mongo']['db_name'],
                          setting['mongo']['url_code']).get_collection_object()

    def comment_url(self):
        while True:
            try:
                temp_coll = self.temp_coll
                code_list = temp_coll.find().sort([('crawler_time',-1)])
                # print(code_list)
                for group in code_list:
                    if group['comment_count'] == '0':
                        continue
                    else:
                        count = group['comment_count']
                        id = group['group_id']
                        url = "http://is.snssdk.com/article/v2/tab_comments/?group_id=" + str(id)+"&count="+ str(count)
                        res = requests.get(url,headers=self.headers)
                        self.comment_info(res, id)
                        time.sleep(180)

            except Exception as e:
                print(e)

    def comment_info(self,res,id):
        comment_dict_list = json.loads(res.text)
        comment_dict_list = comment_dict_list["data"]
        for comment_dict in comment_dict_list:
            comment = Comments()

            comm_dict = comment_dict["comment"]
            comment._id = comm_dict["id"]
            comment.user_id = comm_dict["user_id"]
            comment.user_name = comm_dict["user_name"]
            comment.comment_text = comm_dict["text"]
            comment.good_count = comm_dict["digg_count"]
            comment.create_time = comm_dict["create_time"]
            comment.article_id = id

            comment.insert_db()

if __name__ == '__main__':
    crawler = Comments_crawler()
    crawler.comment_url()