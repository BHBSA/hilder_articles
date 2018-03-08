# import requests
from readability.readability import Document

# res = requests.get('https://www.toutiao.com/group/6527817729099956743/')
# print(res)
# print(res.content.decode())

# readable_article = Document(res.content, positive_keywords=['article-content']).summary()
#
# print(readable_article)

from article import Article

if __name__ == '__main__':
    a = Article('toutiao')
    data = {'post_time': '19分钟钱',
            'title': '40和70',
            'lala': ''}
    print(a.dict_to_attr(data).to_dict())
