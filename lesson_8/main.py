import csv
import pandas as pd
import logging

logging.basicConfig(filename='csv.log', level=logging.DEBUG, encoding='utf-8') # pycharm не хочет, чтобы тут указывали кодировку

# https://www.fao.org/faostat/en/#data/QV
agriculture_df = pd.read_csv('data/agriculture.csv', low_memory=False)  # 2013

# https://data.humdata.org/dataset/a0109830-855f-4f7c-b6e1-f9fedc2e7b39/resource/6a49cfea-51cc-47cc-a376-cfbe1d90c469/download/national-income.csv
income_df = pd.read_csv('data/national-income.csv',
                        encoding='ISO-8859-1',
                        low_memory=False)

countries = agriculture_df['Area'].tolist()

with open('result.csv', 'w', newline='') as csvfile:
    fieldnames = ['Country', 'Agriculture', 'Domestic food price level']

    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    for country in countries:
        try:
            agriculture_value = agriculture_df.loc[agriculture_df['Area'] == country, 'Value'].to_numpy()
            domestic_food_price = income_df.loc[income_df['Location'] == country,
                                                'Domestic food price level Index 2009Ð2014'].to_numpy()

            agriculture_value = int(agriculture_value) // 1000
            domestic_food_price = int(domestic_food_price)

            writer.writerow({'Country': country, 'Agriculture': agriculture_value,
                             'Domestic food price level': domestic_food_price})
            # print(f'{country} - {agriculture_value} - {domestic_food_price}')

        except (ValueError, TypeError) as e:
            logging.log(20, f'{country} skipped! Reason: {e}. '
                            f'Agriculture value: {agriculture_value}. '
                            f'Domestic food price value: {domestic_food_price}')
            continue
