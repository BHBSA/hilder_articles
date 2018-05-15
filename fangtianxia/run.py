import requests
from bs4 import BeautifulSoup
from fangtianxia.city import get_All_City
from fangtianxia.articletwo import getarticle2
from fangtianxia.articleone import getarticle1
from article import Article
import time


article = Article('房天下')



#今日头条
def todaynews(url):
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        html = BeautifulSoup(response.text, 'lxml')

        # 今日头条第一个链接
        link1 = html.select('#newsid_D02_02 > a')[0].get('href')                                #今日头条第一个链接 (图片)
        link2 = html.select('#newsid_D02_02 > a > img')[0].get('src')                           #今日头条第一个图片地址
        # link3 = html.select('.news-content > .news-tit > a')[0].get('href')                     #今日头条第一个链接 (文字)
        # link4 = html.select('.detail-href')[0].get('href')                                      #今日头条第一个链接 ([详情])
        # 抓取字段
        # title1 = html.select('.news-content > .news-tit > a')[0].text.strip()                   #今日头条第一个链接   标题
        main1 = html.select('.news-main')[0].text.strip('[详情]').strip()                       #今日头条第一个链接   概述
        zan1 = html.select('.like')[0].text.strip('（').strip('）').strip()                     #今日头条第一个链接   点赞量

        # 今日头条第二个链接
        link5 = html.select('#newsid_D02_03 > a')[0].get('href')                                #今日头条第二条链接(图片)
        link6 = html.select('#newsid_D02_03 > a > img')[0].get('src')                           #今日头条第二个图片地址
        # link7 = html.select('.news-content > .news-tit > a')[1].get('href')                     #今日头条第二个链接 (文字)
        # link8 = html.select('.detail-href')[1].get('href')                                      #今日头条第二个链接 ([详情])
        # 抓取字段
        # title2 =html.select('.news-content > .news-tit > a')[1].text.strip()                    #今日头条第二个链接   标题
        main2 =html.select('.news-main')[1].text.strip().strip('[详情]')                        #今日头条第二个链接   概述
        zan2 = html.select('.like')[1].text.strip().strip('（').strip('）')                     #今日头条第二个链接   点赞量

        #分类
        category = html.select('.xw-tit')[0].text

        #第一个链接添加字段
        if 'open' in link1:
            list = getarticle2(link1)         #调用方法，获取字段
            article.title = list[0]
            article.source = list[1]
            article.post_time = list[2]
            article.body = list[3]
            article.tag = list[4]
            article.title_img = link2
            article.desc = main1
            article.like_count = zan1
            article.url = link1
            article.category = category
            article.insert_db()
        elif 'open' not in link1:
            list = getarticle1(link1)
            article.title = list[0]
            article.source = list[1]
            article.post_time = list[2]
            article.body = list[3]
            article.tag = list[4]
            article.title_img = link2
            article.desc = main1
            article.like_count = zan1
            article.url = link1
            article.category = category
            article.insert_db()
        else:
            return None

        #第二个链接添加字段
        if 'open' in link5:
            list = getarticle2(link5)         #调用方法，获取字段
            article.title = list[0]
            article.source = list[1]
            article.post_time = list[2]
            article.body = list[3]
            article.tag = list[4]
            article.title_img = link6
            article.desc = main2
            article.like_count = zan2
            article.url = link5
            article.category = category
            article.insert_db()
        elif 'open' not in link5:
            list = getarticle1(link5)
            article.title = list[0]
            article.source = list[1]
            article.post_time = list[2]
            article.body = list[3]
            article.tag = list[4]
            article.title_img = link6
            article.desc = main2
            article.like_count = zan2
            article.url = link5
            article.category = category
            article.insert_db()
        else:
            return None
    except Exception as e:
        print(e)


