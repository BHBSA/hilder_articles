import requests
from bs4 import BeautifulSoup

#第一种文章
def Get_Article1(url):
    #url = 'http://news.fang.com/2018-05-10/28417412.htm'
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text, 'lxml')

        title = soup.select('.news-detail-content > .news-title')[0].text                       #标题
        source = soup.select('.assis-title')[0].text.strip()[0:6]                               #来源
        time = soup.select('.assis-title')[0].text.strip().strip('\n')[6:]                      #时间
        content = soup.select('.news-detail-content')[0].text.strip().strip('\n')               #内容

        tags = soup.find_all('span', 'lab-span')

        L = []                                                                                  #L为所有的标签
        for i in tags:
            tagList = i.text
            L.append(tagList)

        data = [title, source, time, content, L]
        return data

    except Exception as e:
        print(e)
# url = 'http://news.sh.fang.com/2018-05-11/28427291.htm'
# Get_Article1(url)



