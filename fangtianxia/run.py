import requests
from bs4 import BeautifulSoup
from fangtianxia.listlinks import Getlinks
from fangtianxia.city import get_All_City
from fangtianxia.articletwo import Get_Article2
from fangtianxia.articleone import Get_Article1


# url = 'http://news.fang.com/'

#今日头条
def Today_News(url):
    try:
        #url = 'http://news.sh.fang.com'
        response = requests.get(url)
        response.encoding = 'GBK'
        html = BeautifulSoup(response.text, 'lxml')

        # 今日头条第一个链接
        link1 = html.select('#newsid_D02_02 > a')[0].get('href')                                #今日头条第一个链接 (图片)
        link2 = html.select('#newsid_D02_02 > a > img')[0].get('src')                           #今日头条第一个图片地址
        link3 = html.select('.news-content > .news-tit > a')[0].get('href')                     #今日头条第一个链接 (文字)
        link4 = html.select('.detail-href')[0].get('href')                                      #今日头条第一个链接 ([详情])
        # 抓取字段
        title1 = html.select('.news-content > .news-tit > a')[0].text.strip()                   #今日头条第一个链接   标题
        main1 = html.select('.news-main')[0].text.strip('[详情]').strip()                       #今日头条第一个链接   概述
        zan1 = html.select('.like')[0].text.strip('（').strip('）').strip()                     #今日头条第一个链接   点赞量

        # 今日头条第二个链接
        link5 = html.select('#newsid_D02_03 > a')[0].get('href')                                #今日头条第二条链接(图片)
        link6 = html.select('#newsid_D02_03 > a > img')[0].get('src')                           #今日头条第二个图片地址
        link7 = html.select('.news-content > .news-tit > a')[1].get('href')                     #今日头条第二个链接 (文字)
        link8 = html.select('.detail-href')[1].get('href')                                      #今日头条第二个链接 ([详情])
        # 抓取字段
        title2 =html.select('.news-content > .news-tit > a')[1].text.strip()                    #今日头条第二个链接   标题
        main2 =html.select('.news-main')[1].text.strip().strip('[详情]')                        #今日头条第二个链接   概述
        zan2 = html.select('.like')[1].text.strip().strip('（').strip('）')                     #今日头条第二个链接   点赞量

        #第一个链接添加字段
        if 'open' in link1:
            list1 = Get_Article2(link1)         #调用方法，获取字段
            list1.append(link2)
            list1.append(title1)
            list1.append(main1)
            list1.append(zan1)
            print(list1)
        elif 'open' not in link1:
            list2 = Get_Article1(link1)
            list2.append(link2)
            list2.append(title1)
            list2.append(main1)
            list2.append(zan1)
            print(list2)
        else:
            return None

        #第二个链接添加字段
        if 'open' in link5:
            list3 = Get_Article2(link5)         #调用方法，获取字段
            list3.append(link6)
            list3.append(title2)
            list3.append(main2)
            list3.append(zan2)
            print(list3)
        elif 'open' not in link5:
            list4 = Get_Article1(link5)
            list4.append(link6)
            list4.append(title2)
            list4.append(main2)
            list4.append(zan2)
            print(list4)
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
        link3 = html.select('.news-tit > a')[2].get('href')                                     #房产要闻 第一个链接 (文字)
        link4 = html.select('.detail-href')[2].get('href')                                      #房产要闻第一个链接 ([详情])
        #抓取字段
        title1 = html.select('.news-content > .news-tit > a')[2].text.strip()                   #房产要闻第一个链接   标题
        main1 = html.select('.news-main')[2].text.strip('[详情]').strip()                       #房产要闻第一个链接   概述
        zan1 = html.select('.like')[2].text.strip('（').strip('）').strip()                     #房产要闻第一个链接   点赞量

        # 房产要闻 第二个链接
        link5 = html.select('#newsid_D02_04 > a')[1].get('href')                                #房产要闻 第二个链接 (图片)
        link6 = html.select('#newsid_D02_04 > a > img')[1].get('src')                           #房产要闻第二个图片地址
        link7 = html.select('.news-content > .news-tit > a')[3].get('href')                     #房产要闻 第二个链接 (文字)
        link8 = html.select('.detail-href')[3].get('href')                                      #房产要闻第二个链接 ([详情])
        #抓取字段
        title2 = html.select('.news-content > .news-tit > a')[3].text.strip()                   #房产要闻第一个链接   标题
        main2 = html.select('.news-main')[3].text.strip('[详情]').strip()                       #房产要闻第一个链接   概述
        zan2 = html.select('.like')[3].text.strip('（').strip('）').strip()                     #房产要闻第一个链接   点赞量

        # 第一个链接添加字段
        if 'open' in link1:
            list1 = Get_Article2(link1)  # 调用方法，获取字段
            list1.append(link2)
            list1.append(title1)
            list1.append(main1)
            list1.append(zan1)
            print(list1)
        elif 'open' not in link1:
            list2 = Get_Article1(link1)
            list2.append(link2)
            list2.append(title1)
            list2.append(main1)
            list2.append(zan1)
            print(list2)
        else:
            return None

        # 第二个链接添加字段
        if 'open' in link5:
            list3 = Get_Article2(link5)  # 调用方法，获取字段
            list3.append(link6)
            list3.append(title2)
            list3.append(main2)
            list3.append(zan2)
            print(list3)
        elif 'open' not in link5:
            list4 = Get_Article1(link5)
            list4.append(link6)
            list4.append(title2)
            list4.append(main2)
            list4.append(zan2)
            print(list4)
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

        #第一个链接
        link1 = html.select('#newsid_D02_05 > a')[0].get('href')                                #本地热点 第一个链接 (图片)
        link2 = html.select('#newsid_D02_05 > a > img')[0].get('src')                           #本地热点第一个图片地址
        link3 = html.select('.news-tit > a')[4].get('href')                                     #本地热点 第一个链接 (文字)
        link4 = html.select('.detail-href')[4].get('href')                                      #本地热点第一个链接 ([详情])
        #抓取字段
        title1 = html.select('.news-content > .news-tit > a')[4].text.strip()                    #本地热点第一个链接   标题
        main1 = html.select('.news-main')[4].text.strip('[详情]').strip()                       #本地热点第一个链接   概述

        #第二个链接
        link5 = html.select('#newsid_D02_05 > a')[1].get('href')                                #本地热点 第二个链接 (图片)
        link6 = html.select('#newsid_D02_05 > a > img')[1].get('src')                           #本地热点第二个图片地址
        link7 = html.select('.news-content > .news-tit > a')[5].get('href')                     #本地热点 第二个链接 (文字)
        link8 = html.select('.detail-href')[5].get('href')                                      #本地热点第二个链接 ([详情])
        #抓取字段
        title2 = html.select('.news-content > .news-tit > a')[5].text.strip()                   #本地热点第二个链接   标题
        main2 = html.select('.news-main')[5].text.strip().strip('[详情]')                       #本地热点第二个链接   概述

        #第三个链接
        link9 = html.select('#newsid_D02_06')[0].get('href')                                    #本地热点 第三个链接 (文字)
        #抓取字段
        title3 = html.select('#newsid_D02_06')[0].text.strip()                                  #本地热点第二个链接   标题

        #第四个链接
        link10 = html.select('#newsid_D02_06')[1].get('href')                                    #本地热点 第四个链接 (文字)
        #抓取字段
        title4 = html.select('#newsid_D02_06')[1].text.strip()                                  #本地热点第四个链接   标题

        #第五个链接
        link11 = html.select('#newsid_D02_06')[2].get('href')                                    #本地热点 第五个链接 (文字)
        #抓取字段
        title5 = html.select('#newsid_D02_06')[2].text.strip()                                  #本地热点第五个链接   标题

        #第六个链接
        link12 = html.select('#newsid_D02_06')[3].get('href')                                    #本地热点 第六个链接 (文字)
        #抓取字段
        title6 = html.select('#newsid_D02_06')[3].text.strip()                                  #本地热点第六个链接   标题

        #第七个链接
        link13 = html.select('#newsid_D02_06')[4].get('href')                                    #本地热点 第七个链接 (文字)
        #抓取字段
        title7 = html.select('#newsid_D02_06')[4].text.strip()                                  #本地热点第七链接   标题

        #查看更多本地新闻  链接
        link14 = html.select('#newsid_D02_07')[0].get('href')
        Getlinks(link14)                                                                        #调用列表页链接

        # 第一个链接添加字段
        if 'open' in link1:
            list1 = Get_Article2(link1)  # 调用方法，获取字段
            list1.append(link2)
            list1.append(title1)
            list1.append(main1)
            print(list1)
        elif 'open' not in link1:
            list2 = Get_Article1(link1)
            list2.append(link2)
            list2.append(title1)
            list2.append(main1)
            print(list2)
        else:
            return None

        # 第二个链接添加字段
        if 'open' in link5:
            list3 = Get_Article2(link5)  # 调用方法，获取字段
            list3.append(link6)
            list3.append(title2)
            list3.append(main2)
            print(list3)
        elif 'open' not in link5:
            list4 = Get_Article1(link5)
            list4.append(link6)
            list4.append(title2)
            list4.append(main2)
            print(list4)
        else:
            return None
        L = []
        L.append(link9)
        L.append(link10)
        L.append(link11)
        L.append(link12)
        L.append(link13)

        # 三到七链接添加字段
        for i in L:
            if 'open' in i:
                list5 = Get_Article2(i)  # 调用方法，获取字段
                print(list5)
            elif 'open' not in i:
                list6 = Get_Article1(i)
                print(list6)
            else:
                return None



    except Exception as e:
        print(e)


