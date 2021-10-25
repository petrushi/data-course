import scrapy
from scrapy.http import HtmlResponse
import logging
from leroyparser.items import LeroyparserItem


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        self.start_urls = [f'https://leroymerlin.ru/catalogue/elektroinstrumenty']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//a[contains(@data-qa, "product-image")]/@href').extract()
        for link in ads_links:
            yield response.follow('https://leroymerlin.ru' + link, callback=self.parseimg)

    def parseimg(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').extract()[0]
        price = response.xpath('//div[@class="product-detailed-page"]/@data-product-price').extract()[0]
        photos = response.xpath('//img[contains(@alt, "product image")]/@src').extract()

        yield LeroyparserItem(name=name, photos=photos, price=price)
