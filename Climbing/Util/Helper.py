from prettytable import PrettyTable


def chunks(list_: list, number: int):
    """
        Yield successive n-sized chunks from lst.

        :param list_: list
            The list to split
        :param number: int
            The size of a single chunk
    """
    for i in range(0, len(list_), number):
        yield list_[i:i + number]


def create_pretty_table(headings: list, data: list) -> PrettyTable:
    """
        Creates a pretty table using the given headings and data

        :param headings: list
            A list containing all headings for this table
        :param data: list
            A list containing all rows of data for this table
        :return PrettyTable
            Returns the instance of the created table
    """
    table = PrettyTable(headings)
    table.add_rows(data)

    return table
