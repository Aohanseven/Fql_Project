from scrapy.cmdline import execute


def start_ulrspdier():
    execute(["scrapy","crawl","url_spider"])


def start_dataspdier():
    execute(["scrapy","crawl","data_spider"])


def start_agentspider():
    execute(["scrapy","crawl","agent_spider"])


if __name__ == "__main__":
    start_agentspider()
