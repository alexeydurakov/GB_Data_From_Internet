# Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о письмах
# в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172#
import re
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient


def get_visible_links(items):
    mails = []
    for item in items:
        mails.append(item.get_attribute('href'))
    return mails


login = "study.ai_172"
password = "NextPassword172#"
mail_url = "https://account.mail.ru/login/"

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(executable_path="D:\PycharmProjects\LESSONS Methods of collecting and processing data from the Internet\chromedriver.exe", options=chrome_options)
driver.get(mail_url)

login_place = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
login_place.send_keys(login)
login_place.submit()

password_place = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, 'password')))
password_place.send_keys(password)
password_place.submit()

# сколько писем в ящике
inbox_items = WebDriverWait(driver, 40).until(EC.visibility_of_element_located((By.CLASS_NAME, 'nav__item_active')))
title = inbox_items.get_attribute('title')
count_letters = int(re.search(r"Входящие, (\d*) ", title).group(1))

# urls_marker = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.CLASS_NAME, 'js-letter-list-item')))
#mails_list_in_screen = driver.find_elements(By.CLASS_NAME, 'js-letter-list-item')

all_mails = []
# собираем письма на экране в общий список
#all_mails += get_visible_links(mails_list_in_screen)

# прокручивеам и собираем письма на экране в общий список
while len(all_mails) < count_letters:
    mails_list_in_screen = driver.find_elements(By.CLASS_NAME, 'js-letter-list-item')
    all_mails += get_visible_links(mails_list_in_screen)
    actions = ActionChains(driver)
    actions.move_to_element(mails_list_in_screen[-1])
    actions.perform()
    time.sleep(1)
    print(len(all_mails))

letters = []
for mail in all_mails:
    driver.get(mail)
    author_data = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'letter__author')))
    email = {
        'email_author': author_data.find_element(By.CLASS_NAME, 'letter-contact').get_attribute('title'),
        'email_date': author_data.find_element(By.CLASS_NAME, 'letter__date').text,
        'email_title': driver.find_element(By.CLASS_NAME, 'thread__subject').text,
        'email_body': driver.find_element(By.CLASS_NAME, 'letter-body').text.replace('\n', ' ')
    }
    letters.append(email)


driver.quit()

client = MongoClient('127.0.0.1', 27017)
db = client['emails']

db.emails.insert_many(letters)

