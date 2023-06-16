import re
import csv
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

url = 'https://www.rabota.ru/vacancy/?query=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82%20python&page=1'
url_1 = 'https://hh.ru/search/vacancy?text=Python&salary=&area=1&ored_clusters=true'

user = UserAgent()
headers = {'User-Agent': user.random}

page = requests.get(url)
page_1 = requests.get(url_1, headers=headers)

print(page_1.status_code)

soup_rabota = BeautifulSoup(page.text, 'html.parser')
# soup_hh = BeautifulSoup(page_1.content, 'lxml')
soup_hh = BeautifulSoup(page_1.text, 'html.parser')
# print(soup_1)

# Парсинг названий компаний
company_name_rabota = soup_rabota.find_all('span', class_='vacancy-preview-card__company-name')
company_name_hh = soup_hh.find_all(attrs={'class': 'bloko-link bloko-link_kind-tertiary'})

# Парсинг заголовков вакансий
reviews_rabota = soup_rabota.find_all('h3', class_='vacancy-preview-card__title')
reviews_hh = soup_hh.find_all('a', class_='serp-item__title')

# Парсинг описаний вакансий
description_rabota = soup_rabota.find_all('div', class_='vacancy-preview-card__short-description')
description_hh = soup_hh.find_all('a', class_='serp-item__title')

# Систематизация информации по блокам: Компания, Вакансия, Описание, Ссылка
company = []
title = []
overflow = []
href = []

for i in company_name_rabota:
    company.append(i.text[17:-15])

for i in reviews_rabota:
    href.append('https://www.rabota.ru/' + i.a['href'])

for i in reviews_rabota:
    title.append(i.text[17:-15])

for i in description_rabota:
    overflow.append(i.text)

title_text = ['Company', 'Title', 'Overflow', 'Link']

full_text = []

for i in range(len(company)):
    full_text.append([])
    full_text[i].append(company[i])
    full_text[i].append(title[i])
    full_text[i].append(overflow[i])
    full_text[i].append(href[i])

# Запись информации в файл - vacancyes.csv

with open('vacancyes.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(title_text)

with open('vacancyes.csv', 'a') as f:
    writer = csv.writer(f, delimiter=';')
    for i in full_text:
        writer.writerow(i)

print(company_name_hh)