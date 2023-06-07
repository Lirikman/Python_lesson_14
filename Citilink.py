import re
import csv
from bs4 import BeautifulSoup
import requests

url = 'https://www.rabota.ru/vacancy/?query=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82%20python&page=1'

page = requests.get(url)

print(page.status_code)

soup = BeautifulSoup(page.text, 'html.parser')

# Парсинг названий компаний
company_name = soup.find_all('span', class_='vacancy-preview-card__company-name')

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

full_text = ['Company', 'Title', 'Overflow', 'Link']

#for i in range(len(company)):
#    full_text.append([company[i] + ';' + title[i] + ';' + overflow[i] + ';' + href[i]])
#    full_text.append(overflow[i])
#    full_text.append(href[i])

with open('vacancyes.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(full_text)

with open('vacancyes.csv', 'w') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(company)

print(full_text)
# for rev in reviews:
#    print(rev)
