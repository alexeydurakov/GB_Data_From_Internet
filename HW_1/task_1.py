# Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

path = 'https://api.github.com'
user = 'alexeydurakov'

url = f'{path}/users/{user}/repos'

responce = requests.get(url)

with open('data.json', 'w') as f:
    json.dump(responce.json(), f)

for item in responce.json():
    print(item['name'])

#Результат
# -algorithms_2021
# GB_Basics_Django_Framework
# GeekBrains
# GeekBrains_backend_Java
# GeekBrains_durakov_webui
# GeekBrains_For_DZ_SQL
# GeekBrains_JavaCore2_HW
# GeekBrains_JS_base
# GeekBrains_Python_HW
# handlers
# JavaLessons
# project
# Python_lessons_basic
# repo-github