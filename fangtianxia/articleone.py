import requests
from bs4 import BeautifulSoup

#第一种文章
def getarticle1(url):
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.select('.news-detail-content > .news-title')[0].text.strip()          #标题
        source = soup.select('.assis-title')[0].text.strip()[0:5]                          #来源
        time = soup.select('.assis-title')[0].text.strip()[5:]                             #时间
        content = soup.select('.news-detail-content')[0]
        content = content.prettify()                                                        #内容
        tags = soup.find_all('span', 'lab-span')
        summery = soup.select('.news-summery')[0].text.strip('[摘要]').strip()
        L = []                                                                             #L为所有的标签
        for i in tags:
            tagList = i.text
            L.append(tagList)
        data = [title, source, time, content, L, summery]
        return data
    except Exception as e:
        print(e)

# url = 'http://news.sh.fang.com/2018-05-11/28432687.htm'
# getarticle1(url)



