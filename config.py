
token = '5534910733:AAF-EudeFKewovmT18qoRYQDPtCjg5AuAc0'


class SQL:
    @staticmethod
    def parameter_connect():
        # Параметры подключения
        SQL_parameter_connect = {
                                 'host': 'localhost',
                                 'port': '5432',
                                 'database': 'Generals',
                                 'user': 'postgres',
                                 'password': '760652el'
                                }

        return SQL_parameter_connect
