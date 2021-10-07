import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup as bs
import json


def find_by_data_qa(tag, attr_value):
    '''Функция ищет теги, где атрибут data-qa имеет опред-ый суффикс'''
    return tag.find(attrs={'data-qa': 'vacancy-serp__vacancy-' + attr_value})


vacancies_list = []

vacancy_name = input('Введите интересующую должность: ')

while True:
    try:
        pages = int(input('Введите количество страниц(20 вакансий на странице): '))
        break
    except ValueError:
        print('Укажите число')
        continue

user_agent = UserAgent().chrome

for i in range(pages):
    url = f'https://spb.hh.ru/search/vacancy?text={vacancy_name}&page={i}'
    response = requests.get(url, headers={'User-Agent': user_agent})

    if response.status_code == 200:
        soup = bs(response.content, 'lxml')
        vacancies = soup.find_all('div', class_='vacancy-serp-item')

        for vac in vacancies:
            vacancy_dict = {}
            header = find_by_data_qa(vac, 'title')
            vacancy_dict['должность'] = header.get_text()
            vacancy_dict['ссылка'] = header['href']
            vacancy_dict['город'] = find_by_data_qa(vac, 'address').get_text()
            try:
                vacancy_dict['зарплата'] = find_by_data_qa(vac, 'compensation').get_text()

            except AttributeError:
                vacancy_dict['зарплата'] = 'зп не указана'

            vacancies_list.append(vacancy_dict)

with open('vacancies.json', 'w') as f:
    json.dump(vacancies_list, f, ensure_ascii=False)
