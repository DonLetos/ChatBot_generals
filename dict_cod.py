import SQL_mode

def it_ok(message):
    text = f'Здравствуйте, {message.from_user.full_name}!'
    return {'text_message': text, 'list_name_button': []}

def user_not_found(message):
    text = (f'{message.from_user.full_name}'
            ', ваш пользователь не зарегестрирован в базе.')
    name_button = ['Зарегистрироваться']
    return {'text_message': text, 'list_name_button': name_button}

def registration(message):
    id_user = message.chat.id
    cod = SQL_mode.ControlUser(id_user)
    if cod == 404:
        text_result_request = SQL_mode.CreatUser(message)
        return text_result_request
    elif cod == 200:
        return 'Ваш пользователь уже зарегистрирован.'

dict_cod_result = {200: it_ok,
            404: user_not_found,
            'Зарегистрироваться': registration
            }

class cod_control:
    text = ''