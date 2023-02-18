
# @bot.message_handler(commands=['привет'])
# def say_hello(message):
#     bot.send_message(message.chat.id, 'привет!!!')


# @bot.message_handler(content_types=['text'])
# def reply(message):
#     if message.text.lower() == 'привет':
#         bot.reply_to(message, 'Привет!')
    
#     if message.text.lower() == 'пока':
#         bot.reply_to(message, 'Пока!')

import telebot
from telebot import types
from globus import get_product_categories_from_site


bot_token = '6066369963:AAH15Wm3IO52m_6pubxSPBTXSk4oJPjBcB8'

bot = telebot.TeleBot(token=bot_token)


shops = [
    {
        'name': 'Globus',
        'site': 'https://globus-online.kg/'
    },
    {
        'name': 'Фрунзе',
        'site': 'https://online.gipermarket.kg/'
    },
]
welcome_text = 'Здравствуйте, выберите супермаркет'


@bot.message_handler(commands=['start'])
def get_shops(message):
    murkup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    for shop in shops:
        button = types.KeyboardButton(shop['name'])
        murkup.add(button)

    bot.send_message(message.chat.id, welcome_text, reply_markup=murkup)


@bot.message_handler(content_types=['text'])
def get_product_categories(message):
    if message.text == shops[0]['name']: # Globus
        get_product_categories_from_site(shops[0]['site'])
    elif message.text == shops[1]['name']: # Фрунзе
        pass
    else:
        bot.send_message(message.chat.id, 'Выберите супермаркет')


bot.infinity_polling()
