import psycopg2
import configparser
import sqlalchemy.pool as pool


class DatabaseConnect:
    """
    커넥션 풀
    """
    __instance      = None
    __DB_FILE_PATH  = None
    __POOL_SIZE     = None
    __queuePool     = None

    __HOST     = None
    __DATABASE = None
    __USER     = None
    __PASSWORD = None
    __PORT     = None

    def __init__(self):
        self.DB_FILE_PATH = '../sql/db.properties'

        parser = configparser.RawConfigParser()
        parser.read(self.DB_FILE_PATH)

        self.__HOST        = parser.get('database', 'host')
        self.__DATABASE    = parser.get('database', 'database')
        self.__USER        = parser.get('database', 'user')
        self.__PASSWORD    = parser.get('database', 'password')
        self.__PORT        = int(parser.get('database', 'port'))

    def __get_connection(self):
        return psycopg2.connect(
            host=self.__HOST,
            user=self.__USER,
            password=self.__PASSWORD,
            dbname=self.__DATABASE,
            port=self.__PORT
        )

    @staticmethod
    def get_connection():
        self = DatabaseConnect.__get_instance()

        if self.__queuePool is None:
            self.__queuePool = pool.QueuePool(self.__get_connection, max_overflow=10, pool_size=5)
        return self.__queuePool.connect()

    @staticmethod
    def __get_instance():
        if DatabaseConnect.__instance is None:
            DatabaseConnect.__instance = DatabaseConnect()
        return DatabaseConnect.__instance

