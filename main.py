import googletrans
import telebot
from googletrans import Translator

import requests

translator = Translator()

bot = telebot.TeleBot('1860568763:AAG_fCsw53jVv6Ch4WzcItUDWCog3b2H_E0')


@bot.message_handler(commands=['start'])
def help_command(message):

    keyboard = telebot.types.InlineKeyboardMarkup()

    keyboard.add(telebot.types.InlineKeyboardButton(text='Связаться с автором', url='telegram.me/u_cant_c_me'))

    bot.send_message(
       message.from_user.id,
       'Привет, @' + message.from_user.username + '! Я бот, который умеет переводить выражения с английского на '
        'русский, и наоборот. Кроме этого, я умею находить произношение английского слова,'
        ' которое вы получили в результате перевода с русского языка. Чтобы начать переводить, введи /translate',
       reply_markup=keyboard
    )

    bot.register_next_step_handler(message, translate)


@bot.message_handler(commands='translate')
def translate(message):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row((telebot.types.KeyboardButton("С английского на русский")),
                 (telebot.types.KeyboardButton("С русского на английский")))

    keyboard.row(telebot.types.KeyboardButton("Вернуться на главную страницу"))
    question = "Выбери вариант перевода:"
    bot.send_message(message.from_user.id,
                     text=question,
                     reply_markup=keyboard)
    bot.register_next_step_handler(message, helping_function)


def helping_function(message):
    keyboard = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id, "Введите текст:", reply_markup=keyboard)
    if message.text == "С английского на русский":
        bot.register_next_step_handler(message, english_translation)
    elif message.text == "С русского на английский":
        bot.register_next_step_handler(message, russian_translation)
    else:
        help_command(message)


import requests


def english_translation(message):
    result = translator.translate(message.text, src='en', dest='ru')
    bot.send_message(message.from_user.id, "Перевод: " + result.text)
    translate(message)


def russian_translation(message):
    result = translator.translate(message.text, src='ru', dest='en')
    keyboard = telebot.types.InlineKeyboardMarkup()
    try:
        req = requests.get("https://api.dictionaryapi.dev/api/v2/entries/{}/{}".format('en_US', result.text))
        keyboard.row((telebot.types.InlineKeyboardButton("Произношение: ",
                                                         url=req.json()[0]["phonetics"][0]["audio"])))
    except:
        keyboard = telebot.types.InlineKeyboardMarkup()

    bot.send_message(message.from_user.id, "Перевод: " + result.text, reply_markup=keyboard)
    translate(message)


bot.polling(none_stop=True, interval=0)