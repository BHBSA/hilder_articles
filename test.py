from lib.mongo import Mongo
import re

# m = Mongo(host='192.168.0.136', port=27017, db_name='fangjia_youfang', collection_name='news_library')
# coll = m.get_collection_object()
# article = coll.find_one({"title": "提前了解这些，按揭买房更顺利通过"})
# # articles = coll.find()
# # print(article['body'])
#
#
# print(article['body'])
# def change(url):
#     return url.replace('&quot;', '')
#
# for i in articles:
#     url_list = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',change,
#                            i['body'],
#                            re.S | re.M, )

url = 'http://p3.pstatp.com/large/6c3400010f07273f5379'
