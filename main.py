from telebot import TeleBot, types
from globus import get_product_categories_from_site, get_products_from_site


bot_token = '6066369963:AAH15Wm3IO52m_6pubxSPBTXSk4oJPjBcB8'
bot = TeleBot(token=bot_token)
shops = [
    {
        'name': 'Globus',
        'site': 'https://globus-online.kg'
    },
    {
        'name': 'Фрунзе',
        'site': 'https://online.gipermarket.kg'
    },
]
welcome_text = 'Здравствуйте, выберите супермаркет'
categories = []
category_ids = []


@bot.message_handler(commands=['start'])
def get_shops(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(*[shop.get('name') for shop in shops])

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_product_categories(message):
    if message.text == shops[0]['name']: # Globus
        get_product_categories_from_site(categories, shops[0]['site'])

        markup = types.InlineKeyboardMarkup()
        for category in categories:
            category_ids.append(category.get('id'))
            button = types.InlineKeyboardButton(category.get('name'), 
                                                callback_data=category.get('id'))
            markup.add(button)

        bot.send_message(message.chat.id, 'Список категории', reply_markup=markup)

    elif message.text == shops[1]['name']: # Фрунзе
        pass
    else:
        bot.send_message(message.chat.id, 'Выберите супермаркет')


@bot.callback_query_handler(lambda query: query.data in category_ids)
def callback_categories_handler(query):
    for category in categories:
        if category.get('id') == query.data:
            if category.get('sub_categories'):
                markup = types.InlineKeyboardMarkup()
                for sub_c in category.get('sub_categories'):
                    button = types.InlineKeyboardButton(
                        sub_c.get('name'), callback_data=sub_c.get('id')
                    )
                    markup.add(button)
                
                bot.send_message(
                    query.from_user.id, 'Список под категории',  reply_markup=markup,
                )
            else:
                get_products_from_site(url=shops[0].get('site'))


bot.infinity_polling()
