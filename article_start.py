from article_consumer import consumer_run
from article_producer import producer_run
from multiprocessing import Process
if __name__ == '__main__':
    Process(target=consumer_run).start()
    Process(target=producer_run).start()
