from fenghuang.fenghuang_consumer import Consumer
from wangyi.wangyi_consumer import WangyiConsumer
from weixin.weixin_crawler import weixin_start
from fangtianxia.fangtianxia_start import fangtianxia_start
from meijing.meijing_start import meijing_start
# from multiprocessing import Process
from threading import Thread
if __name__ == '__main__':
    con = Consumer()
    wangyi = WangyiConsumer()
    Thread(target=con.start_consume).start()
    Thread(target=wangyi.start_consume).start()
    Thread(target=weixin_start).start()
    Thread(target=fangtianxia_start).start()
    Thread(target=meijing_start).start()