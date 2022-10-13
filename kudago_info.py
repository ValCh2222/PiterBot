import requests
import random


def send_info_about_places(url_place):
    responce3 = requests.get(url_place).json()
    n = random.randint(0, len(responce3['results']) - 1)

    url = (str)(responce3['results'][n]['site_url'])
    new_string = f"{responce3['results'][n]['title']}\n " \
                 f"находится по адресу : {(responce3['results'][n]['address'])}\n " \
                 f"ближайшее метро: {responce3['results'][n]['subway']}\n" \
                 f"ccылка: {url}\n"

    return new_string
