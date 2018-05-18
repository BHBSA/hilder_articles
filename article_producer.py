from fenghuang.fenghuang_producer import Fenghuang
from wangyi.wangyi_producer import Wangyi

from threading import Thread

if __name__ == '__main__':
    fen = Fenghuang()
    wangyi = Wangyi()
    Thread(target=fen.start_crawler).start()
    Thread(target=wangyi.start_crawler).start()

