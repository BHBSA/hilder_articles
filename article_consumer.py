from fenghuang.fenghuang_consumer import Consumer
from wangyi.wangyi_consumer import WangyiConsumer

if __name__ == '__main__':
    # con = Consumer()
    # con.start_consume()
    wangyi = WangyiConsumer()
    wangyi.start_consume()