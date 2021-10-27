import time

from selenium.webdriver.common.by import By
from selenium import webdriver
from pymongo import MongoClient
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def login_to_gmail(email, password):
    try:
        driver.implicitly_wait(5)

        login_box = driver.find_element(By.XPATH, '//*[@id ="identifierId"]')
        login_box.send_keys(email)

        next = driver.find_elements_by_xpath('//*[@id ="identifierNext"]')
        next[0].click()

        pass_box = driver.find_element_by_xpath(
            '//*[@id ="password"]/div[1]/div / div[1]/input')
        pass_box.send_keys(password)

        next = driver.find_elements_by_xpath('//*[@id ="passwordNext"]')
        next[0].click()
        print('Login successful...')

    except Exception as e:
        print('Login failed')
        print(e)


def iterate_over_messages():

    messages = driver.find_elements(By.XPATH, '//tr[@class="zA yO"]')
    print('Message parsed...')

    for message in messages:
        driver.execute_script("arguments[0].click();", message)
        msg = parse_message()
        collection.insert_one(msg)


def parse_message():
    # driver.implicitly_wait(20)  # не помогло
    # WebDriverWait(driver, 150).until(EC.presence_of_element_located((By.XPATH, '//div[@class="nH V8djrc byY"]')))  # не помогло((
    time.sleep(1)  # помогло)
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
    s = 'https://accounts.google.com/signin/v2/identifier?service=mail&passive=true&rm=false&continue='\
        'https%3A%2F%2Fmail.google.com%2Fmail%2F%26ogbl%2F&ss=1&scc=1&ltmpl=default&ltmplcache='\
        '2&emr=1&osid=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
    driver = webdriver.Chrome('/usr/local/bin/chromedriver', service_args=["--verbose", "--log-path=chrome.log"])
    driver.get(s)
    email = input('input ёр email: ')
    password = input('input your password: ')
    login_to_gmail(email, password)
    client = MongoClient('localhost', 27017)
    db = client['emails']
    collection = db.gmail
    iterate_over_messages()
    driver.quit()
