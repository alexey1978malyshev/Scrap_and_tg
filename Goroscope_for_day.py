import requests
import lxml
from bs4 import BeautifulSoup as b
import telebot
import time
import schedule
from datetime import datetime
from threading import Thread

URL = 'https://maykop.retrofm.ru/'
API_KEY = '*****************************************'

# session = requests.Session()                      вариант постоянного соединения
# adapter = requests.adapters.HTTPAdapter(
#     pool_connections=100,
#     pool_maxsize=100)
# session.mount('http://', adapter)
# count = session.params
#r = requests.get(URL)
#soup = b(r.text, 'lxml')

def request_url(url):
    request = requests.get(URL)      # запрос содержимого страницы сайта
    soup = b(request.text, 'lxml')   # создание объекта bs4
    return soup

soup = request_url(URL)

all_zodiac_info = soup.find(class_="index_horoscope_list").find_all('div')
zodiac_info_list = []
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
    bot.send_message(message.chat.id, 'Привет! Чтобы получить гороскоп введи свой знак зодиака:')


@bot.message_handler(content_types=['text'])
def get_goroscope(message):
    bot.send_message(message.chat.id, f'Гороскоп на {time.strftime("%d %B")}: ')
    znak = {
        'овен': zodiac_info_list[0],
        'телец': zodiac_info_list[1],
        'близнецы': zodiac_info_list[2],
        'рак': zodiac_info_list[3],
        'лев': zodiac_info_list[4],
        'дева': zodiac_info_list[5],
        'весы': zodiac_info_list[6],
        'скорпион': zodiac_info_list[7],
        'стрелец': zodiac_info_list[8],
        'козерог': zodiac_info_list[9],
        'водолей': zodiac_info_list[10],
        'рыбы': zodiac_info_list[11]
    }
    input_message = message.text.lower()
    if input_message in znak.keys():
        bot.send_message(message.chat.id, znak[message.text.lower()])

    else:
        bot.send_message(message.chat.id, "Извините. Такого знака астрологи пока не придумали, но идея хороша...")


# запуск функции по расписанию
def starter():
    schedule.every().day.at('00:01').do(request_url(URL))
    while True:
        schedule.run_pending()


if __name__ == '__main__':
    t2 = threading.Thread(target=starter)  # запуск ф-ии starter в отдельном потоке
    t2.start()
    bot.polling()
