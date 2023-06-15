import re
import csv
from bs4 import BeautifulSoup
import requests

url = 'https://www.rabota.ru/vacancy/?query=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82%20python&page=1'
url_1 = 'https://api.hh.ru/vacancies'
params = {
    'text': 'NAME:(Python)',
    'area': 1,
    'page': 1,
    'per_page': 20
}

page = requests.get(url)
page_1 = requests.get(url_1, params=params)

print(page_1.status_code)

soup = BeautifulSoup(page.text, 'html.parser')
soup_1 = BeautifulSoup(page_1.text, 'html.parser')
print(soup_1)

# Парсинг названий компаний
company_name = soup.find_all('span', class_='vacancy-preview-card__company-name')
company_name_1 = soup.find_all('professional_roles', class_='name')

# Парсинг заголовков вакансий
reviews = soup.find_all('h3', class_='vacancy-preview-card__title')

# Парсинг описаний вакансий
description = soup.find_all('div', class_='vacancy-preview-card__short-description')

company = []
title = []
overflow = []
href = []

for i in company_name:
    company.append(i.text[17:-15])

for i in reviews:
    href.append('https://www.rabota.ru/' + i.a['href'])

for i in reviews:
    title.append(i.text[17:-15])

for i in description:
    overflow.append(i.text)

title_text = ['Company', 'Title', 'Overflow', 'Link']

full_text = []

for i in range(len(company)):
    full_text.append([])
    full_text[i].append(company[i])
    full_text[i].append(title[i])
    full_text[i].append(overflow[i])
    full_text[i].append(href[i])

with open('vacancyes.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(title_text)

with open('vacancyes.csv', 'a') as f:
    writer = csv.writer(f, delimiter=';')
    for i in full_text:
        writer.writerow(i)

print(company_name_1)
