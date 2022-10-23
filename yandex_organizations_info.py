import random
import json
import requests


def get_info_about_organizations(organization_type):
    site = f"https://search-maps.yandex.ru/v1/?text={organization_type} в  Санкт-Петербурге&lang=ru_RU&results" \
           f"=100&apikey=a4119f70-2617-4642-b836-a8553a9d9578"
    responce_yandex = requests.get(site)
    y = responce_yandex.text
    d = json.loads(y)
    text = ""
    i = random.randint(0, len(d["features"]) - 1)
    text += (d["features"][i]["properties"]["name"]) + "\n"
    try:
        text += d["features"][i]["properties"]["CompanyMetaData"]["address"] + "\n"
    except Exception:
        print('')
    try:
        url = d["features"][i]["properties"]["CompanyMetaData"]["url"] + "\n"
        text += url
    except Exception:
        print('')
    try:
        text += d["features"][i]["properties"]["CompanyMetaData"]["Phones"][0]["formatted"] + "\n"

    except Exception:
        print('')

    try:
        text += d["features"][i]["properties"]["CompanyMetaData"]["Hours"]["text"] + "\n"

    except Exception:
        print('')

    return text
