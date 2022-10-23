import psycopg2
from psycopg2 import Error
import requests
import json


def get_string_date(text):
    num = text.find('2', 1)
    text = text[num: len(text)]
    return text


def get_date_normal_form(text):
    t = ''
    if text.find(' ') > 0:
        t = text.split()
    if text.find(',') > 0:
        t = text.split(',')
    if text.find('.') > 0:
        t = text.split('.')
    if text.find('/') > 0:
        t = text.split('/')
    if text.find('-') > 0:
        t = text.split('-')

    if int(t[0]) < 100:
        num = int(t[0]) + 2000
        t[0] = str(num)

    res = t[0] + '-' + t[1] + '-' + t[2]
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
    cursor.execute(f" SELECT  PHOTO FROM bridges WHERE Name_of_Bridge =%s", (message,))
    rows2 = cursor.fetchall()
    for row in rows2:
        info = row[0]

    return info


def get_info_of_sightsee(message):
    try:

        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="12345",
                                      host="127.0.0.1",
                                      port="5432",
                                      # database="chatBot"
                                      database='chatBot')

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
        text[0] = str(te)

        cursor.execute(f"SELECT ID, PHOTO_ADDRESS, TICKETS_GET FROM sites WHERE ID=%s", (id,))
        rows2 = cursor.fetchall()
        url = ""
        for row in rows2:
            url = row[1]
        text[1] = str(url)
        cursor.execute(f"SELECT ADDRESS_OF_SITE FROM coordinates WHERE ID=%s", (id,))
        rows = cursor.fetchall()
        web_site = ""
        for row in rows:
            web_site = row[0]
        text[2] = str(web_site)

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        cursor.close()
        connection.close()

    return text


def get_info_flight(message):
    cities = ['', '', '']
    t = message.split()
    start = t[0]
    if start == "Санкт-Петербург":
        start = "Усинск"
    finish = t[1]
    if finish == "Санкт-Петербург":
        finish = "Усинск"
    url = f'''https://www.travelpayouts.com/widgets_suggest_params?q=Из%20{start}%20в%20{finish}'''

    response = requests.get(url)
    info = json.loads(response.text)
    if t[0] == "Санкт-Петербург":
        cities[0] = 'LED'
    else:
        cities[0] = str(info['origin']['iata'])

    if t[1] == "Санкт-Петербург":
        cities[1] = 'LED'
    else:
        cities[1] = str(info['destination']['iata'])

    date = get_string_date(message)
    cities[2] = get_date_normal_form(date)

    return cities


def write_info_to_file(text):
    my_file = open("mes.txt", "w")
    my_file.flush()
    try:
        my_file.write(text)
    except UnicodeEncodeError:
        print(UnicodeEncodeError.args)


def add_favourites(chat_id, message):
    try:

        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="12345",
                                      host="127.0.0.1",
                                      port="5432",
                                      # database="chatBot"
                                      database='chatBot')

        cursor = connection.cursor()

        cursor.execute(f" INSERT INTO favourites(chat_id, information ) VALUES ('{str(chat_id)}', '{message}')")
        cursor.execute('''DELETE FROM favourites AS P1  
USING favourites AS P2
WHERE P1.id > P2.id
   AND P1.chat_id = P2.chat_id
   AND P1.information = P2.information; ''')
        cursor.execute(f"SELECT * FROM favourites")
        connection.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


# очистить избранное
def clear_favourites(chat_id):
    try:

        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="12345",
                                      host="127.0.0.1",
                                      port="5432",
                                      # database="chatBot"
                                      database='chatBot')

        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM favourites WHERE chat_id='%s'", (chat_id,))
        connection.commit()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            cursor.close()
            connection.close()


def show_favourites(chat_id):
    try:
        text = ""
        # Подключение к существующей базе данных
        connection = psycopg2.connect(user="postgres",
                                      # пароль, который указали при установке PostgreSQL
                                      password="12345",
                                      host="127.0.0.1",
                                      port="5432",
                                      # database="chatBot"
                                      database='chatBot')

        cursor = connection.cursor()
        cursor.execute(f" SELECT information FROM favourites WHERE chat_id=%s", (chat_id,))

        rows = cursor.fetchall()
        connection.commit()
        for row in rows:
            text += row[0]
            text += "\n"
            text += "\n"
    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
    if text == "":
        return "у вас пока нет ничего в избранном"
    else:
        return text
