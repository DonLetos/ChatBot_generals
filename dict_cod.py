import SQL_mode
import random

ORIGIN_RANGE = range(1,10)

def it_ok(message):
    text = f'Здравствуйте, {message.from_user.full_name}!'
    return {'text_message': text, 'list_name_button': []}


def user_not_found(message):
    text = (f'{message.from_user.full_name}'
            ', ваш пользователь не зарегестрирован в базе.')
    name_button = [('Зарегистрироваться', 'Зарегистрироваться')]
    return {'text_message': text, 'list_name_button': name_button}


def registration(message):
    id_user = message.chat.id
    cod = SQL_mode.ControlUser(id_user)
    if cod == 404:
        text_result_request = SQL_mode.CreatUser(message)
        return {'text_message': text_result_request, 'list_name_button': []}
    elif cod == 200:
        text = 'Ваш пользователь уже зарегистрирован.'
        return {'text_message': text, 'list_name_button': []}


def Start_new_game(message: tuple = tuple()):
    message, id_game = message
    turn = SQL_mode.TurnGame(id_game)
    randon_element = random.choice(ORIGIN_RANGE)

    it_turn_first_player = turn[6]
    id_game = turn[-1]
    randon_element = 100
    if it_turn_first_player:
        score = randon_element + turn[2]
        chat_id = turn[0]
    else:
        score = randon_element + turn[3]
        chat_id = turn[1]
    if score > 20:
        text = SQL_mode.EndGame(id_game)
        text = f'{text} ваш результат {score}'
    else:
        pass

    return {'text_message': text, 'list_name_button': [], 'chat_id': chat_id}


def Sent_invite(message):
    #message = message.message
    text = f' Пользователь {message.chat.first_name} {message.chat.last_name} приглашает вас на игру'
    name_button = [
                   ('Принять', f'12_002_{message.chat.id}'),
                   ('Отклонить', f'12_003_{message.chat.id}')
                  ]
    return {'text_message': text, 'list_name_button': name_button}

def Accept_invitation(message):
    result = SQL_mode.CreatGame(message)
    message, master_id_chat = message
    text = (f' Пользователь {message.chat.first_name} {message.chat.last_name} принял ваше приглашение.'
           f' Кто будет ходить первый?')
    name_button = [
                   ('Я', f'33_001_{result}'),
                   ('НЕ Я', f'33_002_{result}')
                  ]
    return {'text_message': text, 'list_name_button': name_button}

def Decline_the_invitation(message):
    text = f' Пользователь {message.chat.first_name} {message.chat.last_name} отклонил ваше приглашение'
    return {'text_message': text, 'list_name_button': []}


dict_cod_result = {200: it_ok,
                   404: user_not_found,
                   'Зарегистрироваться': registration,
                   '12_001_': Sent_invite,
                   '12_002_': Accept_invitation,
                   '12_003_': Decline_the_invitation,
                   '33_001_': Start_new_game,
                   '33_002_': Start_new_game
            }
