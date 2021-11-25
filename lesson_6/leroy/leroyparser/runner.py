from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
import sys
from leroyparser.spiders.leroy import LeroySpider
from leroyparser import settings

if __name__ == '__main__':

    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    try:
        pages = int(sys.argv[1])
        process.crawl(LeroySpider, pages=pages)

    except IndexError:
        process.crawl(LeroySpider)

    except ValueError as e:
        print(e)
        print('Аргумент должен быть int')
        sys.exit(1)

    process.start()
