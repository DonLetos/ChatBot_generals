import telebot
import config
import SQL_mode
import dict_cod
from telebot import types
# Создаем бота
bot = telebot.TeleBot(config.token)#load tokin chat bot


# Команда start
@bot.message_handler(commands=["start"])
def start(message):
    id_user = message.from_user.id
    cod = SQL_mode.ControlUser(id_user)
    text_message = dict_cod.dict_cod[cod](message)
    keyboard = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, text_message, reply_markup=keyboard)

# Запускаем бота
bot.polling(none_stop=True, interval=0)
