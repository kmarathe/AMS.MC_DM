import csv
import datetime as date


class SearchesFile(object):
    def __init__(self, filename):
        self.FileName = filename

    # This function will accept a list of cities and will generate a graph displaying number of searches made
    # for a city as destination versus month
    def generate_graph(self, list_cities, destination_column, date_column):
        try:
            with open(self.FileName, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='^')
                first_row = next(csv_reader)
                number_of_fields = len(first_row)
                destination_index = self.get_column_index(first_row, destination_column)
                date_index = self.get_column_index(first_row, date_column)

                if destination_index == -1 or date_index == -1:
                    return

                search_dict = self.get_search_history(csv_reader, list_cities, destination_index,
                                                      date_index, number_of_fields)
                print search_dict
                self.plot_graph(search_dict)

        except IOError:
            print("File not found - " + self.FileName)

    # This method will return a dictionary of dictionaries where key = city, value = second dictionary
    # for second dictionary key = year, value = list of 12 elements representing number of searches made
    # in that month

    def get_search_history(self, csv_reader, list_cities, destination_index, date_index, number_of_fields):
        search_dict = {}
        for city in list_cities:
            search_dict[city] = {}

        for row in csv_reader:
            if len(row) == number_of_fields:
                destination = row[destination_index]
                if destination in list_cities:
                    current_date = date.datetime.strptime(row[date_index], '%Y-%m-%d').date()
                    search_dict[destination] = self.modify_dict(search_dict[destination], current_date)

        return search_dict

    # This method will take the year dictionary of a city and the current search date and it will modify
    # the year dictionary accordingly
    @staticmethod
    def modify_dict(year_dict, current_date):
        current_month = current_date.month
        current_year = current_date.year

        if current_year not in year_dict:
            year_dict[current_year] = [0] * 12

        year_dict[current_year][current_month - 1] += 1
        return year_dict

    # This function will return the index of column_name from the first_row. If column does not exist in the first row
    # it will return -1
    @staticmethod
    def get_column_index(first_row, column_name):
        if column_name not in first_row:
            print 'Column ' + column_name + ' does not exist in the file'
            return -1

        return first_row.index(column_name)

    # This function will plot the graph of searches against the month
    @staticmethod
    def plot_graph(search_dict):
        return
        #
        # TO DO
        #


def main():
    searches_file_name = 'searches.csv'
    list_cities = ['AGP', 'MAD', 'BCN']
    destination_column = 'Destination'
    date_column = 'Date'
    search_file = SearchesFile(searches_file_name)
    search_file.generate_graph(list_cities, destination_column, date_column)

if __name__ == "__main__":
    main()
