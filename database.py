import pymysql
from environs import Env

env = Env()
env.read_env()


class Database:
    def __init__(self, database, user, password, port, host):
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.host = host

    def db(self) -> pymysql.Connection:
        """Return connection to database"""
        return pymysql.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )

    def execute(self,
                sql: str,
                params: tuple = None,
                commit: bool = False,
                fetchall: bool = False,
                fetchone: bool = False) -> tuple:
        """
        Returns tuple, where could be data from database or None if something is committed
        """

        if not params:
            params = ()

        db = self.db()
        cursor = db.cursor()

        cursor.execute(sql, params)
        data = None

        if commit:
            db.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()

        db.close()
        return data

    def create_users_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Users (
                id INT PRIMARY KEY AUTO_INCREMENT,
                telegram_id INT NOT NULL UNIQUE,
                fullname VARCHAR(255)
            )
        """
        self.execute(sql, commit=True)

    def create_cities_table(self):
        sql = """
            CREATE TABLE IF NOT EXISTS Cities (
                id INT PRIMARY KEY AUTO_INCREMENT,
                user INT REFERENCES Users (id),
                name VARCHAR(255) NOT NULL,
                
                CONSTRAINT unique_city_name_for_user UNIQUE(user, name)
            )
        """
        self.execute(sql, commit=True)

    def register_user(self, telegram_id, fullname):
        sql = """
            INSERT INTO Users (telegram_id, fullname) VALUES (%s, %s)
        """
        self.execute(sql=sql, params=(telegram_id, fullname), commit=True)

    def register_city(self, user_id, city_name):
        """Registers city name and attaches it with a certain user"""
        sql = """
            INSERT INTO Cities (user, name)
            VALUES (%s, %s)
        """
        self.execute(sql, (user_id, city_name), commit=True)

    def get_user(self, telegram_id):
        """Returns a single user by telegram id"""
        sql = """
            SELECT * FROM Users
            WHERE telegram_id = %s
        """
        return self.execute(sql, (telegram_id,), fetchone=True)

    def get_users(self):
        """Returns all users list"""
        sql = """
            SELECT * FROM Users
        """
        return self.execute(sql, fetchall=True)

    def get_cities(self, user_id):
        sql = """
            SELECT * FROM Cities 
            WHERE user = %s
        """
        return self.execute(sql, (user_id,), fetchall=True)

    def clear_cities_list(self, user_id):
        sql = """
            DELETE FROM Cities 
            WHERE user = %s
        """
        self.execute(sql, (user_id,), commit=True)


db = Database(
    database=env.str('DB_NAME'),
    user=env.str('DB_USER'),
    password=env.str('DB_PASSWORD'),
    host=env.str('DB_HOST'),
    port=env.str('DB_PORT'),
)

db.create_users_table()
db.create_cities_table()
