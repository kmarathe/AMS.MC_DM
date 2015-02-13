import csv
import datetime as date
import matplotlib.pyplot as plt

# An object of class SearchFile represents a file which stores the search entries


class SearchFile(object):
    # constructor
    def __init__(self, filename):
        self.FileName = filename

    # generate_graph: This function will accept a list of cities and will generate a graph displaying
    # monthly number of searches made for the city as destination
    def generate_graph(self, list_cities, destination_column, date_column):
        # if list of cities is empty, return
        if not list_cities:
            print 'list of cities can not be empty'
            return

        try:
            with open(self.FileName, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='^')
                first_row = next(csv_reader)

                # Get the total number of fields, destination index, date index from first row
                number_of_fields = len(first_row)
                destination_index = self.get_column_index(first_row, destination_column)
                date_index = self.get_column_index(first_row, date_column)

                # If desired columns are not present then return
                if destination_index == -1 or date_index == -1:
                    return

                # create an dictionary with cities as key and empty dictionary as value from list of cities
                search_dict = self.create_cities_dict(list_cities)

                # if search_dict is empty then return
                if not search_dict:
                    print 'please enter non empty city names'
                    return

                # populate the search dictionary
                self.get_search_history(csv_reader, search_dict, destination_index, date_index, number_of_fields)

                # plot the graph from search_dict
                self.plot_graph(search_dict)

        except IOError:
            print("File not found - " + self.FileName)

    # create_cities_dict: This function will create a dictionary from list_cities with key = city_name,
    # value = empty dictionary
    @staticmethod
    def create_cities_dict(list_cities):
        search_dict = {}
        # Add the cities to the dictionary with value as empty dictionary
        for city in list_cities:
            # add only non-empty city names in the dictionary
            if city and len(city.strip()) > 0:
                search_dict[city] = {}

        return search_dict

    # get_search_history: This method will return a dictionary of dictionaries such that
    # for search_dictionary - key = city name, value = year_dictionary
    # for year_dictionary - key = year, value = list of 12 elements representing number of searches made per month in
    # that year
    def get_search_history(self, csv_reader, search_dict, destination_index, date_index, number_of_fields):
        # parse the file row by row
        for row in csv_reader:
            # current row will be taken into consideration only if it has all the fields
            if len(row) == number_of_fields:
                destination = row[destination_index].strip()
                # Check if the destination is in the list of desired cities
                if destination in search_dict:
                    # create a datetime object of the current date, which will be used to get the year and month
                    current_date = date.datetime.strptime(row[date_index].strip(), '%Y-%m-%d').date()
                    search_dict[destination] = self.modify_year_dict(search_dict[destination], current_date)

        return search_dict

    # modify_year_dict: This method will take the year dictionary of a city and the current search date and it
    # will modify the year dictionary accordingly
    @staticmethod
    def modify_year_dict(year_dict, current_date):
        current_month = current_date.month
        current_year = current_date.year

        # if the current year is present in dictionary add an entry for current year with a list of 12 numbers
        # initialized to 0 representing number of search for each month
        if current_year not in year_dict:
            year_dict[current_year] = [0] * 12

        # Increase the count for the current month
        year_dict[current_year][current_month - 1] += 1
        return year_dict

    # get_column_index: This function will return the index of column_name from the first_row.
    # If column does not exist in the first_row it will return -1
    @staticmethod
    def get_column_index(first_row, column_name):
        # Trim the column headers
        for i in range(0, len(first_row)):
            first_row[i] = first_row[i].strip()

        # if column name is not present in first_row return -1
        if column_name not in first_row:
            print 'Column ' + column_name + ' does not exist in the file'
            return -1

        return first_row.index(column_name)

    # This function will plot the graph of number of searches made per month from search_dict
    @staticmethod
    def plot_graph(search_dict):
        # This for loop will iterate over all the cities present in the dictionary
        for city, years_dict in search_dict.iteritems():
            # create an empty x-value and y-value list for the city
            x_values = []
            y_values = []

            # this loop will iterate over all search years present in the dictionary
            for search_year, search_values in years_dict.iteritems():
                # add an entry for month and corresponding search value
                for i in range(1, 13, 1):
                    x_values.append(date.datetime(year=search_year, month=i, day=1))
                    y_values.append(search_values[i - 1])

            plt.plot(x_values, y_values, marker='o', label=city)

        # labels for graph
        plt.title('Exercise 3')
        plt.xlabel('Month')
        plt.ylabel('No. of Searches')
        plt.legend(loc='best', title='Searches')
        plt.show()


def main():
    # name of the file containing search entries
    searches_file_name = 'searches.csv'
    # cities of interest
    list_cities = ['MAD', 'BCN', 'AGP']
    # column headers of destination and date column
    destination_column = 'Destination'
    date_column = 'Date'

    # create an object of search file
    search_file = SearchFile(searches_file_name)
    # generate the graph from search file for the cities of interest
    search_file.generate_graph(list_cities, destination_column, date_column)

if __name__ == "__main__":
    main()
