import psycopg2
from psycopg2 import Error
import requests
import json


def get_string_date(text):
    num = text.find('2', 1)
    text = text[num: len(text)]
    print(text)
    return text


def get_date_normal_form(text):
    print(text)
    res = ''
    t = ''
    if (text.find(' ') > 0):
        t = text.split()
        print(t)
    if (text.find(',') > 0):
        t = text.split(',')
    if (text.find('.') > 0):
        t = text.split('.')
        print(f't:{t}')
    if (text.find('/') > 0):
        t = text.split('/')
    if (text.find('-') > 0):
        t = text.split('-')

    if (int(t[0]) < 100):
        num = int(t[0]) + 2000
        t[0] = (str)(num)
        print(num)
    res = t[0] + '-' + t[1] + '-' + t[2]
    print(res)
    return res


def bridge_inf(message):
    info = ""
    connection = psycopg2.connect(user="postgres",
                                  # пароль, который указали при установке PostgreSQL
                                  password="12345",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="chatBot")

    cursor = connection.cursor()
    string = message
    cursor.execute(f" SELECT  PHOTO FROM bridges WHERE Name_of_Bridge =%s", (message,))
    rows2 = cursor.fetchall()
    for row in rows2:
        info = row[0]
    print(info)

    return info


def get_info_of_sightsee(message):
    try:

        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="12345",
                                      host="127.0.0.1",
                                      port="5432",
                                      database="chatBot")

        cursor = connection.cursor()
        string = message
        cursor.execute(f"SELECT ID, NAME, ADDRESS FROM sightsees_of_SPB WHERE Name=%s", (string,))
        rows = cursor.fetchall()
        text = ["", "", ""]  # text, url_photo, web_site
        te = ""
        id = 0
        for row in rows:
            id = row[0]
            name = row[1]
            address = row[2]
            te = str(name) + " находится по адресу : " + str(address)
        text[0] = (str)(te)

        cursor.execute(f"SELECT ID, PHOTO_ADDRESS, TICKETS_GET FROM sites WHERE ID=%s", (id,))
        rows2 = cursor.fetchall()
        url = ""
        for row in rows2:
            url = row[1]
        text[1] = (str)(url)
        cursor.execute(f"SELECT ADDRESS_OF_SITE FROM coordinates WHERE ID=%s", (id,))
        rows = cursor.fetchall()
        web_site = ""
        id = 0
        for row in rows:
            web_site = row[0]
        text[2] = (str)(web_site)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

    return text


def get_info_flight(message):
    cities = ['', '', '']
    t = message.split()
    start = t[0]
    if (start == "Санкт-Петербург"):
        start = "Усинск"
    finish = t[1]
    if (finish == "Санкт-Петербург"):
        finish = "Усинск"
    url = f'''https://www.travelpayouts.com/widgets_suggest_params?q=Из%20{start}%20в%20{finish}'''

    response = requests.get(url)
    info = json.loads(response.text)
    if (t[0] == "Санкт-Петербург"):
        cities[0] = 'LED'
    else:
        cities[0] = (str)(info['origin']['iata'])

    if (t[1] == "Санкт-Петербург"):
        cities[1] = 'LED'
    else:
        cities[1] = (str)(info['destination']['iata'])

    date = get_string_date(message)
    cities[2] = get_date_normal_form(date)
    print(cities)

    return cities
