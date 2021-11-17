from datetime import datetime
from bs4 import BeautifulSoup
from time import sleep
import requests
import pandas as pd
import mysql.connector
import locale

news_headline = []
news_category = []
news_created = []
news_url = []
next_page_url = []
one_year_date = []
indeks_url = []
all_news_url = []
text_news_content = []

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='okezone'
)

mycursor = mydb.cursor()


def get_one_year_url(url):
    oneyear = pd.date_range(start='2021-11-09', end='2021-11-10')
    final_date = oneyear.strftime('/%Y/%m/%d/')
    for date in range(len(final_date)):
        new_url = url + final_date[date]
        indeks_url.append(new_url)


def get_next_page_url():
    for year in range(len(indeks_url)):
        new_url = indeks_url[year]
        increment = 0
        for i in range(1):
            url_new = new_url + str(increment)
            source = requests.get(new_url).text
            soup = BeautifulSoup(source, 'lxml')
            body = soup.find('body')
            list_berita = body.find('li', class_='col-md-12 p-nol m-nol hei-index')

            if list_berita:
                next_page_url.append(url_new)
                increment += 10
            else:
                break
            sleep(10)


def get_news():
    for all_url in range(len(next_page_url)):
        source = requests.get(next_page_url[all_url]).text
        soup = BeautifulSoup(source, 'lxml')
        body = soup.find('body')
        for headline_index in body.find_all('h4', class_='f17'):
            if headline_index:
                news_headline.append(headline_index.text.strip())

            else:
                break

        for category_index in body.find_all(class_='c-news'):
            if category_index:
                news_category.append(category_index.a.text)
            else:
                break

        for time_index in body.find_all('time', class_='category-hardnews f12'):
            if time_index:
                unwanted = time_index.find('span', class_='c-news')
                unwanted.extract()
                final_date = time_index.text.strip()
                string_date = str(final_date)
                var = string_date.split(' ', 1)[1].rstrip(' WIB')
                locale.setlocale(locale.LC_ALL, 'id')
                datetime_object = datetime.strptime(var, '%d %B %Y %H:%M')
                string_datetime_object = str(datetime_object)
                news_created.append(string_datetime_object)
            else:
                break

        for url_index in body.find_all('h4', class_='f17'):
            if url_index:
                news_url.append(url_index.a.get('href'))
            else:
                break
        sleep(10)


def get_all_news_url(url):
    increment = 0
    for i in range(5):
        increment += 1
        formatted_url = url + f'?page={increment}'
        source = requests.get(formatted_url).text
        soup = BeautifulSoup(source, 'lxml')
        body = soup.find('body')
        no_active = body.find('div', class_='next noactive')
        next_button = body.find('div', class_='next')
        next_article = body.find('a', class_='ga_NextArticle')

        if next_button:
            get_news_content(formatted_url)
            if no_active or next_article:
                break
            else:
                pass
        elif not next_button or next_article:
            get_news_content(url)
            break
        else:
            break
        sleep(10)


def get_news_content(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, 'lxml')
    body = soup.find('body')
    news_content = body.find('div', class_='read')
    text = news_content.get_text()
    final_text = text.replace('\n', ' ')
    text_news_content.append(final_text)
    sleep(10)


def main():
    next_page_url.append('https://news.okezone.com/indeks/2021/11/17/')
    get_news()
    for i in range(len(news_url)):
        get_news_content(news_url[i])
    for j in range(len(news_headline)):
        headline = news_headline[j]
        kategori = news_category[j]
        created = news_created[j]
        url = news_url[j]
        berita = text_news_content[j]

        sql = 'INSERT INTO berita (headline, kategori, tanggal, url, teks) VALUES (%s, %s, %s, %s, %s)'
        val = (headline, kategori, created, url, berita)
        mycursor.execute(sql, val)
        mydb.commit()


if __name__ == '__main__':
    get_news_content('https://nasional.okezone.com/read/2021/11/17/337/2503244/kasus-aktif-covid-19-turun-99-dari-puncak-pada-juli-lalu')
    print(text_news_content)
