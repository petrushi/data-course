# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']

    def parse(self, response: HtmlResponse):
        next_page = 'https://izhevsk.hh.ru' \
                    + response.css('a[class="bloko-button"][data-qa="pager-next"]').attrib['href']
        print(next_page)
        response.follow(next_page, callback=self.parse)
        vacansy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header '
            'a.bloko-link::attr(href)'
        ).extract()
        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacansy_parse(self, response: HtmlResponse):
        name = response.css('h1[data-qa="vacancy-title"]::text').getall()
        salary = ''.join(response.css('span[data-qa="bloko-header-2"]'
                                      '[class="bloko-header-2 bloko-header-2_lite"]::text').getall())

        print('\nНазвание вакансии: ', name[0])
        print('Зарплата: ', salary)

        yield JobparserItem(name=name, salary=salary)
