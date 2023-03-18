class Grade:
    """
        Class for handling grades
    """

    @staticmethod
    def get_grades() -> dict:
        """
            Returns all grades this bot currently supports

            :return dict
                Returns a dict containing all grades as key and the points for topping a route as value
        """
        return {
            'V1':  1,   'V2':  2,   'V3':  3,
            'V4':  4,   'V5':  5,   'V6':  6,
            'V7':  7,   'V8':  8,   'V9':  9,
            'V10': 10, 'V11':  11,  'V12': 12,
            '2':   2,    '3':  3,   '4-':  3.5,
            '4':   4,    '4+': 4.5, '5-':  4.5,
            '5':   5,    '5+': 5.5, '6-':  5.5,
            '6':   6,    '6+': 6.5, '7-':  6.5,
            '7':   7,    '7+': 7.5, '8-':  7.5,
            '8':   8,    '8+': 8.5, '9-':  8.5,
            '9':   9,    '9+': 9.5, '10-': 9.5,
        }
