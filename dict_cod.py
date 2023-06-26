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
    # randon_element = 100
    if it_turn_first_player:
        score = randon_element + turn[2]
        chat_id = turn[0]
    else:
        score = randon_element + turn[3]
        chat_id = turn[1]
    if score > 21:
        text = SQL_mode.EndGame(id_game, score)
        name_button = []
    else:
        result = SQL_mode.TernGame_SaveTurn(id_game, it_turn_first_player, score)
        text = result.get('text')
        name_button = result.get('namebutton')
    return {'text_message': text, 'list_name_button': name_button, 'chat_id': chat_id}


def Next_turn_game(message: tuple = tuple()):
    message, id_game = message
    SQL_mes = SQL_mode.NextTurn(id_game)
    if isinstance(SQL_mes, list) == False:
        if SQL_mes.get('error') == False:
            text = (
                f'Ваш ход! \n' 
                f'Вас счет:: 0'
                )
            name_button = [
                            ('TAKE MORE', f'33_001_{id_game}'),
                            ('PASS', f'33_003_{id_game}')
                          ]
        else:
            text = SQL_mes.get('text')
            name_button = []
        return {'text_message': text,
                'list_name_button': name_button,
                'chat_id': SQL_mes.get('chat_id')}
    else:
        return  SQL_mes


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
                   ('Разумеется Я!', f'33_002_{result}')
                  ]
    return {'text_message': text, 'list_name_button': name_button}


def Decline_the_invitation(message: tuple = tuple()):
    message, id_game = message
    text = f' Пользователь {message.chat.first_name} {message.chat.last_name} отклонил ваше приглашение'
    return {'text_message': text, 'list_name_button': []}


dict_cod_result = {200: it_ok,
                   404: user_not_found,
                   'Зарегистрироваться': registration,
                   '12_001_': Sent_invite,
                   '12_002_': Accept_invitation,
                   '12_003_': Decline_the_invitation,
                   '33_001_': Start_new_game,
                   '33_002_': Start_new_game,
                   '33_003_': Next_turn_game
            }
