from Climbing.Bot.Database import Database
from Climbing.Bot.Importer import Importer
from Config import database_path

from argparse import ArgumentParser
from os import remove

if __name__ == '__main__':
    # This program needs to be called with the file argument in order to run
    parser = ArgumentParser(description='Imports CSV files into the database.')
    parser.add_argument('file', help='The path to the file which should be imported.')
    parser.add_argument('-d', '--delete', action='store_true', help='If this flag is set, the csv file will get deleted after importing.')
    args = vars(parser.parse_args())

    # Create an instance of the Importer and run it
    importer = Importer(
        args['file'], Database(database_path)
    )
    result = importer.run()
    print('File successfully imported.' if result else 'There was a problem while importing the given file.')

    # Delete the file if the flag was set
    if args['delete']:
        remove(args['file'])
        print(f'Deleted {args["file"]}.')
