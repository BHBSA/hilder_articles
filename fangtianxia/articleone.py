import requests
from bs4 import BeautifulSoup

#第一种文章
def getarticle1(url):
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.select('.news-detail-content > .news-title')[0].text.strip()                       #标题
        source = soup.select('.assis-title')[0].text.strip()[0:5]                                       #来源
        time = soup.select('.assis-title')[0].text.strip()[5:]                                          #时间
        content = soup.select('.news-detail-content')[0].text.strip()                                             #内容
        tags = soup.find_all('span', 'lab-span')
        L = []                                                                                  #L为所有的标签
        for i in tags:
            tagList = i.text
            L.append(tagList)
        data = [title, source, time, content, L]
        return data
    except Exception as e:
        print(e)




