import config
import SQL_mode
import dict_cod
import telebot
from telebot import types
from dataclasses import dataclass

# Создаем бота
bot = telebot.TeleBot(config.token)#load tokin chat bot


def Creat_NameButton(list_name):
    keyboard = types.InlineKeyboardMarkup()
    for NameButton in list_name:
        callback_button = types.InlineKeyboardButton(text=NameButton, callback_data=NameButton)
        keyboard.add(callback_button)
    return keyboard

# Команда start
@bot.message_handler(commands=["start"])
def start(message):
    id_user = message.from_user.id
    cod = SQL_mode.ControlUser(id_user)
    result = dict_cod.dict_cod_result[cod](message)

    text_message = result['text_message']
    list_name_button = result['list_name_button']

    keyboard = Creat_NameButton(list_name_button)
    bot.send_message(message.chat.id, text_message, reply_markup=keyboard)

@bot.message_handler(commands=["new_game"])
def new_game(message):
    bot.send_message(141029496, 'очень круто! Спасибо за сотрудничество!')

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    cod = call.data
    message = call.message
    result = dict_cod.dict_cod_result[cod](message)
    bot.send_message(message.chat.id, result)

# Запускаем бота
bot.polling(none_stop=True, interval=0)
