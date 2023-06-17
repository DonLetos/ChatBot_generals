
token = '5534910733:AAF-EudeFKewovmT18qoRYQDPtCjg5AuAc0'

class SQL():
    @staticmethod
    def parameter_connect():
        # Параметры подключения
        SQL_parameter_connect = {}
        SQL_parameter_connect['host'] = 'localhost'
        SQL_parameter_connect['port'] = '5432'
        SQL_parameter_connect['database'] = 'Generals'
        SQL_parameter_connect['user'] = 'postgres'
        SQL_parameter_connect['password'] = '760652el'
        x  =1
        return SQL_parameter_connect
