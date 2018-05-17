from fenghuang.fenghuang_producer import Fenghuang
from wangyi.wangyi_producer import Wangyi

if __name__ == '__main__':
    fen = Fenghuang()
    fen.start_crawler()
    # wangyi = Wangyi()
    # wangyi.start_crawler()