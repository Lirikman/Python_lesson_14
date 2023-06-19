import re
import csv

import fake_useragent
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent

url = 'https://www.rabota.ru/vacancy/?query=%D0%9F%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%81%D1%82%20python&page=1'
url_1 = 'https://hh.ru/search/vacancy?text=Python&salary=&area=1&ored_clusters=true'
url_2 = 'https://joblab.ru/search.php?r=vac&srprofecy=python&kw_w2=1&srzpmin=&srregion=50&srcity=&srcategory=&submit=1'

user = UserAgent()
headers = {'User-Agent': user.random}

page = requests.get(url)
#page_1 = requests.get(url_1, headers=headers)
page_2 = requests.get(url_2, headers=headers)

print(page_2.status_code)

soup_rabota = BeautifulSoup(page.text, 'html.parser')
#soup_hh = BeautifulSoup(page_1.text, 'html.parser')
soup_joblab = BeautifulSoup(page_2.text, 'html.parser')

# Парсинг названий компаний
company_name_rabota = soup_rabota.find_all('span', class_='vacancy-preview-card__company-name')
#company_name_hh = []
#hh_soup_1 = soup_hh.find_all(attrs={'class': 'bloko-link bloko-link_kind-tertiary'})
#for i in hh_soup_1:
#    company_name_hh.append((i.text).replace('\xa0', ' '))
company_name_joblab = []
joblab_soup_1 = soup_joblab.find_all('p', class_ ='org')
for i in joblab_soup_1:
    company_name_joblab.append((i.text))

# Парсинг заголовков вакансий
reviews_rabota = soup_rabota.find_all('h3', class_='vacancy-preview-card__title')
reviews_joblab = []
joblab_soup_1 = soup_joblab.find_all('p', class_='prof')
for i in joblab_soup_1:
    reviews_joblab.append((i.text))

#hh_soup_2 = soup_hh.find_all('a', class_='serp-item__title')
#reviews_hh = []
#for i in hh_soup_2:
#    reviews_hh.append(i.text)

# Парсинг описаний вакансий
description_rabota = soup_rabota.find_all('div', class_='vacancy-preview-card__short-description')
description_joblab = []
joblab_soup_3 = soup_joblab.find_all('p', class_='descr2')
for i in joblab_soup_3:
    description_joblab.append((i.text))

# Парсинг ссылок на вакансии
href_joblab = []
for i in joblab_soup_1:
    href_joblab.append('https://joblab.ru/' + i.a['href'])

# Систематизация информации по блокам: Компания, Вакансия, Описание, Ссылка
company = []
title = []
overflow = []
href = []

for i in company_name_rabota:
    company.append(i.text[17:-15])

for i in company_name_joblab:
    company.append(i)

for i in reviews_rabota:
    href.append('https://www.rabota.ru/' + i.a['href'])

for i in href_joblab:
    href.append(i)

for i in reviews_rabota:
    title.append(i.text[17:-15])

for i in reviews_joblab:
    title.append(i)

for i in description_rabota:
    overflow.append(i.text)

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