import psycopg2
import config

SQL_parametr_connect = config.SQL.parameter_connect()

# Подключение к базе данных
conn = psycopg2.connect(
    host = SQL_parametr_connect['host'],
    port = SQL_parametr_connect['port'],
    database = SQL_parametr_connect['database'],
    user = SQL_parametr_connect['user'],
    password = SQL_parametr_connect['password']
)

def ControlUser(id_user):
    # Создание курсора
    with conn.cursor() as curs:
        text_sql_request = 'select * from users where users.id_users = %s'
        # Выполнение запроса SELECT
        curs.execute(text_sql_request, (id_user,))
        # Получение одну строку результатов
        results = curs.fetchone()
        if results == None:
            cod = 404
        else:
            cod = 200
    return cod