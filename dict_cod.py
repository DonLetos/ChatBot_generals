import SQL_mode

def it_ok(message):
    text = f'Здравствуйте, {message.from_user.full_name}!'
    return {'text_message': text, 'list_name_button': []}

def user_not_found(message):
    text = (f'{message.from_user.full_name}'
            ', ваш пользователь не зарегестрирован в базе.')
    name_button = [('Зарегистрироваться','Зарегистрироваться')]
    return {'text_message': text, 'list_name_button': name_button}

def registration(message):
    id_user = message.chat.id
    cod = SQL_mode.ControlUser(id_user)
    if cod == 404:
        text_result_request = SQL_mode.CreatUser(message)
        return {'text_message': text_result_request,'list_name_button': []}
    elif cod == 200:
        text = 'Ваш пользователь уже зарегистрирован.'
        return {'text_message': text, 'list_name_button': []}

def Start_new_game(message, id_users: int):
    pass

def Sent_invite(message):
    text = f' Пользователь {message.chat.username} приглашает вас на игру'
    name_button = [('Принять', 'Accept_invitation'),
                 ('Отклонить', 'Decline_the_invitation')
                ]
    return {'text_message': text, 'list_name_button': name_button}

def Accept_invitation(message):
    pass

def Decline_the_invitation(messege):
    pass

dict_cod_result = {200: it_ok,
                   404: user_not_found,
                   'Зарегистрироваться': registration,
                   '12_01': Sent_invite,
                   'Accept_invitation': Accept_invitation,
                   'Decline_the_invitation':Decline_the_invitation
            }

class cod_control:
    text = ''