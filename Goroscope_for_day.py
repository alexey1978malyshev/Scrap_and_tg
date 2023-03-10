import requests
import lxml
from bs4 import BeautifulSoup as b
import telebot
from telebot import types
import time
import schedule
from datetime import datetime
from threading import Thread

URL = 'https://maykop.retrofm.ru/'
API_KEY = '6044839241:AAG9Xp704t2E73B79jPprVap-Fq_t6vt5T4'


# session = requests.Session()                      вариант постоянного соединения
# adapter = requests.adapters.HTTPAdapter(
#     pool_connections=100,
#     pool_maxsize=100)
# session.mount('http://', adapter)
# count = session.params
# r = requests.get(URL)
# soup = b(r.text, 'lxml')

def request_url(url):
    request = requests.get(URL)  # запрос содержимого страницы сайта
    soup = b(request.text, 'lxml')  # создание объекта bs4
    return soup


soup = request_url(URL)

all_zodiac_info = soup.find(class_="index_horoscope_list").find_all('div')
zodiac_info_list = []
znak = {}

for item in all_zodiac_info:
    zodiac_info_list.append(item.text)

# print(title.text)
# print(r.text )# получение HTML кода
# print(zodiac_info_list)

# пишем бота

bot = telebot.TeleBot(API_KEY)
date = time.strftime("%d %B")


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет! Чтобы получить гороскоп нажми на свой знак зодиака: ',
                     reply_markup=create_keys())


@bot.message_handler(content_types=['text'])
def get_goroscope(message):
    bot.send_message(message.chat.id, f'Гороскоп на {time.strftime("%d %B")}: ')
    znak = {
        '♈ Овен': zodiac_info_list[0],
        '♉ Телец': zodiac_info_list[1],
        '♊ Близнецы': zodiac_info_list[2],
        '♋ Рак': zodiac_info_list[3],
        '♌ Лев': zodiac_info_list[4],
        '♍ Дева': zodiac_info_list[5],
        '♎ Весы': zodiac_info_list[6],
        '♏ Скорпион': zodiac_info_list[7],
        '♐ Стрелец': zodiac_info_list[8],
        '♑ Козерог': zodiac_info_list[9],
        '♒ Водолей': zodiac_info_list[10],
        '♓ Рыбы': zodiac_info_list[11]
    }
    # input_message = message.text.lower()

    try:
        bot.send_message(message.chat.id, znak[message.text], reply_markup=create_keys())
        who_was = bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        print(datetime.now())
        print(message.text)
        print(f"id: {who_was.user.id} ---- имя: {who_was.user.first_name} ---- никнейм: {who_was.user.username}")
    except:

        bot.send_message(message.chat.id, f"""Ууупс... что то пошло не так... во всем виноваты иллюминаты и бури на 
        солнце... не нажать ли <b>/start </b>?
        
                  ... <b>или кнопку со своим знаком зодиака</b>...""", parse_mode='html')
        print('---------------\nex: ' + message.text + '\n---------------')


def create_keys():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for z in znak:
        btn = types.KeyboardButton(znak.keys())
        markup.add(btn)
    return markup


# запуск функции по расписанию
def starter():
    schedule.every().day.at('00:01').do(request_url(URL))
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    # t2 = threading.Thread(target=starter)  # запуск ф-ии starter в отдельном потоке
    # t2.start()
    bot.polling(non_stop=True)
