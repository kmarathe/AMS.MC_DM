import csv
import datetime as date
import matplotlib.pyplot as plt


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
        # This for loop will iterate over all the cities present in the dictionary
        for city, years_dict in search_dict.iteritems():
            # create an empty x-value and y-value list for the city
            x_values = []
            y_values = []

            # this loop will iterate over all search years present in the dictionary
            for search_year, search_values in years_dict.iteritems():
                # add the object for month of that year and its corresponding search value
                for i in range(1, 13, 1):
                    x_values.append(date.datetime(year=search_year, month=i, day=1))
                    y_values.append(search_values[i - 1])

            plt.plot(x_values, y_values, marker='o', label=city)

        plt.title('Exercise 3')
        plt.xlabel('Month')
        plt.ylabel('No. of Searches')
        plt.legend(loc='best', title='Searches')
        plt.show()


def main():
    searches_file_name = 'searches.csv'
    list_cities = ['AGP', 'MAD', 'BCN', 'JFK']
    destination_column = 'Destination'
    date_column = 'Date'
    search_file = SearchesFile(searches_file_name)
    search_file.generate_graph(list_cities, destination_column, date_column)

    #search_dict = {'BCN': {2013: [29469, 28329, 30552, 31236, 28728, 26505, 29241, 27075, 23427, 20276, 19824, 15400],
    #                       2014: [29469, 28329, 30552, 31236, 28728, 26505, 29241, 27075, 23427, 20276, 19824, 15400]},
    #               'MAD': {2014: [24258, 22800, 24681, 25251, 26334, 22800, 22971, 21831, 21147, 22294, 20272, 14504],
    #                       2013: [258, 220, 241, 251, 263, 220, 271, 231, 217, 224, 272, 104]},
    #               'AGP': {2011: [9633, 8379, 10659, 8265, 10830, 7923, 8892, 7866, 8151, 6499, 6384, 3696]}}
    #search_file.plot_graph(search_dict)
if __name__ == "__main__":
    main()
