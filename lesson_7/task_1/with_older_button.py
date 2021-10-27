import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from pymongo import MongoClient
from selenium.common.exceptions import NoSuchElementException


def login_to_gmail(email, password):
    try:
        driver.implicitly_wait(5)

        login_box = driver.find_element(By.XPATH, '//*[@id ="identifierId"]')
        login_box.send_keys(email)

        next = driver.find_elements(By.XPATH, '//*[@id ="identifierNext"]')
        next[0].click()

        pass_box = driver.find_element(By.XPATH,
            '//*[@id ="password"]/div[1]/div / div[1]/input')
        pass_box.send_keys(password)

        next = driver.find_elements(By.XPATH, '//*[@id ="passwordNext"]')
        next[0].click()
        print('Login successful...')

    except Exception as e:
        print('Login failed')
        print(e)


def iterate_over_messages():
    # driver.implicitly_wait(10)  # не помогло

    newest_message = driver.find_elements(By.XPATH, '//tr[@class="zA yO"]')[0]
    newest_message.click()

    while True:
        msg = parse_message()
        collection.insert_one(msg)

        try:
            older_button = driver.find_element(By.XPATH, '//div[@aria-label="Older" and not(@aria-disabled)]')
            older_button.click()
        except NoSuchElementException:
            print('done')
            break
        time.sleep(1)  # помогло)
        # driver.implicitly_wait(10)  # не помогло


def parse_message():
    subj = driver.find_element(By.XPATH, '//div[@class="nH V8djrc byY"]//h2').text
    header = driver.find_element(By.XPATH, '//div[@class="gE iv gt"]').text
    sender, date, to_me = header.split('\n')
    body = driver.find_element(By.XPATH, '//div[@class="ii gt"]').text
    message = {
        'subject': subj,
        'sender': sender,
        'date': date,
        'body': body
    }
    return message


if __name__ == "__main__":
    url = 'https://accounts.google.com/signin/v2/identifier?service=mail'
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', service_args=["--verbose", "--log-path=chrome.log"])
    driver.get(url)
    email = input('input your email: ')
    password = input('input your password: ')
    login_to_gmail(email, password)
    client = MongoClient('localhost', 27017)
    db = client['emails']
    collection = db.gmail
    iterate_over_messages()
    driver.quit()
