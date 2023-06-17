
def it_ok():
    pass

def user_not_found(message):
    text = (f'{message.from_user.full_name}'
            ', ваш пользователь не зарегестрирован в базе.')

    return text

dict_cod = {200: it_ok,
            404: user_not_found
            }

class cod_control:
    text = ''