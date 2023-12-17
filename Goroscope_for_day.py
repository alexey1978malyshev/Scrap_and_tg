import random

import requests
import lxml
from bs4 import BeautifulSoup as b
import telebot
from telebot import types
import time
import schedule
from datetime import datetime
import threading
from threading import Thread

URL = 'https://maykop.retrofm.ru/'
URL1 = 'https://www.forbes.ru/forbeslife/dosug/262327-na-vse-vremena-100-vdokhnovlyayushchikh-tsitat'
API_KEY = '6044839241:AAG9Xp704t2E73B79jPprVap-Fq_t6vt5T4'

zodiac_info_list = []
quotes_list = []


def request_url(url, url1):
    zodiac_info_list.clear()
    request = requests.get(URL)
    request_1 = requests.get(URL1)  # запрос содержимого страницы сайта
    # global soup, soup1
    soup = b(request.text, 'lxml')  # создание объекта bs4
    soup1 = b(request_1.text, 'lxml')  # создание объекта bs4
    print(datetime.now())
    print(f"{request.status_code} : 'гороскоп'")
    print(f"{request_1.status_code} : 'цитаты'")

    # return soup, soup1
    def do_lists():
        all_zodiac_info = soup.find(class_="index_horoscope_list").find_all('div')
        all_quotes = soup1.find(class_="CFaZ3").find_all('span')
        # all_autors_of_quotes = soup1.find(class_="CFaZ3").find_next('span')

        for item in all_zodiac_info:
            zodiac_info_list.append(item.text)

        for item in all_quotes:
            quotes_list.append(item.text)
        return zodiac_info_list, quotes_list

    do_lists()


request_url(URL, URL1)

print(zodiac_info_list)

short_quotes_list = []
for i in range(len(quotes_list)):
    if i % 2 == 0:
        quotes_list[i] = quotes_list[i][3:]  # Убираем номера цитат, т.к каждая цитата в списке начинается с номера,
        short_quotes_list.append(
            quotes_list[i] + '\n' + quotes_list[i + 1])  # затем объединяем цитату и автора в один элемент списка:

random.shuffle(short_quotes_list)
print(short_quotes_list)

# print(title.text)
# print(r.text )# получение HTML кода
# print(zodiac_info_list)

# пишем бота

bot = telebot.TeleBot(API_KEY)
date = time.strftime("%d %B")


def create_goroscope_keys():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

    btn1 = types.KeyboardButton('♈ Овен')
    btn2 = types.KeyboardButton('♉ Телец')
    btn3 = types.KeyboardButton('♊ Близнецы')
    btn4 = types.KeyboardButton('♋ Рак')
    btn5 = types.KeyboardButton('♌ Лев')
    btn6 = types.KeyboardButton('♍ Дева')
    btn7 = types.KeyboardButton('♎ Весы')
    btn8 = types.KeyboardButton('♏ Скорпион')
    btn9 = types.KeyboardButton('♐ Стрелец')
    btn10 = types.KeyboardButton('♑ Козерог')
    btn11 = types.KeyboardButton('♒ Водолей')
    btn12 = types.KeyboardButton('♓ Рыбы')
    # for z in znak_btn:                    #добавление кнопки в цикле(не работает)
    #     btn = types.KeyboardButton(z)
    #     markup.add(btn)
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12)

    return markup


# def create_quotes_keys():
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
#     btn13 = types.KeyboardButton('Цитата на день. Жми!')
#     markup.add(btn13)
#     return markup


@bot.message_handler(commands=['start'])
def hello(message):
    bot.send_message(message.chat.id, 'Привет! Чтобы получить гороскоп нажми на свой знак зодиака: ',
                     reply_markup=create_goroscope_keys())


@bot.message_handler(content_types=['text'])
def get_goroscope(message):
    bot.send_message(message.chat.id, f'<b>Гороскоп на {time.strftime("%d %B")}:</b> ', parse_mode="html")
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
    # qoute =
    # znak_btn = []
    # for z in znak.keys():
    #     znak_btn.append(z)
    #     print(znak_btn)
    # input_message = message.text.lower()

    try:
        bot.send_message(message.chat.id, znak[message.text], reply_markup=create_goroscope_keys())
        bot.send_message(message.chat.id,
                         f'<b>Сегодня стоит подумать над этим </b>:\n{short_quotes_list[random.randint(0,100)]}',
                         parse_mode="html", reply_markup=create_goroscope_keys())

        who_was = bot.get_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
        print(datetime.now())
        print(message.text)
        print(f"id: {who_was.user.id} ---- имя: {who_was.user.first_name} ---- никнейм: {who_was.user.username}")
    except:

        bot.send_message(message.chat.id, f"""Ууупс... что то пошло не так... во всем виноваты иллюминаты и бури на солнце
        ... не нажать ли <b>/start </b>?
        
                  ... <b>или кнопку со своим знаком зодиака</b>...""", parse_mode='html')
        print('---------------\nex: ' + message.text + '\n---------------')


# @bot.message_handler(content_types=['text'])
#
#
# def get_quot(message):
#     bot.send_message(message.chat.id, quotes_list[0], reply_markup=create_goroscope_keys())


# TODO добавить продолжение диагога и предложение свежего анекдота или цитаты дня


# запуск функции по расписанию
def starter():
    schedule.every().day.at('00:01').do(request_url, URL, URL1)
    print('soup refreshed')
    while True:
        schedule.run_pending()
        # time.sleep(1)


if __name__ == '__main__':
    t2 = threading.Thread(target=starter)  # запуск ф-ии starter в отдельном потоке
    t2.start()

    bot.polling(non_stop=True)
