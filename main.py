import telebot
import emoji
from database import *
from config import *
from wheather import *
from yandex_organizations_info import *
from kudago_info import *
from psycopg2 import Error
from telebot import types

# owm(open wheather map) KEY: b811b03b45c576c95ef39b89c1742e13
# aviasales KEY : cb614ccdbe22289b22511e54c8e02fc9
bot = telebot.TeleBot('5687900058:AAGmBIKKIDAFfLyV0i6IVKP58XVZM2hXerg')
text_info = 'Данный бот позволит Вам познакомиться с интересными местами Санкт-Петербурга !\n\n'




def get_user_photo(message):
    markup = types.InlineKeyboardMarkup()  # базовая кнопка
    markup.add(types.InlineKeyboardButton("посетить веб-сайт Русского музея",
                                          url="http://en.rusmuseum.ru/"))  # переходим на сайт русского музея
    bot.send_message(message.chat.id, "вот сайт русского музея, посети его", reply_markup=markup)
    bd = False


@bot.message_handler(commands=['start'])
def get_user_photo(message):
    message_text = 'Привет, *' + str(message.chat.first_name) + '*!\n'
    message_text += text_info

    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    weather = types.KeyboardButton(
        emoji.emojize('Прогноз погоды в Питере :sun:'))  # кнопки в самой панели, не встроенные в сообщения
    start = types.KeyboardButton('/start')  # кнопки в самой панели, не встроенные в сообщения
    where_to_go = types.KeyboardButton(emoji.emojize('куда сходить? :classical_building:'))
    where_to_stay = types.KeyboardButton(emoji.emojize('где остановиться? :hotel:'))
    where_to_eat = types.KeyboardButton(emoji.emojize('где поесть? :pot_of_food:'))
    metro = types.KeyboardButton(emoji.emojize('транспорт :bus:'))
    where_to_shop = types.KeyboardButton(emoji.emojize('торговые центры:shopping_bags:'))
    airplane = types.KeyboardButton(emoji.emojize('авиабилеты:airplane:'))
    free_search = types.KeyboardButton('свободный поиск по организациям')
    markup1.add(weather, where_to_stay, where_to_go, where_to_eat, where_to_shop, metro, airplane,free_search, start)
    bot.send_message(message.chat.id, message_text, reply_markup=markup1)


