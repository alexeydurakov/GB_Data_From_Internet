# Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем
# должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц
# сайта (также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
# Наименование вакансии.
# Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# Ссылку на саму вакансию.
# Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
# одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas.
# Сохраните в json либо csv.
import json

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re
import pandas as pd


def parsing_hh(item):
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
            # salary = salary.replace(u'\xa0', u'')
            # salary = salary.replace('  ', '')
            # salary = salary.replace(' ', '')
            match = re.findall(r'\d+', re.sub(r'\D', ' ', salary))
            min_Salary = match[0]
            max_Salary = match[1]

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

    return vacancy_item


def request_to_hh(vacancy):
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
            vacancy_item.append(parsing_hh(item))
    return vacancy_item




def parsing_superjob(item):
    vacancy_item = {}
    position_name = item.find('span', {'class': '_1e6dO _1XzYb _2EZcW'}).getText()
    salary_as_string = item.find('span', {'class': '_2Wp8I _1e6dO _1XzYb Js9sN _3Jn4o'}).getText()
    if salary_as_string == 'По договорённости':
        max_Salary = None
        min_Salary = None
        currency = None
    else:
        salary = salary_as_string.replace(u'\xa0', u'')
        if salary.find("до") != -1:
            min_Salary = None
            max_Salary = int(re.sub(r'[^0-9]+', '', salary))
            salary = re.split(r'\s|-', salary_as_string)
            currency = salary[len(salary) - 1]
        elif salary.find("от") != -1:
            min_Salary = int(re.sub(r'[^0-9]+', '', salary))
            max_Salary = None
            salary = re.split(r'\s|-', salary_as_string)
            currency = salary[len(salary) - 1]
        else:
            salaryStr = re.split(r'\s|-', salary)
            currency = salaryStr[len(salaryStr) - 1]
            salary = ''.join(salaryStr)
            match = re.findall(r'\d+', re.sub(r'\D', ' ', salary))
            min_Salary = match[0]
            max_Salary = match[1]

    vacancy_link = item.find('a',{'class':'icMQ_'}).get('href')
    company_name = item.find('span', {'class': 'f-test-text-vacancy-item-company-name'}).find('a', {
        'class': 'icMQ_'}).getText().replace(u'\xa0', u'')
    city_work = item.find('span', {'class': 'f-test-text-company-item-location'}).getText()
    city_work = re.split(r'\s|-', city_work)[2]
    metro_station = item.find('span', {'class': 'f-test-text-company-item-location'}).getText()
    metro_station = re.split(r'\s|-', metro_station)
    if len(metro_station) < 4:
        metro_station = None
    else:
        metro_station = metro_station[3]

    vacancy_item['position_name'] = position_name
    vacancy_item['company_name'] = company_name
    vacancy_item['min_Salary'] = min_Salary
    vacancy_item['max_Salary'] = max_Salary
    vacancy_item['currency'] = currency
    vacancy_item['vacancy_link'] = vacancy_link
    vacancy_item['city_work'] = city_work
    vacancy_item['metro_station'] = metro_station
    vacancy_item['site'] = 'superjob.ru'
    return vacancy_item


def request_to_superjob(vacancy):
    vacancy_item = []
    url = 'https://www.superjob.ru/vacancy/search/'

    params = {'keywords': vacancy,
              'geo': '%5Bt%5D%5B0%5D=4',
              'page': 1}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'}

    response = requests.get(url, params=params, headers=headers)

    dom = BeautifulSoup(response.text, 'html.parser')

    # Находим последнюю страницу
    pages_block = dom.find('div', {'class': 'we08m L1p51 _106ov Z-TZg _2rimQ _298jM onoJj'})
    last_page = int(pages_block.find_all('a', {'class': 'icMQ_'})[-2].getText())
    for page in range(1, last_page):
        params['page'] = page
        response = requests.get(url, params=params, headers=headers)
        dom = BeautifulSoup(response.text, 'html.parser')

        vacancy_list = dom.find_all('div', {'class': 'f-test-search-result-item'})

        for item in vacancy_list:
            vacancy_item.append(parsing_superjob(item))
    return vacancy_item



def search_vacancy(vacancy):
    vacancy_date = []
    vacancy_date.extend(request_to_hh(vacancy))
    vacancy_date.extend(request_to_superjob(vacancy))

    with open('data.json', 'w', encoding="koi8-r") as f:
        json.dump(vacancy_date, f)

    df = pd.DataFrame(vacancy_date)

    return df


vacancy = 'python'  # input("Введите ключевое слово названия професии:")
df = search_vacancy(vacancy)
