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
    if data.username is None:
        last_name = ' ' if data.last_name is None else data.last_name
        first_name = ' ' if  data.first_name is None else data.first_name
        user_name = last_name +' '+ first_name
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
    text_sql_request = 'select users.login, users.id_users  from users ' #where users.id_users != %s'
    results = execute_request(text_sql_request, (id_user,), fetchone = False)
    return results


def TurnGame(id_game):
    text_sql_request = 'select * from game where game.id_game = %s'
    result = execute_request(text_sql_request, (id_game, ))
    return result


def TernGame_SaveTurn(id_game: int, it_turn_first_player: bool, score: int):
    if it_turn_first_player:
        sql_text = 'first_players_score'
    else:
        sql_text = 'second_players_score'
    text_sql_request = f'update game set {sql_text} = %s where id_game = %s'
    try:
        execute_request_edit(text_sql_request, (score, str(id_game)))
        results = f'Ваш результат:: {score}'
        name_button = [
            ('TAKE MORE', f'33_001_{id_game}'),
            ('PASS', f'33_003_{id_game}')
        ]
    except psycopg2.Error as error:
        results = f'Ошибка при работе с SQL {error}'
        name_button = []
    return {'text': results, 'namebutton': name_button}


def EndGame(id_game, score):
    text_sql_request = 'delete from game where game.id_game = %s'
    try:
        execute_request_edit(text_sql_request, (id_game,))
        results = f'Вы проиграли! У вас перебор. {score}'
    except psycopg2.Error as error:
        results = f'Ошибка при работе с SQL {error}'
    return results


def NextTurn(id_game):
    text_sql_request = (f'select game.turn_first_player,  ' 
                       f'game.id_first_player,' 
                       f'game.id_second_player,' 
                       f'game.first_players_score,'
                       f'game.second_players_score'  
                       f' from game where id_game = %s')
    value = (str(id_game),)
    request_rez = execute_request(text_sql_request, value)

    f_score = request_rez[3]
    s_score = request_rez[4]
    text_win = 'Вы победили'
    text_lose = 'Вы проиграли. у вас меньше'
    if f_score != 0 and s_score != 0:
        WIN_FIRST_PLAYER = f_score > s_score
        if WIN_FIRST_PLAYER:
            win_id_chat = request_rez[1]
            lose_id_chat = request_rez[2]
        else:
            win_id_chat = request_rez[2]
            lose_id_chat = request_rez[1]
        win_rez = f_score - s_score
        if win_rez == 0:
            text_win = text_lose = 'НИЧЬЯ!'
        list_result = [
                        {'text_message': text_win, 'chat_id': win_id_chat, 'list_name_button': []},
                        {'text_message': text_lose, 'chat_id': lose_id_chat, 'list_name_button': []}
                      ]
        return list_result
    else:
        chak_bool = not request_rez[0]
        if chak_bool:
            id_chat = request_rez[1]
        else:
            id_chat = request_rez[2]
        text_sql_request = (
                        f'update game set turn_first_player = %s'
                        f' where id_game = %s'
                        )
        value = (str(chak_bool), str(id_game))
        try:
            execute_request_edit(text_sql_request, value)
            result = {'text':'Ваш ход!', 'chat_id': id_chat, 'error': False}
        except psycopg2.Error as error:
            text = f'Ошибка при работе с SQL {error}'
            result = {'text': text, 'chat_id': id_chat, 'error': True}
    return result