#房产要闻
def House_News(url):
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        html = BeautifulSoup(response.text, 'lxml')

        # 房产要闻 第一个链接
        link1 = html.select('#newsid_D02_04 > a')[0].get('href')                                #房产要闻 第一个链接 (图片)
        link2 = html.select('#newsid_D02_04 > a > img')[0].get('src')                           #房产要闻第一个图片地址
        # link3 = html.select('.news-tit > a')[2].get('href')                                     #房产要闻 第一个链接 (文字)
        # link4 = html.select('.detail-href')[2].get('href')                                      #房产要闻第一个链接 ([详情])
        #抓取字段
        # title1 = html.select('.news-content > .news-tit > a')[2].text.strip()                   #房产要闻第一个链接   标题
        main1 = html.select('.news-main')[2].text.strip('[详情]').strip()                       #房产要闻第一个链接   概述
        zan1 = html.select('.like')[2].text.strip('（').strip('）').strip()                     #房产要闻第一个链接   点赞量

        # 房产要闻 第二个链接
        link5 = html.select('#newsid_D02_04 > a')[1].get('href')                                #房产要闻 第二个链接 (图片)
        link6 = html.select('#newsid_D02_04 > a > img')[1].get('src')                           #房产要闻第二个图片地址
        # link7 = html.select('.news-content > .news-tit > a')[3].get('href')                     #房产要闻 第二个链接 (文字)
        # link8 = html.select('.detail-href')[3].get('href')                                      #房产要闻第二个链接 ([详情])
        #抓取字段
        # title2 = html.select('.news-content > .news-tit > a')[3].text.strip()                   #房产要闻第一个链接   标题
        main2 = html.select('.news-main')[3].text.strip('[详情]').strip()                       #房产要闻第一个链接   概述
        zan2 = html.select('.like')[3].text.strip('（').strip('）').strip()                     #房产要闻第一个链接   点赞量

        #分类
        category = html.select('.xw-tit')[1].text
        # 第一个链接添加字段
        if 'open' in link1:
            list = getarticle2(link1)  # 调用方法，获取字段
            article.title = list[0]
            article.source = list[1]
            article.post_time = list[2]
            article.body = list[3]
            article.tag = list[4]
            article.title_img = link2
            article.desc = main1
            article.like_count = zan1
            article.url = link1
            article.category = category
            article.insert_db()
        elif 'open' not in link1:
            list = getarticle1(link1)
            article.title = list[0]
            article.source = list[1]
            article.post_time = list[2]
            article.body = list[3]
            article.tag = list[4]
            article.title_img = link2
            article.desc = main1
            article.like_count = zan1
            article.url = link1
            article.category = category
            article.insert_db()
        else:
            return None

        # 第二个链接添加字段
        if 'open' in link5:
            list = getarticle2(link5)  # 调用方法，获取字段
            article.title = list[0]
            article.source = list[1]
            article.post_time = list[2]
            article.body = list[3]
            article.tag = list[4]
            article.title_img = link6
            article.desc = main2
            article.like_count = zan2
            article.url = link5
            article.category = category
            article.insert_db()
        elif 'open' not in link5:
            list = getarticle1(link5)
            article.title = list[0]
            article.source = list[1]
            article.post_time = list[2]
            article.body = list[3]
            article.tag = list[4]
            article.title_img = link6
            article.desc = main2
            article.like_count = zan2
            article.url = link5
            article.category = category
            article.insert_db()
        else:
            return None
    except Exception as e:
        print(e)


#本地热点
def localhot(url):
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        html = BeautifulSoup(response.text, 'lxml')

        piece = html.select('.left-part > dl')[2]
        category = piece.select('dt > h2')[0].text
        eachpiece1 = piece.select('dd > div')
        eachpiece2 = piece.select('dd > ul > li')
        for i in eachpiece1:
            link = i.select('.news-content > h3 > a')[0].get('href')
            main = i.select('.news-content > p')[0].text.strip().strip('[详情]')
            imglink = i.select('a > .news-img')[0].get('src')
            if 'open' in link:
                list = getarticle2(link)
                article.title = list[0]
                article.source = list[1]
                article.post_time = list[2]
                article.body = list[3]
                article.tag = list[4]
                article.desc = main
                article.url = link
                article.title_img = imglink
                article.category = category
                article.insert_db()
            elif 'open' not in link:
                list = getarticle1(link)
                article.title = list[0]
                article.source = list[1]
                article.post_time = list[2]
                article.body = list[3]
                article.tag = list[4]
                article.desc = main
                article.url = link
                article.title_img = imglink
                article.category = category
                article.insert_db()
            else:
                return None

        for j in eachpiece2:
            link = j.select('span > a')[0].get('href')
            if 'open' in link:
                list = getarticle2(link)
                article.title = list[0]
                article.source = list[1]
                article.post_time = list[2]
                article.body = list[3]
                article.tag = list[4]
                article.url = link
                article.category = category
                article.insert_db()
            elif 'open' not in link:
                list = getarticle1(link)
                article.title = list[0]
                article.source = list[1]
                article.post_time = list[2]
                article.body = list[3]
                article.tag = list[4]
                article.url = link
                article.category = category
                article.insert_db()
            else:
                return None

        # # 查看更多本地新闻  链接
        # link2 = html.select('#newsid_D02_07')[0].get('href')
        # getlinks(link2)

    except Exception as e:
        print(e)




