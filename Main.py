import telebot
from telebot import types

users = []
with open("Data.txt", encoding="utf-8") as file:
    TOKEN = str(file.readline()).rstrip("\n")
    print(TOKEN)
    for x in file:
        print(x)
        users.append(int(x))

bot = telebot.TeleBot(token=TOKEN)
channel_ids = []
content_type = []

@bot.message_handler(commands="new")
def start(message):
    bot.send_message(chat_id=message.chat.id, text="Отлично, тогда начнём \nОтправьте сообщение, которое вы бы хотели переслать")
    bot.register_next_step_handler(message, get_text_messages)


@bot.message_handler(content_types=['text', 'photo'])
def get_text_messages(message):
    if message.from_user.id in users:
        global first_message
        global content_type
        try:
            bot.send_photo(chat_id=message.chat.id, photo=message.photo[len(message.photo) - 1].file_id,
                           caption=message.caption)
            first_message = message
            content_type = "photo"
        except TypeError:
            bot.send_message(chat_id=message.chat.id, text=message.text)
            first_message = message
            content_type = "text"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Yes_B = types.KeyboardButton("Всё верно")
        No_B = types.KeyboardButton("Что-то не то")
        markup.add(Yes_B, No_B)
        bot.send_message(message.chat.id, 'Корректно ли отображается пост?', reply_markup=markup)
        bot.register_next_step_handler(message, button_reply)
        global channel_ids
        channel_ids = []
    else:
        bot.send_message(chat_id=message.chat.id, text='Кто вы? Я вас не знаю. Идите отсюда =)')


def button_reply(message):
    if message.text == 'Всё верно':
        bot.send_message(message.chat.id, 'Ну и супер', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        Channel1 = types.KeyboardButton("тут основной тест")
        Channel2 = types.KeyboardButton("тут копиракр")
        Channel3 = types.KeyboardButton("Channel 3")
        Channel4 = types.KeyboardButton("Channel 4")
        Channel5 = types.KeyboardButton("Channel 5")
        Finish = types.KeyboardButton('Всё')
        markup.add(Channel1, Channel2, Channel3, Channel4, Channel5, Finish)
        bot.send_message(message.chat.id, 'А теперь по одному напишите название канала', reply_markup=markup)
        bot.register_next_step_handler(message, channels)
    elif message.text == 'Что-то не то':
        bot.send_message(message.chat.id, "Ну, тут тогда вам к разработчику", reply_markup=types.ReplyKeyboardRemove())


def channels(message):
    global channel_ids
    if message.text == 'Всё':
         markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
         Button_1 = types.KeyboardButton("Всё правильно")
         Button_2 = types.KeyboardButton("Неа, давай заного")
         markup.add(Button_1, Button_2)
         bot.send_message(chat_id=message.chat.id, text=f'Отправляем в следующие группы? \n {channel_ids}', reply_markup=markup)
         bot.register_next_step_handler(message, send)
    else:
        channel_ids.append(message.text)
        bot.send_message(chat_id=message.chat.id, text="Ещё что-нибудь?")
        bot.register_next_step_handler(message, channels)


def send(message):
    if message.text == "Всё правильно":
        global channel_ids
        print(channel_ids)
        if "тут основной тест" in channel_ids:
            channel_ids.remove("тут основной тест")
            channel_ids.append("-1001540310569")
        if "тут копиракр" in channel_ids:
            channel_ids.remove("тут копиракр")
            channel_ids.append('-1001512308669')
        print(channel_ids)
        for channel_id in channel_ids:
            if content_type == "photo":
                bot.send_photo(chat_id=channel_id, photo=first_message.photo[len(message.photo) - 1].file_id,
                               caption=first_message.caption)
            if content_type == "text":
                bot.send_message(chat_id=channel_id, text=first_message.text)
    elif message.text == "Неа, давай заного":
        bot.message_handler(message, button_reply)


bot.infinity_polling()

