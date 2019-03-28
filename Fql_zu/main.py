from scrapy.cmdline import execute



def start_urlspider():
    execute(['scrapy', 'crawl', 'anjuke_urlspider'])


def start_dataspider():
    execute(['scrapy', 'crawl', 'anjuke_dataspdier'])


if __name__ == '__main__':
    start_urlspider()
    start_dataspider()