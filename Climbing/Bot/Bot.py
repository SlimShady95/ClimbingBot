from Climbing.Bot.Database import Database
from Climbing.Util.Grade import Grade
from Climbing.Util.Helper import chunks, create_pretty_table
from Climbing.Util.Telegram import Telegram

from collections import OrderedDict
import datetime
from datetime import date
import matplotlib
from matplotlib import pyplot
from string import digits
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters


class Bot:
    """
        Class for handling all bot related things
    """

    # The instance of the telegram API
    _telegram = None

    # The instance of the database
    _database = None

    def __init__(self, telegram: Telegram, database: Database) -> None:
        """
            Initializes the bot

            :param telegram: Telegram
                The instance of the telegram API
            :param database: Database
                The instance of the sqlite database
        """
        self._telegram = telegram
        self._telegram.add_command(CommandHandler('start', self._start))
        self._telegram.add_command(CommandHandler('end', self._end))
        self._telegram.add_command(CommandHandler('help', self._help))
        self._telegram.add_command(CommandHandler('chart', self._chart, pass_args=True))
        self._telegram.add_command(CommandHandler('ranking', self._ranking, pass_args=True))
        self._telegram.add_command(CommandHandler('session', self._session, pass_args=True))
        self._telegram.add_command(CommandHandler('stats', self._stats, pass_args=True))
        self._telegram.add_command(MessageHandler(Filters.text, self._message))
        self._database = database

    def _start(self, update: Update, context: CallbackContext) -> None:
        """
            Starts a session

            :param update: Update
                The context of the current message
            :param context: CallbackContext
                The callback context
            :return None
        """
        markup = ReplyKeyboardMarkup(chunks(list(Grade.get_grades().keys()), 4))
        update.message.reply_text('To add a route you have done, simply click its difficulty:', reply_markup=markup)

    def _end(self, update: Update, context: CallbackContext) -> None:
        """
            Ends a session

            :param update: Update
                The context of the current message
            :param context: CallbackContext
                The callback context
            :return None
        """
        update.message.reply_text(reply_markup=ReplyKeyboardRemove())

    def _chart(self, update: Update, context: CallbackContext) -> None:
        """
            Generates a chart and sends it to the user

            :param update: Update
                The context of the current message
            :param context: CallbackContext
                The callback context
            :return None
        """
        username = context.args[0] if context.args else update.message.from_user.first_name
        routes = self._database.get_routes(username=username)
        routes_grouped_by_date = OrderedDict()
        for route in routes:
            date_ = route[3]
            if date_ not in routes_grouped_by_date.keys():
                routes_grouped_by_date[date_] = []

            routes_grouped_by_date[date_].append(route)

        # Calculate the average grade for each date for both bouldering and climbing
        averages_bouldering = OrderedDict()
        averages_climbing = OrderedDict()
        grades = Grade.get_grades()
        for date_, routes in routes_grouped_by_date.items():
            bouldering_grades = [grades[route[2]] for route in routes if route[2].startswith('V')]
            climbing_grades = [grades[route[2]] for route in routes if not route[2].startswith('V')]

            averages_bouldering[date_] = sum(bouldering_grades) / len(bouldering_grades) if bouldering_grades else 0
            averages_climbing[date_] = sum(climbing_grades) / len(climbing_grades) if climbing_grades else 0

        del routes_grouped_by_date

        # Sort the data by ascending date
        bouldering_chart_data = OrderedDict(sorted(averages_bouldering.items(), key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d')))
        climbing_chart_data = OrderedDict(sorted(averages_climbing.items(), key=lambda x: datetime.datetime.strptime(x[0], '%Y-%m-%d')))
        del averages_bouldering
        del averages_climbing

        # Draw the chart and save it to charts/USERNAME.png
        # TODO remove hardcoded path
        matplotlib.use('agg')
        pyplot.title('Average grade for bouldering/climbing in each session.')
        pyplot.xlabel('Date')
        pyplot.ylabel('Grade')
        pyplot.plot(bouldering_chart_data.keys(), bouldering_chart_data.values(), label='Bouldering')
        pyplot.plot(climbing_chart_data.keys(), climbing_chart_data.values(), label='Climbing')
        pyplot.legend()
        file_path = f'charts/{username}.png'
        pyplot.savefig(file_path)
        pyplot.clf()

        # Send the image back to the user
        with open(file_path, 'rb') as file_:
            update.message.reply_photo(file_)

    def _ranking(self, update: Update, context: CallbackContext) -> None:
        """
            Displays a ranking of all users

            :param update: Update
                The context of the current message
            :param context: CallbackContext
                The callback context
            :return None
        """
        ranking = OrderedDict()
        grades = Grade.get_grades()
        routes = self._database.get_routes()
        for route in routes:
            username = route[1]
            if username not in ranking.keys():
                ranking[username] = 0

            ranking[username] += grades[route[2]]

        ranking = OrderedDict(sorted(ranking.items(), key=lambda x: x[1], reverse=True))
        table = create_pretty_table(['Username', 'Points'], list(ranking.items()))
        update.message.reply_text(f'`{table}`', parse_mode='MARKDOWN')

    def _stats(self, update: Update, context: CallbackContext) -> None:
        """
            Lists all stats of the given user

            :param update: Update
                The context of the current message
            :param context: CallbackContext
                The callback context
            :return None
        """
        # If username is 'all', we return the stats for all users combined.
        username = context.args[0] if context.args else update.message.from_user.first_name
        if username.lower() == 'all':
            username = None

        self._show_stats(update, username)

    def _session(self, update: Update, context: CallbackContext) -> None:
        """
            Lists all stats of the given user for the current session

            :param update: Update
                The context of the current message
            :param context: CallbackContext
                The callback context
            :return None
        """
        self._show_stats(update, context.args[0] if context.args else update.message.from_user.first_name, date.today())

    def _show_stats(self, update: Update, username: str, date_: date = None) -> None:
        """
            Shows the stats according to the given parameters

            :param update: Update
                The context of the current message
            :param username: str
                The user to show the stats of
            :param date_: date
                The date to show the stats of
            :return:
        """
        routes = self._database.get_routes(username, date_)

        # Count how many routes of each difficulty the user has done
        grades = {}
        for route in routes:
            grade = route[2]
            if grade not in grades.keys():
                grades[grade] = 0

            grades[grade] += 1

        # Order the routes based on difficulty ascending and split them into two, one for bouldering and one for climbing
        grades = OrderedDict(sorted(grades.items(), key=lambda x: int(''.join([num for num in x[0] if num in digits]))))
        grades_boulder = {grade: num for grade, num in grades.items() if grade.startswith('V')}
        grades_climbing = {grade: num for grade, num in grades.items() if not grade.startswith('V')}

        # Create the tables to display them nicely
        table_boulder = create_pretty_table(['Grade', 'Completed'], list(grades_boulder.items()))
        table_climbing = create_pretty_table(['Grade', 'Completed'], list(grades_climbing.items()))

        # Build the message
        message = ''
        if grades_boulder:
            message += f'`{table_boulder.get_string(title="Boulder")}`\n\n\n'

        if grades_climbing:
            message += f'`{table_climbing.get_string(title="Climbing Routes")}`'

        # If there were no topped routes, state so
        if not message:
            message = f'{username} has not topped anything today!'

        update.message.reply_text(message, parse_mode='MARKDOWN')

    def _message(self, update: Update, context: CallbackContext) -> None:
        """
            Handles a sent grade

            :param update: Update
                The context of the current message
            :param context: CallbackContext
                The callback context
            :return None
        """
        username = update.message.from_user.first_name
        grade = update.message.text
        if grade not in Grade.get_grades().keys():
            self._telegram.send_message(f'The grade you entered is not valid: {grade}\.')
            return

        self._database.add_route(username, grade)

    def _help(self, update: Update, context: CallbackContext) -> None:
        """
            Displays the help for all existing commands

            :param update: Update
                The context of the current message
            :param context: CallbackContext
                The callback context
            :return None
        """
        help_texts = {
            '/start':              'Starts a session and displays the grade keyboard.',
            '/end':                'Ends a session and removes the grade keyboard again.',
            '/ranking':            'Displays a ranking for all users of this bot.',
            '/chart':              'Displays a chart with data of the topped routes.',
            '/chart [username]':   'Displays a chart with data of the topped routes for the given user.',
            '/session':            'Displays your statistics of the current session.',
            '/session [username]': 'Displays the statistics of the given user of the current session.',
            '/stats':              'Displays your all time statistics',
            '/stats [username]':   'Displays the all time statistics of the given user.',
            '/help':               'Displays this help section.',
        }

        message = ''
        for command, help_ in help_texts.items():
            message += f'{command}\n`{help_}`\n\n'

        update.message.reply_text(f'`{message}`', parse_mode='MARKDOWN')
