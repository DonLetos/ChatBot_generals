import psycopg2
import config
from dataclasses import dataclass

SQL_parametr_connect = config.SQL.parameter_connect()

# Подключение к базе данных
CONN = psycopg2.connect(
    host = SQL_parametr_connect['host'],
    port = SQL_parametr_connect['port'],
    database = SQL_parametr_connect['database'],
    user = SQL_parametr_connect['user'],
    password = SQL_parametr_connect['password']
)

def execute_request(text_request: str, requirement = '', fetchone = True):
    # Создание курсора
    with CONN.cursor() as curs:
        curs.execute(text_request, requirement)
        try:
            if fetchone:
                results = curs.fetchone()
            else:
                results = curs.fetchall()
            return results
        except:
            CONN.commit()

def ControlUser(id_user):
    text_sql_request = 'select * from users where users.id_users = %s'
    results = execute_request(text_sql_request, (id_user,))
    if results == None:
        cod = 404
    else:
        cod = 200
    return cod

def CreatUser(message):
    # Создание курсора
    data = message.chat
    text_sql_request = (f'INSERT INTO users'
                        f'(id_users, login, chat_id, firstname,lastname) '
                        f'VALUES( %s,  %s,  %s,  %s,  %s);')
    if data.username == None:
        user_name = data.last_name +' '+ data.first_name
    else:
        user_name = data.username
    VALUES = (data.id, user_name, data.id, data.first_name, data.last_name)
    try:
        execute_request(text_sql_request, VALUES)
        results = 'Ваш пользователь успешно создан!'
    except psycopg2.Error as error:
        results = f'Ошибка при работе с SQL {error}'
    return  results

def New_game(id_user: int):
    text_sql_request = 'select users.login, users.id_users  from users where users.id_users != %s'
    results = execute_request(text_sql_request, (id_user,), fetchone = False)
    return results

