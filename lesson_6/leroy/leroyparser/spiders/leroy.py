import logging

import scrapy
from leroyparser.items import LeroyparserItem
from scrapy.http import HtmlResponse


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']
    current_page = 1
    start_urls = [f'https://leroymerlin.ru/catalogue/elektroinstrumenty/']

    def __init__(self, pages=1, **kwargs):
        super().__init__(**kwargs)
        self.pages = pages

    def parse(self, response: HtmlResponse):
        print(f'Парcинг {self.current_page}-й страницы...')
        products_links = response.xpath(
            '//a[contains(@data-qa, "product-image")]/@href').extract()

        for link in products_links:

            yield response.follow('https://leroymerlin.ru' + link,
                                  callback=self.parse_img)

        if self.current_page < self.pages:
            try:
                next_page = 'https://leroymerlin.ru' + response.xpath(
                    '//a[contains(@data-qa-pagination-item, "right")]/@href'
                ).extract()[0]
                self.current_page += 1

                yield scrapy.Request(response.urljoin(next_page),
                                     callback=self.parse)
            except IndexError:
                print('Страницы закончились')

    def parse_img(self, response: HtmlResponse):
        name = response.xpath('//h1//text()').extract()[0]
        price = response.xpath(
            '//div[@class="product-detailed-page"]/@data-product-price'
        ).extract()[0]
        link = response.url
        photos = response.xpath(
            '//img[contains(@alt, "product image")]/@src').extract()

        yield LeroyparserItem(name=name, price=price,
                              link=link, photos=photos)
