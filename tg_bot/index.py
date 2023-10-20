import json
import random
import schedule
import telebot
from telebot import types
import time
import threading

from bot_token import token
from data import *
from db.database import get_place, insert_place, new_day


bot = telebot.TeleBot(token)
bot.delete_webhook()
bot.remove_webhook()
bot.set_webhook("https://functions.yandexcloud.net/d4e0fpjghis39cl88um3")


def handler(event, context):
    body = json.loads(event['body'])
    update = telebot.types.Update.de_json(body)
    bot.process_new_updates([update])
    return {
        'statusCode': 200,
        'body': 'ok',
    }


def flag_update():
    schedule.every(24).hours.do(new_day)
    while True:
        schedule.run_pending()
        time.sleep(15)


thread = threading.Thread(target=flag_update, daemon=True)
thread.start()


@bot.message_handler(commands=['start'])
def send_keyboard(message, text='Привет, я бот-путешественник! Я могу предложить тебе место дня,'
                                ' случайное путешествие или дать советы по путешествиям.'
                                ' Выбери одну из кнопок ниже:'):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Место дня')
    itembtn2 = types.KeyboardButton('Случайное путешествие')
    itembtn3 = types.KeyboardButton('Советы по путешествиям')
    keyboard.add(itembtn1, itembtn2, itembtn3)
    bot.send_message(message.from_user.id, text=text, reply_markup=keyboard)


@bot.message_handler(commands=['place_of_the_day'])
@bot.message_handler(func=lambda message: message.text.lower() == 'место дня')
def send_place_of_the_day(message):
    # info = get_place(message) - реализация с бд
    if message.chat.id not in users:
        users[message.chat.id] = dict()
    if users[message.chat.id]:
        current_place, place_flag = users[message.chat.id]['place'], users[message.chat.id]['place_flag']
        if place_flag:
            bot.send_message(message.chat.id, f'Место дня сегодня было обнаружено! Это {current_place}!')
        else:
            # insert_place(message, random.choice(places_to_visit)) - реализация с бд, задеплоить с бд не получилось
            # current_place = get_place(message)[-1][0]
            users[message.chat.id]['place'] = random.choice(places_to_visit)
            users[message.chat.id]['place_flag'] = 1
            current_place = users[message.chat.id]['place']
            bot.send_message(message.chat.id, f'Я считаю, что наикрутейшее место дня сегодня - {current_place}!'
                                                f'И очень советую там побывать!')

    else:
        # insert_place(msg, random.choice(places_to_visit)) - реализация с бд
        users[message.chat.id]['place'] = random.choice(places_to_visit)
        users[message.chat.id]['place_flag'] = 1
        current_place = users[message.chat.id]['place']
        # current_place = get_place(message)[-1][0]
        bot.send_message(message.chat.id, f'Я считаю, что наикрутейшее место дня сегодня - {current_place}!'
                                            f'И очень советую там побывать!')


@bot.message_handler(commands=['random_travel'])
@bot.message_handler(func=lambda message: message.text.lower() == 'случайное путешествие')
def send_random_travel(message):
    place = random.choice(places_to_visit)
    tip = random.choice(travel_tips)
    bot.send_message(message.chat.id, f"Случайное путешествие: {place}. Совет: {tip}")


@bot.message_handler(commands=['travel_tips'])
@bot.message_handler(func=lambda message: message.text.lower() == 'советы по путешествиям')
def send_travel_tips(message):
    tip = random.choice(travel_tips)
    bot.send_message(message.chat.id, f"Совет по путешествиям: {tip}")


# import json
# import random
# import schedule
# import telebot
# from telebot import types
# import time
# import threading
#
# from bot_token import token
# from data import *
# from db.database import get_place, insert_place, new_day
#
#
# bot = telebot.TeleBot(token)
#
# bot.delete_webhook()
# bot.remove_webhook()
# bot.set_webhook("https://functions.yandexcloud.net/d4e0fpjghis39cl88um3")
#
#
# def handler(event, context):
#     if 'body' in event:
#         body = json.loads(event['body'])
#         update = telebot.types.Update.de_json(body)
#         bot.process_new_updates([update])
#     return {
#         'statusCode': 200,
#         'body': 'Hello'
#     }
#
#
# def flag_update():
#     schedule.every(24).hours.do(new_day)
#     while True:
#         schedule.run_pending()
#         time.sleep(15)
#
#
# thread = threading.Thread(target=flag_update, daemon=True)
# thread.start()
#
#
# def callback_worker(call):
#     if call.text.lower() == "место дня":
#         send_place_of_the_day(call)
#     elif call.text.lower() == 'случайное путешествие':
#         send_random_travel(call)
#     elif call.text.lower() == 'советы по путешествиям':
#         send_travel_tips(call)
#     else:
#         msg = bot.send_message(call.chat.id, 'Не знаю такой команды(')
#         bot.register_next_step_handler(msg, callback_worker)
#
#
# @bot.message_handler(commands=['start'])
# def send_keyboard(message, text='Привет, я бот-путешественник! Я могу предложить тебе место дня,'
#                                 ' случайное путешествие или дать советы по путешествиям.'
#                                 ' Выбери одну из кнопок ниже:'):
#     keyboard = types.ReplyKeyboardMarkup(row_width=2)
#     itembtn1 = types.KeyboardButton('Место дня')
#     itembtn2 = types.KeyboardButton('Случайное путешествие')
#     itembtn3 = types.KeyboardButton('Советы по путешествиям')
#     keyboard.add(itembtn1, itembtn2, itembtn3)
#     msg = bot.send_message(message.from_user.id,
#                            text=text, reply_markup=keyboard)
#     bot.register_next_step_handler(msg, callback_worker)
#
#
# @bot.message_handler(commands=['place_of_the_day'])
# @bot.message_handler(func=lambda message: message.text.lower() == 'место дня')
# def send_place_of_the_day(msg):
#     info = get_place(msg)
#     if info:
#         current_place, place_flag = info[-1][0], info[-1][1]
#         if place_flag:
#             msg = bot.send_message(msg.chat.id, f'Место дня сегодня было обнаружено! Это {current_place}!')
#         else:
#             insert_place(msg, random.choice(places_to_visit))
#             current_place = get_place(msg)[-1][0]
#             msg = bot.send_message(msg.chat.id, f'Я считаю, что наикрутейшее место дня сегодня - {current_place}!'
#                                                 f'И очень советую там побывать!')
#
#     else:
#         insert_place(msg, random.choice(places_to_visit))
#
#         current_place = get_place(msg)[-1][0]
#         msg = bot.send_message(msg.chat.id, f'Я считаю, что наикрутейшее место дня сегодня - {current_place}!'
#                                             f'И очень советую там побывать!')
#     bot.register_next_step_handler(msg, callback_worker)
#
#
# @bot.message_handler(commands=['random_travel'])
# @bot.message_handler(func=lambda message: message.text.lower() == 'советы по путешествиям')
# def send_random_travel(message):
#     place = random.choice(places_to_visit)
#     tip = random.choice(travel_tips)
#     bot.send_message(message.chat.id, f"Случайное путешествие: {place}. Совет: {tip}")
#     bot.register_next_step_handler(message, callback_worker)
#
#
# @bot.message_handler(commands=['travel_tips'])
# @bot.message_handler(func=lambda message: message.text.lower() == 'советы по путешествиям')
# def send_travel_tips(message):
#     tip = random.choice(travel_tips)
#     bot.send_message(message.chat.id, f"Совет по путешествиям: {tip}")
#
#
# bot.polling(none_stop=True)
#
#
#