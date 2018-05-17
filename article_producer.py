from fenghuang.fenghuang_producer import Fenghuang
from wangyi.wangyi_producer import Wangyi
from fangtianxia.fangtianxia_start import fangtianxia_start

if __name__ == '__main__':
    fen = Fenghuang()
    fen.start_crawler()
    # wangyi = Wangyi()
    # wangyi.start_crawler()
    fangtianxia_start()