#未分类新闻
def UnfiledNews(url):
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        html = BeautifulSoup(response.text, 'lxml')

        piece = html.select('.left-part > dl')[3]
        eachpiece = piece.select('dd > div')
        for i in eachpiece:
            link = i.select('div > h3 > a')[0].get('href')
            main = i.select('div > .news-main')[0].text.strip().strip('[详情]')
            imglink = i.select('a > .news-img')[0].get('src')
            zan = i.select('.news-content > div > .like')[0].text.strip('（').strip('）')
            if 'open' in link:
                list = getarticle2(link)
                article.title = list[0]
                article.source = list[1]
                article.post_time = list[2]
                article.body = list[3]
                article.tag = list[4]
                article.desc = main
                article.url = link
                article.title_img = imglink
                article.like_count = zan
                article.insert_db()
            elif 'open' not in link:
                list = getarticle1(link)
                article.title = list[0]
                article.source = list[1]
                article.post_time = list[2]
                article.body = list[3]
                article.tag = list[4]
                article.desc = main
                article.url = link
                article.title_img = imglink
                article.like_count = zan
                article.insert_db()

    except Exception as e:
        print(e)


#列表页链接
def getlinks(url):
    try:
        page = 0
        while page >= 0:
            page = page + 1
            time1 = time.strftime('%Y-%m-%d', time.localtime(time.time()))
            url1 = url.replace('.com/', '.com/gdxw') + '/' + time1 + '/' + str(page) + '.html'
            if url1:
                headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.9',
                        'Cache-Control': 'max-age=0',
                        'Connection': 'keep-alive'
                        }
                response = requests.get(url=url1, headers=headers)
                response.encoding = 'GBK'
                soup = BeautifulSoup(response.text,'lxml')

                links1 = soup.select('.infoBox-txt > h3 > a')
                for i1 in links1:
                    link1 = i1.get('href')
                    if 'open' in link1:
                        list = getarticle2(link1)        #调用方法，获取字段
                        article.title = list[0]
                        article.source = list[1]
                        article.post_time = list[2]
                        article.body = list[3]
                        article.tag = list[4]
                        article.url = link1
                        article.insert_db()
                    elif 'open' not in link1:
                        list = getarticle1(link1)
                        article.title = list[0]
                        article.source = list[1]
                        article.post_time = list[2]
                        article.body = list[3]
                        article.tag = list[4]
                        article.url = link1
                        article.insert_db()
                    else:
                        return None
                links2 = soup.select('.infoBox-item > h3 > a')
                for i2 in links2:
                    link2 = i2.get('href')
                    if 'open' in link2:
                        list = getarticle2(link2)
                        article.title = list[0]
                        article.source = list[1]
                        article.post_time = list[2]
                        article.body = list[3]
                        article.tag = list[4]
                        article.url = link2
                        article.insert_db()
                    elif 'open' not in link2:
                        list = getarticle1(link2)
                        article.title = list[0]
                        article.source = list[1]
                        article.post_time = list[2]
                        article.body = list[3]
                        article.tag = list[4]
                        article.url = link2
                        article.insert_db()
                    else:
                        return None
            else:
                break
    except Exception as e:
        print(e)




def start():
    list1 = get_All_City()
    for url in list1:
        todaynews(url)
        House_News(url)
        localhot(url)
        UnfiledNews(url)
        getlinks(url)







