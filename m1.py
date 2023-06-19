import telebot
import config

from telebot import types

#Первый набор кнопок
fgb   = ['1. Торговое здание','2. Административный комплекс','3. Жилой комплекс','4. Офисное здание','5. Складское помещение/комплекс']
#Кнопки Да/Нет
ButtonYN = ['Есть','Нет']

answer = {'Недвижимость':'','Площадь':'','Документация':'','Тех.задание':'','Телефон':''}
# Создаем бота
bot = telebot.TeleBot(config.token)#load tokin chat bot

# Команда start
@bot.message_handler(commands=["start"])
def start(message):
    keyboard = types.InlineKeyboardMarkup()
    for NameButton in fgb:
        callback_button = types.InlineKeyboardButton(text=NameButton, callback_data=NameButton)
        keyboard.add(callback_button)
    bot.send_message(message.chat.id, 'Выберите недвижимость по происхождению и масштабности ', reply_markup=keyboard)

# В большинстве случаев целесообразно разбить этот хэндлер на несколько маленьких
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    global answer;
    message_text = call.data
    if call.message:
        if message_text in fgb:
            answer['Недвижимость'] = message_text
            secon_que(call)
        elif message_text.find('Документация') != -1:
            fourth_que(call)
        elif message_text.find('ТехЗадание') != -1:
            fifth_que(call)
        else:
            bot.send_message(call.message.chat.id, 'Опс! Произошла какая-то ошибка!')
def secon_que(call):
    # Добавляем  кнопки 2
    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    global answer;
    message = call.message
    answer['Недвижимость'] = call.data
    null_buton = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Напишите площадь объекта аудита',reply_markup=null_buton)
    bot.register_next_step_handler(message, third_que)

def third_que(message):
    # Добавляем  кнопки 3
    global answer;

    answer['Площадь'] = message.text

    keyboard = types.InlineKeyboardMarkup()
    for NameButton in ButtonYN:
        val_but = 'Документация '+ str(NameButton)
        callback_button = types.InlineKeyboardButton(text=NameButton, callback_data=val_but)
        keyboard.add(callback_button)
    bot.send_message(message.chat.id, 'Есть ли у вас документация?', reply_markup=keyboard)

def fourth_que(call):
    # Добавляем  кнопки 4
    global answer;
    message = call.message
    answer['Документация'] = call.data

    keyboard = types.InlineKeyboardMarkup()
    for NameButton in ButtonYN:
        val_but = 'ТехЗадание ' + str(NameButton)
        callback_button = types.InlineKeyboardButton(text=NameButton, callback_data=val_but)
        keyboard.add(callback_button)
    bot.send_message(message.chat.id, 'Есть ли у вас техническое задание?', reply_markup=keyboard)

def fifth_que(call):
    global answer;
    message = call.message
    answer['Тех.задание'] = call.data

    null_buton = telebot.types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, 'Можете оставить свой номер телефона. \nНаш специалист свяжется с вами и проконсультирует по вопросам обследования. ',reply_markup=null_buton)
    bot.register_next_step_handler(message, final_que);

def final_que(message):
    global answer;
    x =1
    answer['Телефон'] = message.text
    bot.send_message(message.chat.id, 'Ваш запрос передан специалисту')
    f = open('data.txt','r')
    old_lis_f = []
    for line in f:
        old_lis_f.append(line)
    f = open('data.txt', 'w')
    for data in old_lis_f:
        f.write(str(data))
    f.write(str(answer)+'\n')
    f.close()

    # Запускаем бота
bot.polling(none_stop=True, interval=0)