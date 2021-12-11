# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import re

from itemadapter import ItemAdapter
from pymongo import MongoClient


class JobparserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancy071221

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]

        if spider.name == 'hhru':
            item['min'], item['max'], item['cur'] = self.hhru_process_salary(item['salary'])
        else:
            item['min'], item['max'], item['cur'] = self.superjob_process_salary(item['salary'])

        del (item['salary'])
        collection.insert_one(item)
        return item

    @staticmethod
    def hhru_process_salary(salary):
        if len(salary) == 1:
            min_Salary = None
            max_Salary = None
            currency = None
        else:
            if salary[0] == "до":
                min_Salary = None
                max_Salary = int(salary[1].replace('\xa0', ''))
                currency = salary[1]
            elif salary[2] == "до":
                min_Salary = int(salary[1].replace('\xa0', ''))
                max_Salary = int(salary[3].replace('\xa0', ''))
                currency = salary[5]
            else:
                min_Salary = int(salary[1].replace('\xa0', ''))
                max_Salary = None
                currency = salary[3]
        return min_Salary, max_Salary, currency

    @staticmethod
    def superjob_process_salary(salary):
        lenth = len(salary)
        if len(salary) == 1:
            min_Salary = None
            max_Salary = None
            currency = None
        else:
            if salary[0] == "до":
                temp = salary[2].split('\xa0')
                min_Salary = None
                max_Salary = int(temp[0] + temp[1])
                currency = temp[2]
            elif salary[0] == "от":
                temp = salary[2].split('\xa0')
                min_Salary = int(temp[0] + temp[1])
                max_Salary = None
                currency = temp[2]
            else:
                min_Salary = int(salary[0].replace('\xa0', ''))
                max_Salary = int(salary[4].replace('\xa0', ''))
                currency = salary[6]
        return min_Salary, max_Salary, currency
