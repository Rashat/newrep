import requests
from bs4 import BeautifulSoup


DOLLAR_RUB = 'https://yandex.ru/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}

full_page = requests.get(DOLLAR_RUB, headers)

soup = BeautifulSoup(full_page.content, 'html.parser')

convert = soup.findAll('span', {'class': "inline-stocks__value_inner"})

DOLLAR = convert[0].text
EURO = convert[1].text
PETROL = convert[2].text


print(f' Курс доллара на сегодняшний день = {DOLLAR}\n\n'
      f' Курс доллара на сегодняшний день = {EURO}\n\n'
      f' Цена нефти на сегодняшний день = {PETROL}')
