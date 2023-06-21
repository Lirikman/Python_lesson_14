import re
import csv

import fake_useragent
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

url = 'https://www.rabota.ru/vacancy/?query=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82%20python&page=1'
url_2 = 'https://joblab.ru/search.php?r=vac&srprofecy=python&kw_w2=1&srzpmin=&srregion=50&srcity=&srcategory=&submit=1'

user = UserAgent()
headers = {'User-Agent': user.random}

page = requests.get(url)
page_2 = requests.get(url_2, headers=headers)


soup_rabota = BeautifulSoup(page.text, 'html.parser')
soup_joblab = BeautifulSoup(page_2.text, 'html.parser')

# Парсинг названий компаний
company_name_rabota = []
rabota_soup = soup_rabota.find_all('span', class_='vacancy-preview-card__company-name')
for i in rabota_soup:
    company_name_rabota.append((i.text).replace('\n', '').strip())
company_name_joblab = []
joblab_soup = soup_joblab.find_all('p', class_='org')
for i in joblab_soup:
    company_name_joblab.append(i.text)

# Парсинг заголовков вакансий
reviews_rabota = []
rabota_soup_1 = soup_rabota.find_all('a', class_='vacancy-preview-card__title_border')
for i in rabota_soup_1:
    reviews_rabota.append((i.text).replace('\n', '').strip())
reviews_joblab = []
joblab_soup_1 = soup_joblab.find_all('p', class_='prof')
for i in joblab_soup_1:
    reviews_joblab.append(i.text)

# Парсинг описаний вакансий
description_rabota = []
rabota_soup_2 = soup_rabota.find_all('div', class_='vacancy-preview-card__short-description')
for i in rabota_soup_2:
    description_rabota.append(i.text)
description_joblab = []
joblab_soup_2 = soup_joblab.find_all('p', class_='descr2')
for i in joblab_soup_2:
    description_joblab.append((i.text))

# Парсинг ссылок на вакансии
href_rabota = []
for i in rabota_soup_1:
    href_rabota.append('https://www.rabota.ru/' + i['href'])
href_joblab = []
for i in joblab_soup_1:
    href_joblab.append('https://joblab.ru/' + i.a['href'])

# Систематизация информации по блокам: Компания, Вакансия, Описание, Ссылка
company = []
title = []
overflow = []
href = []

for i in company_name_rabota:
    company.append(i)

for i in company_name_joblab:
    company.append(i)

for i in reviews_rabota:
    title.append(i)

for i in reviews_joblab:
    title.append(i)

for i in href_rabota:
    href.append(i)
for i in href_joblab:
    href.append(i)

for i in description_rabota:
    overflow.append(i)
for i in description_joblab:
    overflow.append(i)

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
