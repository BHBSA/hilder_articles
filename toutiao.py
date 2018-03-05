from selenium import webdriver
import time
import requests


def selenium_cralwer():
    driver = webdriver.Chrome()
    driver.get("https://www.toutiao.com/ch/news_house/")

    time.sleep(3)

    title_list = driver.find_elements_by_xpath('/html/body/div/div[4]/div[2]/div[2]/div/div/div/ul/li/div/div/div/div/a')

    for i in title_list:
        print(i.text)
        i.click()

    driver.close()


def get_by_url():
    url = 'https://www.toutiao.com/a6396133802262921473/'
    res = requests.get(url)
    print(res.content.decode('utf8'))


if __name__ == '__main__':
    while True:
        get_by_url()
