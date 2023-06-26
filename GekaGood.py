import config
import SQL_mode
import dict_cod
import telebot
from telebot import types

# Создаем бота
bot = telebot.TeleBot(config.token)#load tokin chat bot

#Edit
#COD_WORK_WHITH_USERS_BUTTON = False

def Creat_NameButton(list_name):
    keyboard = types.InlineKeyboardMarkup()
    for NameButton in list_name:
        callback_button = types.InlineKeyboardButton(text=NameButton[0], callback_data=NameButton[1])
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
    CHAT_ID = message.from_user.id
    fetchall = SQL_mode.New_game(CHAT_ID)
    if fetchall == None:
        bot.send_message(CHAT_ID, 'Список участников пуст.')
    keyboard = Creat_NameButton(fetchall)
    text_message = 'С кем вы хотите сыграить?'
    # Edit
    # COD_WORK_WHITH_USERS_BUTTON = '12_01'
    bot.send_message(message.chat.id, text_message, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    cod = call.data
    message = call.message
    result_req = dict_cod.dict_cod_result.get(cod)
    # Кнопки с именами ползователей в возвратных данных (cod) содержет ID их чата...
    # ...т.е. на них нет кода в справочнике
    if result_req is None:
        cod_button = str(cod[:7])
        result_req = dict_cod.dict_cod_result.get(cod_button)
        if result_req is None:
            result = dict_cod.dict_cod_result.get('12_001_')(message)
            chat_id = cod
            bot.send_message(message.chat.id, 'Приглашение отправлено')
        else:
            chat_id = str(cod[7:])
            result = result_req((message, chat_id))
            if isinstance(result, list) == False:
                if result.get('chat_id') is not None:
                    chat_id = result.get('chat_id')
    else:
        result = result_req(message)
        chat_id = message.chat.id
    if isinstance(result, list):
        for res in result:
            text_message = res['text_message']
            list_name_button = res['list_name_button']
            chat_id = res['chat_id']

            keyboard = Creat_NameButton(list_name_button)
            bot.send_message(chat_id, text_message, reply_markup=keyboard)
    else:
        text_message = result['text_message']
        list_name_button = result['list_name_button']

        keyboard = Creat_NameButton(list_name_button)
        bot.send_message(chat_id, text_message, reply_markup=keyboard)

#Edit
# COD_WORK_WHITH_USERS_BUTTON = False

# Запускаем бота
bot.polling(none_stop=True, interval=0)
