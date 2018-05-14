import requests
from bs4 import BeautifulSoup

#第二种文章
def Get_Article2(url):
    #url = 'http://news.sh.fang.com/open/28412928.html'
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text,'lxml')

        title = soup.select('.news-cont > .news-title')[0].text                     #标题
        source = soup.select('#xfopen_B01_01')[1].text                              #来源
        time = soup.select('.comment > span')[2].text                               #时间
        content = soup.select('.news-text')[0].text                                 #内容

        tags = soup.select('#xfopen_B01_11')
        L = []                                                                      #L为所有的标签
        for i in tags:
            tagList = i.text
            L.append(tagList)

        data = [title, source, time, content, L]
        return data

    except Exception as e:
        print(e)
# url = 'http://news.sh.fang.com/open/28429773.html'
# Get_Article2(url)