#未分类新闻
def UnfiledNews(url):
    try:
        response = requests.get(url)
        response.encoding = 'GBK'
        html = BeautifulSoup(response.text, 'lxml')

        #第一个链接
        link1 = html.select('#newsid_D02_08 > a')[0].get('href')                                    #第一个链接 (图片)
        link2 = html.select('#newsid_D02_08 > a > img')[0].get('src')                               #第一个链接图片地址
        #抓取字段
        title1 = html.select('#newsid_D02_08 > div > h3 > a')[0].text.strip()                       #第一个链接   标题
        main1 = html.select('#newsid_D02_08 > div > p')[0].text.strip().strip('[详情]')             #第一个链接   概述

        # 第一个链接添加字段
        if 'open' in link1:
            list1 = Get_Article2(link1)  # 调用方法，获取字段
            list1.append(link2)
            list1.append(title1)
            list1.append(main1)
            print(list1)
        elif 'open' not in link1:
            list2 = Get_Article1(link1)
            list2.append(link2)
            list2.append(title1)
            list2.append(main1)
            print(list2)
        else:
            return None

        #第二个链接
        link3 = html.select('#newsid_D02_08 > a')[1].get('href')                                    #第二个链接 (图片)
        link4 = html.select('#newsid_D02_08 > a > img')[1].get('src')                               #第二个链接图片地址
        # 抓取字段
        title2 = html.select('#newsid_D02_08 > div > h3 > a')[1].text.strip()                       #第二个链接   标题
        main2 = html.select('#newsid_D02_08 > div > p')[1].text.strip().strip('[详情]')             #第二个链接   概述

        # 第二个链接添加字段
        if 'open' in link3:
            list3 = Get_Article2(link3)  # 调用方法，获取字段
            list3.append(link4)
            list3.append(title2)
            list3.append(main2)
            print(list3)
        elif 'open' not in link3:
            list4 = Get_Article1(link3)
            list4.append(link4)
            list4.append(title2)
            list4.append(main2)
            print(list4)
        else:
            return None

        # 第三个链接
        link5 = html.select('#newsid_D02_08 > a')[2].get('href')                                    #第三个链接 (图片)
        link6 = html.select('#newsid_D02_08 > a > img')[2].get('src')                               #第三个链接图片地址
        # 抓取字段
        title3 = html.select('#newsid_D02_08 > div > h3 > a')[2].text.strip()                       #第三个链接   标题
        main3 = html.select('#newsid_D02_08 > div > p')[2].text.strip().strip('[详情]')             #第三个链接   概述

        # 第三个链接添加字段
        if 'open' in link5:
            list5 = Get_Article2(link5)  # 调用方法，获取字段
            list5.append(link6)
            list5.append(title3)
            list5.append(main3)
            print(list5)
        elif 'open' not in link5:
            list6 = Get_Article1(link5)
            list6.append(link6)
            list6.append(title3)
            list6.append(main3)
            print(list6)
        else:
            return None


        # 第四个链接
        link7 = html.select('#newsid_D02_08 > a')[3].get('href')#第四个链接 (图片)
        link8 = html.select('#newsid_D02_08 > a > img')[3].get('src')#第四个链接图片地址
        # 抓取字段
        title4 = html.select('#newsid_D02_08 > div > h3 > a')[3].text.strip()#第四个链接   标题
        main4 = html.select('#newsid_D02_08 > div > p')[3].text.strip().strip('[详情]')#第四个链接   概述

        # 第四个链接添加字段
        if 'open' in link7:
            list7 = Get_Article2(link7)  # 调用方法，获取字段
            list7.append(link8)
            list7.append(title4)
            list7.append(main4)
            print(list7)
        elif 'open' not in link7:
            list8 = Get_Article1(link7)
            list8.append(link8)
            list8.append(title4)
            list8.append(main4)
            print(list8)
        else:
            return None

        # 第五个链接
        link9 = html.select('#newsid_D02_08 > a')[4].get('href')#第五个链接 (图片)
        link10 = html.select('#newsid_D02_08 > a > img')[4].get('src')#第五个链接图片地址
        # 抓取字段
        title5 = html.select('#newsid_D02_08 > div > h3 > a')[4].text.strip()#第五个链接   标题
        main5 = html.select('#newsid_D02_08 > div > p')[4].text.strip().strip('[详情]')#第五个链接   概述

        # 第五个链接添加字段
        if 'open' in link9:
            list9 = Get_Article2(link9)  # 调用方法，获取字段
            list9.append(link10)
            list9.append(title5)
            list9.append(main5)
            print(list9)
        elif 'open' not in link9:
            list10 = Get_Article1(link9)
            list10.append(link10)
            list10.append(title5)
            list10.append(main5)
            print(list10)
        else:
            return None

        # 第六个链接
        link11 = html.select('#newsid_D02_08 > a')[5].get('href')#第六个链接 (图片)
        link12 = html.select('#newsid_D02_08 > a > img')[5].get('src')#第六个链接图片地址
        # 抓取字段
        title6 = html.select('#newsid_D02_08 > div > h3 > a')[5].text.strip()#第六个链接   标题
        main6 = html.select('#newsid_D02_08 > div > p')[5].text.strip().strip('[详情]')#第六个链接   概述

        # 第六个链接添加字段
        if 'open' in link11:
            list11 = Get_Article2(link11)  # 调用方法，获取字段
            list11.append(link12)
            list11.append(title6)
            list11.append(main6)
            print(list11)
        elif 'open' not in link11:
            list12 = Get_Article1(link11)
            list12.append(link12)
            list12.append(title6)
            list12.append(main6)
            print(list12)
        else:
            return None


        # 第七个链接
        link13 = html.select('#newsid_D02_08 > a')[6].get('href')#第七个链接 (图片)
        link14 = html.select('#newsid_D02_08 > a > img')[6].get('src')#第七个链接图片地址
        # 抓取字段
        title7 = html.select('#newsid_D02_08 > div > h3 > a')[6].text.strip()#第七个链接   标题
        main7 = html.select('#newsid_D02_08 > div > p')[6].text.strip().strip('[详情]')#第七个链接   概述

        # 第七个链接添加字段
        if 'open' in link13:
            list13 = Get_Article2(link13)  # 调用方法，获取字段
            list13.append(link14)
            list13.append(title7)
            list13.append(main7)
            print(list13)
        elif 'open' not in link13:
            list14 = Get_Article1(link13)
            list14.append(link14)
            list14.append(title7)
            list14.append(main7)
            print(list14)
        else:
            return None

        # 第八个链接
        link15 = html.select('#newsid_D02_08 > a')[7].get('href')#第八个链接 (图片)
        link16 = html.select('#newsid_D02_08 > a > img')[7].get('src')#第八个链接图片地址
        # 抓取字段
        title8 = html.select('#newsid_D02_08 > div > h3 > a')[7].text.strip()#第八个链接   标题
        main8 = html.select('#newsid_D02_08 > div > p')[7].text.strip().strip('[详情]')#第八个链接   概述

        # 第八个链接添加字段
        if 'open' in link15:
            list15 = Get_Article2(link15)  # 调用方法，获取字段
            list15.append(link16)
            list15.append(title8)
            list15.append(main8)
            print(list15)
        elif 'open' not in link15:
            list16 = Get_Article1(link15)
            list16.append(link16)
            list16.append(title8)
            list16.append(main8)
            print(list16)
        else:
            return None

        # 第九个链接
        link17 = html.select('#newsid_D02_08 > a')[8].get('href')#第九个链接 (图片)
        link18 = html.select('#newsid_D02_08 > a > img')[8].get('src')#第九个链接图片地址
        # 抓取字段
        title9 = html.select('#newsid_D02_08 > div > h3 > a')[8].text.strip()#第九个链接   标题
        main9 = html.select('#newsid_D02_08 > div > p')[8].text.strip().strip('[详情]')#第九个链接   概述

        # 第九个链接添加字段
        if 'open' in link17:
            list17 = Get_Article2(link17)  # 调用方法，获取字段
            list17.append(link18)
            list17.append(title9)
            list17.append(main9)
            print(list17)
        elif 'open' not in link17:
            list18 = Get_Article1(link17)
            list18.append(link18)
            list18.append(title9)
            list18.append(main9)
            print(list18)
        else:
            return None

        # 第10个链接
        link19 = html.select('#newsid_D02_08 > a')[9].get('href')#第10个链接 (图片)
        link20 = html.select('#newsid_D02_08 > a > img')[9].get('src')#第10个链接图片地址
        # 抓取字段
        title10 = html.select('#newsid_D02_08 > div > h3 > a')[9].text.strip()#第10个链接   标题
        main10 = html.select('#newsid_D02_08 > div > p')[9].text.strip().strip('[详情]')#第10个链接   概述

        # 第10个链接添加字段
        if 'open' in link19:
            list19 = Get_Article2(link19)  # 调用方法，获取字段
            list19.append(link20)
            list19.append(title10)
            list19.append(main10)
            print(list19)
        elif 'open' not in link19:
            list20 = Get_Article1(link19)
            list20.append(link20)
            list20.append(title10)
            list20.append(main10)
            print(list20)
        else:
            return None

        # 第11个链接
        link21 = html.select('#newsid_D02_08 > a')[10].get('href')#第11个链接 (图片)
        link22 = html.select('#newsid_D02_08 > a > img')[10].get('src')#第11个链接图片地址
        # 抓取字段
        title11 = html.select('#newsid_D02_08 > div > h3 > a')[10].text.strip()#第11个链接   标题
        main11 = html.select('#newsid_D02_08 > div > p')[10].text.strip().strip('[详情]')#第11个链接   概述

        # 第11个链接添加字段
        if 'open' in link21:
            list21 = Get_Article2(link21)  # 调用方法，获取字段
            list21.append(link22)
            list21.append(title11)
            list21.append(main11)
            print(list21)
        elif 'open' not in link21:
            list22 = Get_Article1(link21)
            list22.append(link22)
            list22.append(title11)
            list22.append(main11)
            print(list22)
        else:
            return None

        # 第12个链接
        link23 = html.select('#newsid_D02_08 > a')[11].get('href')  # 第12个链接 (图片)
        link24 = html.select('#newsid_D02_08 > a > img')[11].get('src')  # 第12个链接图片地址
        # 抓取字段
        title12 = html.select('#newsid_D02_08 > div > h3 > a')[11].text.strip()  # 第12个链接   标题
        main12 = html.select('#newsid_D02_08 > div > p')[11].text.strip().strip('[详情]')  # 第12个链接   概述

        # 第12个链接添加字段
        if 'open' in link23:
            list23 = Get_Article2(link23)  # 调用方法，获取字段
            list23.append(link24)
            list23.append(title12)
            list23.append(main12)
            print(list23)
        elif 'open' not in link23:
            list24 = Get_Article1(link23)
            list24.append(link24)
            list24.append(title12)
            list24.append(main12)
            print(list24)
        else:
            return None

        # 第13个链接
        link25 = html.select('#newsid_D02_08 > a')[12].get('href')  # 第12个链接 (图片)
        link26 = html.select('#newsid_D02_08 > a > img')[12].get('src')  # 第12个链接图片地址
        # 抓取字段
        title13 = html.select('#newsid_D02_08 > div > h3 > a')[12].text.strip()  # 第12个链接   标题
        main13 = html.select('#newsid_D02_08 > div > p')[12].text.strip().strip('[详情]')  # 第12个链接   概述

        # 第13个链接添加字段
        if 'open' in link25:
            list25 = Get_Article2(link25)  # 调用方法，获取字段
            list25.append(link26)
            list25.append(title13)
            list25.append(main13)
            print(list25)
        elif 'open' not in link25:
            list26 = Get_Article1(link25)
            list26.append(link26)
            list26.append(title13)
            list26.append(main13)
            print(list26)
        else:
            return None

        # 第14个链接
        link27 = html.select('#newsid_D02_08 > a')[13].get('href')  # 第12个链接 (图片)
        link28 = html.select('#newsid_D02_08 > a > img')[13].get('src')  # 第12个链接图片地址
        # 抓取字段
        title14 = html.select('#newsid_D02_08 > div > h3 > a')[13].text.strip()  # 第12个链接   标题
        main14 = html.select('#newsid_D02_08 > div > p')[13].text.strip().strip('[详情]')  # 第12个链接   概述

        # 第14个链接添加字段
        if 'open' in link27:
            list27 = Get_Article2(link27)  # 调用方法，获取字段
            list27.append(link28)
            list27.append(title14)
            list27.append(main14)
            print(list27)
        elif 'open' not in link27:
            list28 = Get_Article1(link27)
            list28.append(link28)
            list28.append(title14)
            list28.append(main14)
            print(list28)
        else:
            return None

    except Exception as e:
        print(e)







if __name__ == '__main__':
    list = get_All_City()
    for url in list:
        Today_News(url)
        House_News(url)
        localhot(url)
        UnfiledNews(url)







