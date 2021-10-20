import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import JobparserItem
import re

class SjruSpider(scrapy.Spider):
    name = 'sjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://spb.superjob.ru/vacancy/search/?keywords=SQL']
    current_page = 0
    max_page = 5

    def parse(self, response: HtmlResponse):
        if self.current_page < self.max_page:
            next_page = 'https://spb.superjob.ru/' \
                    + response.css('a.f-test-button-dalshe').attrib['href']
        else:
            next_page = None

        response.follow(next_page, callback=self.parse)
        vacancy = response.css(
            'div.jNMYr '
            'a.icMQ_::attr(href)'
        ).extract()

        for link in vacancy:
            yield response.follow('https://spb.superjob.ru' + link,
                                  callback=self.vacancy_parse)

        if next_page:
            self.current_page += 1
            yield scrapy.Request(response.urljoin(next_page),
                                 callback=self.parse)

    def vacancy_parse(self, response: HtmlResponse):
        name = response.css('div._3MVeX h1::text').getall()[0]
        salary = response.css(
            'div._3MVeX span._2Wp8I::text'
        ).getall()
        salary = list(map(lambda x: x.replace('\xa0', ''), salary))

        min_salary, max_salary, currency = None, None, None

        if len(salary) != 1:

            if len(salary) == 4:
                min_salary = salary[0]
                max_salary = salary[1]
                currency = salary[-1]

            elif salary[0].isdigit():
                min_salary, max_salary = salary[0], salary[0]
                currency = salary[-1]

            elif salary[0] == 'от':
                min_salary, currency = re.split(r'(\d+)', salary[-1])[1:]

            elif salary[0] == 'до':
                max_salary, currency = re.split(r'(\d+)', salary[-1])[1:]

        yield JobparserItem(name=name,
                            min_salary=min_salary,
                            max_salary=max_salary,
                            source=self.allowed_domains,
                            link=response.url,
                            currency=currency)
