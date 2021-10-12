from pymongo import MongoClient


def find_greater_wage(vacancies, min):
    return vacancies.find({
        'currency': 'руб.',
        'compensation': {'$gt': min}
        })


def main():
    min_wage = int(input('Введите минимальный порог заработной платы:'))
    client = MongoClient('localhost', 27017)
    db = client['jobs_db']
    vacancies = db.vacancies
    suiting_jobs = find_greater_wage(vacancies, min_wage)
    for vacancy in suiting_jobs:
        print(vacancy)


if __name__ == '__main__':
    main()
