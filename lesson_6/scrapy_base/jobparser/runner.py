from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from jobparser.spiders.avito import AvitoSpider
from jobparser import settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitoSpider, mark='asus')
    process.start()
