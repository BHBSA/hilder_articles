from fenghuang.fenghuang_producer import Fenghuang
from wangyi.wangyi_producer import Wangyi
from threading import Thread
import schedule
import time
from lib.log import LogHandler
import datetime

log = LogHandler("producer_schedule")
def fenghuang():
    fen = Fenghuang()
    log.info('{}开始抓取{}url'.format(datetime.datetime.now(), 'fenghuang'))
    Thread(target=fen.start_crawler).start()
    # g1 = gevent.spawn(fen.start_crawler)
    # g1.join()

def wangyi():
    wangyi = Wangyi()
    log.info('{}开始抓取{}url'.format(datetime.datetime.now(),'wangyi'))
    Thread(target=wangyi.start_crawler).start()
    # g2 = gevent.spawn(wangyi.start_crawler)
    # g2.join()

def producer_run():
    schedule.every().day.at("18:30").do(fenghuang)
    schedule.every().day.at("18:30").do(wangyi)
    while True:

        schedule.run_pending()
        time.sleep(1)


