import requests
from bs4 import BeautifulSoup
from article_img.image_replace import ImageReplace

#第一种文章
def getarticle1(url):
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.select('.news-detail-content > .news-title')[0].text.strip()          #标题
        allsource = soup.select('.assis-title')[0].text.strip().split('\n')
        source1 = allsource[0].strip('\r').split('\xa0')
        source = source1[0]                                                                #来源
        author = source1[2].strip('作者：')                                                #作者
        time = allsource[1].strip().strip('\t')                                            #时间
        content = soup.select('.news-detail-content')[0]
        content = content.prettify()
        img_replace = ImageReplace()
        con = img_replace.image_download(content)                                         #内容
        tags = soup.find_all('span', 'lab-span')
        summery = soup.select('.news-summery')[0].text.strip('[摘要]').strip()             #概述
        L = []                                                                             #L为所有的标签
        for i in tags:
            tagList = i.text
            L.append(tagList)
        data = [title, source, time, con, L, summery, author]
        return data
    except Exception as e:
        print(e)

# url = 'http://news.sh.fang.com/2018-05-11/28432687.htm'
# getarticle1(url)



