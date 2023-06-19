import psycopg2
import config
from dataclasses import dataclass

SQL_parameter_connect = config.SQL.parameter_connect()

# Подключение к базе данных
CONN = psycopg2.connect(**SQL_parameter_connect)

def execute_request(text_request: str, requirement: tuple = tuple(), fetchone = True):
    # Создание курсора
    with CONN.cursor() as curs:
        curs.execute(text_request, requirement)
        if fetchone:
            results = curs.fetchone()
        else:
            results = curs.fetchall()
        return results


def execute_request_edit(text_request: str, requirement: tuple = tuple()):
    # Создание курсора
    with CONN.cursor() as curs:
        curs.execute(text_request, requirement)
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
        execute_request_edit(text_sql_request, VALUES)
        results = 'Ваш пользователь успешно создан!'
    except psycopg2.Error as error:
        results = f'Ошибка при работе с SQL {error}'
    return results


def CreatGame(message: tuple):
    message, master_id_chat = message
    test_sql_request = (
                        f'INSERT INTO game'
                        f'(id_first_player, '
                        f'id_second_player, '
                        f'first_players_score, '
                        f'second_players_score, '
                        f'number_of_wins_second_players, '
                        f'number_of_wins_first_players, '
                        f'turn_first_player, '
                        f'id_game)'
                        f' VALUES(%s, %s, %s, %s, %s, %s, %s, %s)'
                        )
    id_game = str(master_id_chat) + str(message.chat.id)
    VALUE = (master_id_chat, message.chat.id, 0, 0, 0, 0, True, id_game)
    try:
        execute_request_edit(test_sql_request, VALUE)
        return id_game
    except psycopg2.Error as error:
        results = f'Ошибка при работе с SQL {error}'
    return results


def New_game(id_user: int):
    text_sql_request = 'select users.login, users.id_users  from users where users.id_users != %s'
    results = execute_request(text_sql_request, (id_user,), fetchone = False)
    return results


def TurnGame(id_game):
    text_sql_request = 'select * from game where game.id_game = %s'
    result = execute_request(text_sql_request, (id_game, ))
    return result

def EndGame(id_game):
    text_sql_request = 'delete from game where game.id_game = %s'
    try:
        execute_request_edit(text_sql_request, (id_game,))
        results = 'Вы проиграли'
    except psycopg2.Error as error:
        results = f'Ошибка при работе с SQL {error}'
    return results


def NextTurn(id_game):
    pass