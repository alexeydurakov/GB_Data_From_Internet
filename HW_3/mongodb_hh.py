# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы
# (необходимо анализировать оба поля зарплаты). Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска
# продуктов с рейтингом не ниже введенного или качеством не ниже введенного (то есть цифра вводится одна, а запрос
# проверяет оба поля)
from pprint import pprint

import requests
from bs4 import BeautifulSoup
import re

from pymongo import MongoClient
from pymongo.errors import *

client = MongoClient('127.0.0.1', 27017)
db = client['DB_vacancy_from_hh']
vacancy_from_hh = db.vacancy_hh

vacancy = input("Введите ключевое слово названия професии:")
salary = int(input("Введите ваш уровень по зарплате:"))

vacancy_item = []
url = 'https://hh.ru/search/vacancy'

params = {'text': vacancy,
          'page': 1}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

response = requests.get(url, params=params, headers=headers)

dom = BeautifulSoup(response.text, 'html.parser')

# Находим последнюю страницу
pages_block = dom.find('div', {'data-qa': 'pager-block'})
last_page = int(pages_block.find_all('a', {'data-qa': 'pager-page'})[-1].getText())
for page in range(1, last_page):
    params['page'] = page
    response = requests.get(url, params=params, headers=headers)
    dom = BeautifulSoup(response.text, 'html.parser')

    vacancy_list = dom.find_all('div', {'class': 'vacancy-serp-item'})

    for item in vacancy_list:
        vacancy_item = {}
        position_name = item.find('a', {'class': 'bloko-link'}).getText()
        salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            max_Salary = None
            min_Salary = None
            currency = None
        else:
            salary = salary.getText().replace(u'\xa0', u'')
            if salary.find("до") != -1:
                min_Salary = None
                max_Salary = int(re.sub(r'[^0-9]+', '', salary))
                salary = re.split(r'\s|-', salary)
                currency = salary[len(salary) - 1]
            elif salary.find("от") != -1:
                min_Salary = int(re.sub(r'[^0-9]+', '', salary))
                max_Salary = None
                salary = re.split(r'\s|-', salary)
                currency = salary[len(salary) - 1]
            else:
                salaryStr = re.split(r'\s|-', salary)
                currency = salaryStr[len(salaryStr) - 1]
                salary = ''.join(salaryStr)
                match = re.findall(r'\d+', re.sub(r'\D', ' ', salary))
                min_Salary = int(match[0])
                max_Salary = int(match[1])

        vacancy_link = item.find('a', {'class': 'bloko-link'}).get('href')
        company_name = item.find('div', {'class': 'vacancy-serp-item__meta-info-company'}).find('a', {
            'data-qa': 'vacancy-serp__vacancy-employer'}).getText().replace(u'\xa0', u'')
        city_work = item.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).getText().split(', ')[0]
        metro_station = item.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).findChild()
        if not metro_station:
            metro_station = None
        else:
            metro_station = metro_station.getText()

        vacancy_item['position_name'] = position_name
        vacancy_item['company_name'] = company_name
        vacancy_item['min_Salary'] = min_Salary
        vacancy_item['max_Salary'] = max_Salary
        vacancy_item['currency'] = currency
        vacancy_item['vacancy_link'] = vacancy_link
        vacancy_item['city_work'] = city_work
        vacancy_item['metro_station'] = metro_station
        vacancy_item['site'] = 'hh.ru'

        try:
            vacancy_from_hh.insert_one(vacancy_item)
        except DuplicateKeyError as e:
            print(e)


for doc in vacancy_from_hh.find({'$or': [{'min_Salary': {'$gt': salary}}, {'max_Salary': {'$gt': salary}}]}):
    pprint(doc)
