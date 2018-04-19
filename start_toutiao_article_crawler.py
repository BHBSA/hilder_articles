"""
开启头条抓取
"""
from toutiao.toutiao_api import Toutiao

if __name__ == '__main__':
    toutiao = Toutiao()
    toutiao.start_crawler()
