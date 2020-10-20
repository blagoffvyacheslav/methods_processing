from bs4 import BeautifulSoup as bs
import requests
import re
import pandas as pd

TITLE = 'Python'

vacancy_date = []

params = {
    'text': TITLE,
    'search_field': 'name',
    'items_on_page': '100',
    'page': ''
}

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0'
}

link = 'https://hh.ru/search/vacancy'

html = requests.get(link, params=params, headers=headers)

if html.ok:
    parsed_html = bs(html.text, 'html.parser')

    page_block = parsed_html.find('div', {'data-qa': 'pager-block'})
    if not page_block:
        last_page = '1'
    else:
        last_page = int(page_block.find_all('a', {'class': 'HH-Pager-Control'})[-2].getText())

for page in range(0, last_page):
    params['page'] = page
    html = requests.get(link, params=params, headers=headers)

    if html.ok:
        parsed_html = bs(html.text, 'html.parser')
        vacancy_items = parsed_html.find('div', {'data-qa': 'vacancy-serp__results'}).find_all('div', {'class': 'vacancy-serp-item'})

        for item in vacancy_items:
            print(item)
            vacancy = {}
            vacancy_name = item.find('div', {'class': 'resume-search-item__name'}).getText().replace(u'\xa0', u' ')
            vacancy['vacancy_name'] = vacancy_name
            salary = item.find('div', {'class': 'vacancy-serp-item__compensation'})
            if not salary:
                salary_min = None
                salary_max = None
                salary_currency = None
            else:
                salary = salary.getText().replace(u'\xa0', u'')
                salary = re.split(r'\s|-', salary)
                if salary[0] == 'до':
                    salary_min = None
                    salary_max = int(salary[1])
                elif salary[0] == 'от':
                    salary_min = int(salary[1])
                    salary_max = None
                else:
                    salary_min = int(salary[0])
                    salary_max = int(salary[1])
                salary_currency = salary[2]
            vacancy['salary_min'] = salary_min
            vacancy['salary_max'] = salary_max
            vacancy['salary_currency'] = salary_currency
            is_ad = item.find('span',
                              {'class': 'vacancy-serp-item__controls-item vacancy-serp-item__controls-item_last'}).getText()
            vacancy_link = item.find('div', {'class': 'resume-search-item__name'}).find('a')['href']
            if is_ad != 'Реклама':
                vacancy_link = vacancy_link.split('?')[0]
            vacancy['vacancy_link'] = vacancy_link
            vacancy['site'] = 'hh.ru'
            vacancy_date.append(vacancy)
df = pd.DataFrame(vacancy_date)
print(df)