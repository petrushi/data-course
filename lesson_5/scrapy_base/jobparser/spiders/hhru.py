# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem


class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://izhevsk.hh.ru/search/vacancy?area=&st=searchVacancy&text=python']
    current_page = 0
    max_page = 5

    def parse(self, response: HtmlResponse):
        if self.current_page < self.max_page:
            next_page = 'https://izhevsk.hh.ru' \
                    + response.css('a[class="bloko-button"][data-qa="pager-next"]').attrib['href']
        else:
            next_page = None

        response.follow(next_page, callback=self.parse)
        vacancy = response.css(
            'div.vacancy-serp div.vacancy-serp-item div.vacancy-serp-item__row_header '
            'a.bloko-link::attr(href)'
        ).extract()

        for link in vacancy:
            yield response.follow(link, callback=self.vacancy_parse)

        if next_page:
            self.current_page += 1
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('h1[data-qa="vacancy-title"]::text').getall()[0]
        salary = response.css(
            'div.vacancy-salary '
            'span.bloko-header-2::text '
        ).getall()
        salary = list(map(lambda x: x.replace('\xa0', ''), salary))

        min_salary, max_salary, currency = None, None, None

        if len(salary) != 1:

            currency = salary[-2]

            if len(salary) == 7:
                min_salary = salary[1]
                max_salary = salary[3]

            elif salary[0] == 'от ':
                min_salary = salary[1]

            elif salary[0] == 'до ':
                max_salary = salary[1]

            elif salary[0].isdigit():
                min_salary, max_salary = salary[0], salary[0]

        yield JobparserItem(name=name,
                            min_salary=min_salary,
                            max_salary=max_salary,
                            source=self.allowed_domains,
                            link=response.url,
                            currency=currency)
