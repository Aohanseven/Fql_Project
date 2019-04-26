from scrapy.cmdline import execute


def start_urlspider():
    execute(['scrapy', 'crawl', 'anjuke_urlspider'])


def start_dataspider():
    execute(['scrapy', 'crawl', 'anjuke_dataspdier'])


def start_agentspider():
    execute(['scrapy', 'crawl', 'anjuke_agentspdier'])


if __name__ == '__main__':
    start_agentspider()
