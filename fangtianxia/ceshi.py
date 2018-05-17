#
# import requests
# from bs4 import BeautifulSoup
#
# #第一种文章
# def getarticle1(url):
#     try:
#         response = requests.get(url)
#         response.encoding = 'GBK'
#         soup = BeautifulSoup(response.text, 'lxml')
#         title = soup.select('.news-detail-content > .news-title')[0].text.strip()          #标题
#         # source = soup.select('.assis-title')[0].text.strip()[0:5]                          #来源
#         # time = soup.select('.assis-title')[0].text.strip()[5:]                             #时间
#         allsource = soup.select('.assis-title')[0].text.strip().split('\n')
#         source1 = allsource[0].strip('\r').split('\xa0')
#         source = source1[0]
#         author = source1[2].strip('作者：')
#         time = allsource[1].strip().strip('\t')
#         content = soup.select('.news-detail-content')[0]
#         content = content.prettify()                                                        #内容
#         tags = soup.find_all('span', 'lab-span')
#         summery = soup.select('.news-summery')[0].text.strip('[摘要]').strip()
#         city = soup.select('.s4Box > a')[0].text
#         print(city)
#         # L = []                                                                             #L为所有的标签
#         # for i in tags:
#         #     tagList = i.text
#         #     L.append(tagList)
#         # data = [title, source, time, content, L, summery, author]
#         # print(data)
#     except Exception as e:
#         print(e)
#
# url = 'http://news.fang.com/2018-05-14/28452833.htm'
# getarticle1(url)
#
#
#
