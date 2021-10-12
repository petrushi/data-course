import requests
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
import re


def get_title_and_pages():
    '''Функция запрашивает название и кол-во страниц для парсинга'''
    vacancy_title = input('Введите интересующую должность: ')
    while True:
        try:
            pages = int(input('Введите количество страниц(20 вакансий на странице): '))
            break
        except ValueError:
            print('Укажите число')
            continue

    return vacancy_title, pages


def find_by_data_qa(tag, attr_value):
    '''Функция ищет теги, где атрибут data-qa имеет опред-ый суффикс'''

    return tag.find(attrs={'data-qa': 'vacancy-serp__vacancy-' + attr_value})


def make_vacancy(vacancy_tag):
    '''Функция создает словарь вакансии'''
    header = find_by_data_qa(vacancy_tag, 'title')
    title = header.get_text()
    link = header['href']
    city = find_by_data_qa(vacancy_tag, 'address').get_text()

    try:
        comp_text = find_by_data_qa(vacancy_tag, 'compensation').get_text()

        compensation = int(re.sub(r'\D', '', re.search(r'\d+\D?\d+', comp_text).group(0)))
        currency = re.search(r'\D+$', comp_text).group(0).strip()

    except AttributeError:
        compensation, currency = None, None

    vac_dict = {'title': title,
                'link': link,
                'compensation': compensation,
                'currency': currency,
                'city': city}

    return vac_dict


def parse_hh(title, pages, collection):
    '''Функция парсит HH.ru и добавляет вакансии в коллекцию'''
    mode = 'new' if collection.count_documents({}) == 0 else 'update'

    for i in range(pages):
        url = f'https://spb.hh.ru/search/vacancy?text={title}&page={i}&order_by=publication_time'
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

        if response.status_code == 200:
            soup = bs(response.content, 'lxml')
            vacancy_tags = soup.find_all('div', class_='vacancy-serp-item')
            vacancy_list = []

            for vacancy_tag in vacancy_tags:
                vacancy_list.append(make_vacancy(vacancy_tag))
            if mode == 'new':  # если коллекция пустая, добавляю все вакансии разом
                collection.insert_many(vacancy_list)
            else:  # если не пустая, добавляю по одной, если такой ссылки нет
                for vacancy in vacancy_list:
                    if collection.find_one({'link': vacancy['link']}) is None:
                        collection.insert_one(vacancy)
                    else:  # если попадается существующая, выхожу, т.к. они отсортированы по дате
                        break


def main(title=None, pages=None):
    if title is None:
        title, pages = get_title_and_pages()

    client = MongoClient('localhost', 27017)
    db = client['jobs_db']
    vacancies_collection = db.vacancies
    parse_hh(title, pages, vacancies_collection)


if __name__ == '__main__':
    main()
