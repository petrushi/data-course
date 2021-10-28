import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from pymongo import MongoClient


def parse_product():
    main_hot_product = driver.find_element(By.XPATH,
                                           '//mvid-day-products-block'
                                           '/*//mvid-product-mini-card[contains(@class, "main")]')

    header = main_hot_product.find_element(By.XPATH, './/a')
    sale = header.text
    link = header.get_attribute('href')

    price = main_hot_product.find_elements(By.XPATH, './/div[@class="price__wrapper"]//span')[0].text
    name = main_hot_product.find_element(By.XPATH, './/div[@class="title"]').text

    product = {'name': name,
               'price': price,
               'sale': sale,
               'link': link}
    print(product)
    collection.insert_one(product)


if __name__ == "__main__":
    url = 'https://www.mvideo.ru/'
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', service_args=["--verbose", "--log-path=chrome.log"])
    driver.get(url)

    client = MongoClient('localhost', 27017)
    db = client['mvideo']
    collection = db.hot
    driver.implicitly_wait(5)

    hot_cards = driver.find_elements(By.XPATH, '//mvid-day-products-block/*//mvid-product-mini-card')
    button_next = driver.find_element(By.XPATH, '//mvid-day-products-block/*//button[contains(@class, "forward")]')

    for i in range(len(hot_cards)):
        driver.implicitly_wait(10)

        parse_product()
        button_next.click()
        time.sleep(2)

    driver.quit()
    print('Products saved!')
