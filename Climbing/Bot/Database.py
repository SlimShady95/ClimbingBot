from datetime import date
from os.path import exists
import sqlite3


class Database:
    _connection = None
    _database_file = ''

    def __init__(self, database_file: str) -> None:
        """
            Initializes the database connection and sets up the database if needed

            :param database_file: str
                The path to the database file
            :return None
        """
        self._database_file = database_file
        if not self._create_database():
            self._connection = sqlite3.connect(database_file, check_same_thread=False)

    def __del__(self) -> None:
        """
            If the database object gets deleted, close the connection to it.

            :return None
        """
        self._connection.close()

    def _create_database(self) -> bool:
        """
            Creates the databse if it does not exist yet

            :return bool
                Returns true if the database was created, false otherwise
        """
        if exists(self._database_file):
            return False

        # Create file first
        file_ = open(self._database_file, 'w+')
        file_.close()

        # Create tables
        self._connection = sqlite3.connect(self._database_file, check_same_thread=False)
        cursor = self._connection.cursor()
        cursor.execute('''
            CREATE TABLE `routes` (
                `id` INTEGER PRIMARY KEY,
                `username` TEXT NOT NULL,
                `grade` TEXT NOT NULL,
                `date` date
            );
        ''')
        cursor.close()
        print('Creates table: routes')

        return True

    def add_route(self, username: str, grade: str, date_: date = None) -> None:
        """
            Adds a route to the database

            :param username: str
                The name of the user who did the route
            :param grade: str
                The grade of the route the user did
            :param date_: date
                The date when the route was achieved. If not given, this will be the current date.
            :return None
        """
        route_date = date_ if date_ is not None else date.today()
        cursor = self._connection.cursor()
        cursor.execute('INSERT INTO `routes` (`username`, `grade`, `date`) VALUES (?, ?, ?)', (username, grade, route_date))
        cursor.close()
        self._connection.commit()

    def get_routes(self, username: str = None, date_: date = None) -> list:
        """
            Returns a list of achieved routes

            :param username: str
                If given, only routes done by this user will be fetched
            :param date_: date
                If given, only routes done at this date will be fetched
            :return list
                Returns a list with all achieved routes that fit the requirements
        """
        cursor = self._connection.cursor()
        where = []
        data = []
        if username is not None:
            where.append('`username` = ?')
            data.append(username)

        if date_ is not None:
            where.append('`date` = ?')
            data.append(date_)

        where_clause = ''
        if where:
            where_clause = 'WHERE ' + ' AND '.join(where)

        cursor.execute('SELECT * FROM `routes`' + where_clause, data)
        rows = cursor.fetchall()
        cursor.close()

        return rows