@bot.message_handler(content_types=['text'])
def getUserMessage(user_message):
    bd = False
    # bot.send_message(user_message.chat.id, user_message.text, parse_mode='html') #делаем так, чтобы бот писал именно сам текст, если написать просто user_message,
    # отправит кучу информации
    if (user_message.text == "hello"):
        mess = f'hello, {user_message.from_user.first_name} , my dear'  # здoроваемся
        bot.send_message(user_message.chat.id, mess, parse_mode='html')
    elif (user_message.text == emoji.emojize('транспорт :bus:')):
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        metro = types.KeyboardButton(emoji.emojize('Метро :metro:'))
        trolleibus = types.KeyboardButton(emoji.emojize('Троллейбусы 🚎'))
        bus = types.KeyboardButton(emoji.emojize('Трамваи :tram:'))
        tarif = types.KeyboardButton('Тарифы')
        card = types.KeyboardButton('Пополнить проездной')
        back = types.KeyboardButton('в главное меню')
        markup1.add(metro, trolleibus, bus, tarif, card, back)
        bot.send_message(user_message.chat.id, "вы перешли в меню транспорт", reply_markup=markup1)

    elif (user_message.text == emoji.emojize('Троллейбусы 🚎')):
        bot.send_photo(user_message.chat.id, "https://transphoto.org/photo/08/83/99/883994.png")
    elif (user_message.text == emoji.emojize('Трамваи :tram:')):
        bot.send_photo(user_message.chat.id, "https://transphoto.org/photo/12/56/49/1256499.png?1")




    elif (user_message.text == emoji.emojize('куда сходить? :classical_building:')):
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        sobory = types.KeyboardButton(emoji.emojize('соборы :church:'))
        museums = types.KeyboardButton(
            emoji.emojize('музеи :classical_building:'))  # кнопки в самой панели, не встроенные в сообщения
        parks = types.KeyboardButton(emoji.emojize('парки :national_park:'))
        skulptures = types.KeyboardButton(emoji.emojize('памятники :fountain:'))
        bridges = types.KeyboardButton(emoji.emojize('мосты :bridge_at_night:'))
        cinema = types.KeyboardButton(emoji.emojize('кино :cinema:'))
        map = types.KeyboardButton(emoji.emojize('карта мест :round_pushpin:'))
        back = types.KeyboardButton('в главное меню')
        markup1.add(sobory, museums, parks, skulptures, bridges, map, cinema, back)
        bot.send_message(user_message.chat.id, "вы перешли в меню куда сходить", reply_markup=markup1)


    elif (user_message.text == emoji.emojize('мосты :bridge_at_night:')):
        bridgesmas = ["Александра Невского", "Биржевой", "Благовещенский", "Большеохтинский", "Володарский",
                      "Дворцовый", "Литейный", "Троицкий", "Тучков"]

        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for bridge in bridgesmas:
            bridge = types.KeyboardButton(bridge)
            markup1.add(bridge)

        bridges = types.KeyboardButton('график разведения мостов')
        where_to_go = types.KeyboardButton(emoji.emojize('куда сходить? :classical_building:'))
        back = types.KeyboardButton('в главное меню')
        markup1.add(bridges, where_to_go, back)
        bot.send_message(user_message.chat.id, "вы перешли в меню мосты", reply_markup=markup1)

    elif (user_message.text == "график разведения мостов"):
        bot.send_photo(user_message.chat.id,
                       "https://peterburg.center/sites/default/files/styles/long_image/public/razvod-mostov-2021.png?itok=dAKCuKUT")

    elif (user_message.text == emoji.emojize('кино :cinema:')):
        url_place = " https://kudago.com/public-api/v1.4/places/?lang=&fields" \
                    "=&expand=&order_by=&text_format=&ids=&location=spb&has_showings=&showing_since=" \
                    "1444385206&showing_until=1444385206&categories=cinema&lon=&lat=&radius="
        text = send_info_about_places(url_place)
        bot.send_message(user_message.chat.id, text)

    elif (user_message.text == emoji.emojize('соборы :church:')):

        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        for i in churches:
            church = types.KeyboardButton(i)
            markup1.add(church)
        back = types.KeyboardButton('в главное меню')
        where_to_go = types.KeyboardButton(emoji.emojize('куда сходить? :classical_building:'))
        markup1.add(where_to_go, back)
        bot.send_message(user_message.chat.id, "вы перешли в меню соборы", reply_markup=markup1)


    elif (user_message.text == emoji.emojize('парки :national_park:')):
        bd = True
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)

        parks = ["Марсово поле", "Петергоф",
                 "Екатерининский парк", "Парк на Елагином острове", "Александровский парк", "Александровский сад",
                 "Летний сад", "Парк 300-летия Санкт-Петербурга", "Московский Парк Победы", "Охта Парк",
                 "Лапландия Парк", "Михайловский сад", "Новая Голландия"
            , "Парк Дубки", "Андерсенград", "Таврический сад"
            , "Приморский парк Победы", "Музей-усадьба Державина", "Сад 9 января", "Муринский парк"
                 ]

        for i in parks:
            park = types.KeyboardButton(i)
            markup1.add(park)
        back = types.KeyboardButton('в главное меню')
        where_to_go = types.KeyboardButton(emoji.emojize('куда сходить? :classical_building:'))
        markup1.add(where_to_go, back)
        bot.send_message(user_message.chat.id, "вы перешли в меню парки", reply_markup=markup1)

    elif (user_message.text == "в главное меню"):
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        weather = types.KeyboardButton(emoji.emojize('Прогноз погоды в Питере :sun:'))
        start = types.KeyboardButton('/start')  # кнопки в самой панели, не встроенные в сообщения
        where_to_go = types.KeyboardButton(emoji.emojize('куда сходить? :classical_building:'))
        where_to_stay = types.KeyboardButton(emoji.emojize('где остановиться? :hotel:'))
        where_to_eat = types.KeyboardButton(emoji.emojize('где поесть? :pot_of_food:'))
        where_to_shop = types.KeyboardButton(emoji.emojize('торговые центры:shopping_bags:'))
        metro = types.KeyboardButton(emoji.emojize('транспорт :bus:'))
        airplane = types.KeyboardButton(emoji.emojize('авиабилеты:airplane:'))
        free_search = types.KeyboardButton('свободный поиск по организациям')
        markup1.add(weather, where_to_stay, where_to_go, where_to_eat, where_to_shop, metro, airplane, free_search, start)
        bot.send_message(user_message.chat.id, "вы вернулись в главное меню", reply_markup=markup1)
    elif (user_message.text == "пока"):
        bot.send_message(user_message.chat.id, "и тебе пока", parse_mode='html')
    elif (user_message.text == "id"):
        bot.send_message(user_message.chat.id, f'your id: {user_message.from_user.id}', parse_mode='html')
    elif (user_message.text == "свободный поиск по организациям"):
        bot.send_message(user_message.chat.id, text="Вы можете найти интересующую вас ОРГАНИЗАЦИЮ в Санкт-Петербурге, введя запрос , начинающийся со слова НАЙДИ"
                                                    "пример : Найди Вкусно - и Точка ")




    elif (user_message.text == emoji.emojize("авиабилеты:airplane:")):

        bot.send_message(user_message.chat.id, '''Введи через пробел город отправления(только Российские), город назначения и дату вылета, 
        например :Москва Санкт-Петербург 2022-12-31''')


    elif (user_message.text.find(" ") != -1 and user_message.text.find("2") != -1):
        try:
            t = user_message.text.split()
            aviasales_token = "cb614ccdbe22289b22511e54c8e02fc9"
            information = get_info_flight(user_message.text)
            origin = information[0]
            destination = information[1]
            departure_at = information[2]
            print(f'origin is {origin}')
            print(f'dest is {destination}')
            print(f'departure at {departure_at}')

            url = f'''https://api.travelpayouts.com/aviasales/v3/prices_for_dates?origin={origin}&destination={destination}&currency=rub&departure_at={departure_at}&
                                                            return_at={departure_at}&sorting=price&direct=true&limit=10&token={aviasales_token}'''

            response = requests.get(url)
            info = json.loads(response.text)
            price = info["data"][0]["price"]
            link = "https://www.aviasales.ru" + (str)(info["data"][0]["link"])
            text = f"билеты  {t[0]} --{t[1]} от {price} рублей на дату: {departure_at} "
            keyboard = types.InlineKeyboardMarkup()
            url_button = types.InlineKeyboardButton(text="подробнее", url=link)
            keyboard.add(url_button)
            bot.send_message(user_message.chat.id, text, reply_markup=keyboard)

        except Exception as e:
            bot.send_message(user_message.chat.id, "не удалось найти авиабилеты по указанным данным")
            print(e)





    elif ((user_message.text.lower().find("найди")!=-1)):
        organization = user_message.text[user_message.text.find('и', 1): len(user_message.text)]
        text=get_info_about_organizations(organization)
        bot.send_message(user_message.chat.id, text)


    elif (user_message.text == "info"):
        bot.send_message(user_message.chat.id, "и тебе пока", parse_mode='html')
    elif (user_message.text == emoji.emojize('Метро :metro:')):
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        scheme = types.KeyboardButton('Схема метро')  # кнопки в самой панели, не встроенные в сообщения
        time = types.KeyboardButton('Режим работы станций')  # кнопки в самой панели, не встроенные в сообщения
        transport = types.KeyboardButton(emoji.emojize('транспорт :bus:'))
        back = types.KeyboardButton('в главное меню')
        markup1.add(scheme, time, transport, back)
        bot.send_message(user_message.chat.id, "Вы перешли в меню метро", reply_markup=markup1)

    elif (user_message.text == emoji.emojize('музеи :classical_building:')):

        text = '[музеи](https://www.culture.ru/museums/institutes/location-sankt-peterburg?ysclid=l891xtiuj7335039208)'
        bot.send_message(user_message.chat.id, text, parse_mode='MarkdownV2')


    elif (user_message.text == emoji.emojize('памятники :fountain:')):
        text = '[памятники](https://peterburg.center/category/pamyatniki?ysclid=l8a1uhdnii583269947)'
        bot.send_message(user_message.chat.id, text, parse_mode='MarkdownV2')

    elif (user_message.text == emoji.emojize('где поесть? :pot_of_food:')):
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        restaurants = types.KeyboardButton(emoji.emojize('рестораны 🥘'))
        fastfood = types.KeyboardButton(emoji.emojize('фастфуд :hamburger:'))
        national_kitchen = types.KeyboardButton(emoji.emojize('азиатская кухня 🍱'))
        kafe = types.KeyboardButton(emoji.emojize('кафе :doughnut:'))
        back = types.KeyboardButton('в главное меню')
        markup1.add(restaurants, fastfood, national_kitchen, kafe, back)
        bot.send_message(user_message.chat.id, "вы перешли в меню где поесть\n Выбери категорию заведения, и бот "
                                               "порекомендует тебе место", reply_markup=markup1)

    elif (user_message.text == emoji.emojize('где остановиться? :hotel:')):
        markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        hotel = types.KeyboardButton(emoji.emojize('отели :hotel:'))
        hostel = types.KeyboardButton(emoji.emojize('хостелы :bed:'))
        arend = types.KeyboardButton(emoji.emojize('арендовать жильё :house:'))
        back = types.KeyboardButton('в главное меню')
        markup1.add(hotel, hostel, arend, back)
        bot.send_message(user_message.chat.id, "вы перешли в меню где остановиться \n Выбери категорию заведения, и бот "
                                               "порекомендует тебе место", reply_markup=markup1)


    elif (user_message.text == emoji.emojize('фастфуд :hamburger:')):
        bot.send_message(user_message.chat.id, text = get_info_about_organizations("Фастфуд"))
    elif (user_message.text == emoji.emojize('азиатская кухня 🍱')):
        bot.send_message(user_message.chat.id, text = get_info_about_organizations("Азиатская кухня"))




    elif (user_message.text == emoji.emojize('Прогноз погоды в Питере :sun:')):
        get_weather()
        my_file = open("BabyFile.txt", "r")
        prognos = my_file.read()
        bot.send_message(user_message.chat.id, prognos)
    elif (user_message.text == emoji.emojize('Схема метро')):
        photo = open('photos/metro.jpg', 'rb')
        bot.send_photo(user_message.chat.id, photo)  # отправляем фото
    elif (user_message.text == emoji.emojize('Тарифы')):
        bot.send_photo(user_message.chat.id, 'http://www.metro.spb.ru/uploads/tarif2022_1.jpg')  # отправляем фото
    elif (user_message.text == emoji.emojize('Пополнить проездной')):
        text = '[пополнить проездной](http://www.metro.spb.ru/bzoplata.html?ysclid=l88hx9ekrf653992473)'
        bot.send_message(user_message.chat.id, text, parse_mode='MarkdownV2')


    elif (user_message.text == emoji.emojize('карта мест :round_pushpin:')):
        text = '[карта мест](https://yandex.ru/maps/2/saint-petersburg/category/landmark_attraction/89683368508/?ll=30.433514%2C59.899008&sll=30.433514%2C59.898920&z=11)'
        bot.send_message(user_message.chat.id, text, parse_mode='MarkdownV2')

    elif ((user_message.text in ["Александра Невского", "Биржевой", "Благовещенский", "Большеохтинский", "Володарский",
                                 "Дворцовый", "Литейный", "Троицкий", "Тучков"])):
        try:
            link = bridge_inf(user_message.text)
            bot.send_photo(user_message.chat.id, link, user_message.text)
        except (Exception, Error) as error:
            print("Error", error)
    elif (user_message.text == emoji.emojize('Режим работы станций')):
        text = '[режим работы станций](http://www.metro.spb.ru/rejimrabotystancii.html?ysclid=l81yz39056997330556)'
        bot.send_message(user_message.chat.id, text, parse_mode='MarkdownV2')

    elif (user_message.text == emoji.emojize('рестораны 🥘')):
        bot.send_message(user_message.chat.id, text = get_info_about_organizations("Рестораны"))
    elif (user_message.text == emoji.emojize('хостелы :bed:')):
        bot.send_message(user_message.chat.id, text = get_info_about_organizations("Хостелы"))
    elif (user_message.text == emoji.emojize('отели :hotel:')):
        bot.send_message(user_message.chat.id, text = get_info_about_organizations("Отели"))

    elif (user_message.text == emoji.emojize('кафе :doughnut:')):
        bot.send_message(user_message.chat.id, text = get_info_about_organizations("Кафе"))

    elif (user_message.text == emoji.emojize('торговые центры:shopping_bags:')):
        bot.send_message(user_message.chat.id, text =  get_info_about_organizations("торговые центры"))



    elif ((user_message.text in churches) or (user_message.text != "")):
        try:
            text = get_info_of_sightsee(user_message.text)
            text1 = f'{text[0]}\n'
            url = text[1]
            web_site = text[2]
            text = text1 + f' подробнее : {web_site}'
            bot.send_photo(user_message.chat.id, url, text)

        except (Exception, Error) as error:
            print("Error", error)


    else:

        bot.send_message(user_message.chat.id, "я тебя не понимаю", parse_mode='html')


@bot.message_handler(content_types=['photo'])
def get_user_photo(message):
    bot.send_message(message.chat.id, "ВАУ, крутое фото!", parse_mode='html')


bot.polling(none_stop=True)
