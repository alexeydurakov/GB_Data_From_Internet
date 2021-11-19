import json
import requests


path = 'https://api.kinopoisk.cloud/movies/all/page/'

pages = list(range(100, 103))

# Считываем токен
with open('key.txt') as key_file:
    token = key_file.read()

all_films_json = []

for page in pages:
    url = f'{path}{page}/token/{token}'
    responce = requests.get(url)
    result_json = responce.json()
    all_films_json += result_json['movies']

for item in all_films_json:
    print(item['title'])

#Результат
# Разные судьбы
# Гран при
# Месть кинематографического оператора
# Живет такой парень
# Буковски
# Вечера на хуторе близ Диканьки
# Мужчины
# Мост Ватерлоо
# Математик и черт
# Саламанка
# Те мгновения...
# Корова
# Поп Америка
# Танго нашего детства
# Внимание, ТРЭШ! История трэш металла
# Путь к вечной жизни
# Про рок
# Большой Ух
# Любимая мозоль
# Ладони
# Любите ли вы Брамса?
# Первая позиция
# Бродский не поэт
# За пределом
# Хочу быть дирижером
# Майкл Джордан
# Курьер
# Мышонок в школе
# Сон в летнюю ночь
# Треугольник


