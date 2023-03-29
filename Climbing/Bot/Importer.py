from Climbing.Bot.Database import Database

from csv import reader
import datetime
from os.path import isfile


class Importer:
    """
        Handles importing csv files
    """

    # The instance of the database connection
    _database = None

    def __init__(self, file_: str, database: Database) -> None:
        """
            Sets up all properties

            :param file_: str
                The path to the csv file
            :param database: Database
                The connection to the database
            :return None
        """
        self._file = file_
        self._database = database

    def run(self) -> bool:
        """
            Runs the importing process

            :return bool
                Returns true if the import was successful, false otherwise
        """
        if not isfile(self._file):
            raise ValueError('The given filepath is not a valid file.')

        # Open the csv file and insert each row into the database
        i = 0
        with open(self._file, mode='r') as file_:
            csv = list(reader(file_, delimiter='|'))
            csv.pop(0)
            for row in csv:
                # Convert the date into a datetime object
                user_name, grade, date_ = row
                date_ = datetime.datetime.strptime(date_, '%Y-%m-%d').date()

                self._database.add_route(user_name, grade, date_)
                i += 1

        print(f'Imported {i} rows successfully.')
        return True
