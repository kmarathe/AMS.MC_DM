import csv

# An object of class BookingsFile represents a file which stores the booking entries


class BookingsFile(object):
    # Constructor
    def __init__(self, filename):
        self.FileName = filename

    # get_top_arrival_airports: This function will find the number of arriving passengers at each airport in the year
    # of 'year_value' and will print top 'n' airports with the passenger count
    def get_top_arrival_airports(self, airport_column, passenger_column, year_column, year_value, n):
        # if number of airports to be displayed is less than zero then return
        if n <= 0:
            print 'Number of airports to be displayed should be greater than 0'
            return

        try:
            with open(self.FileName, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='^')
                first_row = next(csv_reader)

                # get the total number of fields index of airport column index, passenger column index
                # and year column index from the first row
                number_of_fields = len(first_row)
                airport_index = self.get_column_index(first_row, airport_column)
                passenger_index = self.get_column_index(first_row, passenger_column)
                year_index = self.get_column_index(first_row, year_column)

                # check if all the columns are present in the file
                if airport_index == -1 or passenger_index == -1 or year_index == -1:
                    return

                # create an dictionary object with key = airport_name, value = number of arriving passengers
                airport_dict = self.get_arrival_count(csv_reader, airport_index, passenger_index,
                                                      year_index, number_of_fields, year_value)

                # print top 'n' airports from the airport_dict
                self.print_top_n_airports(airport_dict, n)
        except IOError:
            print("File not found - " + self.FileName)

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

    # print_top_n_airports: This function will print the top 'n' airports from airport_dict
    # by descending passenger count
    @staticmethod
    def print_top_n_airports(airport_dict, n):
        # sort the dictionary by value in a list
        sorted_airport_list = sorted(airport_dict.items(), key=lambda x: x[1], reverse=True)
        list_length = len(sorted_airport_list)
        i = 1
        # if number of airports to be displayed are more than total number of airports present in dictionary
        # then set n to size of dictionary
        if list_length < n:
            print 'Only ' + str(list_length) + ' airports are present in the file'
            n = list_length

        print 'Top ' + str(n) + ' arrival airports are (by passenger count):'
        for port in sorted_airport_list:
            # print the airport name with passenger count
            print str(i) + '. ' + port[0] + ' ' + str(port[1])
            if i == n:
                break
            i += 1

    # get_arrival_count: This function will return an dictionary with key = airport_name,
    # value = number of passengers arriving at that airport in 'year_value'
    @staticmethod
    def get_arrival_count(csv_reader, airport_index, passenger_index,
                          year_index, number_of_fields, year_value):
        # initialize an empty dictionary
        airport_dict = {}
        for row in csv_reader:
            # check if all the columns are present in booking entry and year of booking is 'year_value'
            if len(row) == number_of_fields and row[year_index] == year_value:
                # get the airport name and passenger count
                airport = row[airport_index].strip()
                passengers = int(row[passenger_index].strip())
                if airport in airport_dict:
                    airport_dict[airport] += passengers
                else:
                    airport_dict[airport] = passengers

        return airport_dict


def main():
    # name of the file containing booking entries
    bookings_file_name = 'bookings.csv'
    # airport, passenger and year column headers
    airport_column = 'off_port'
    passenger_column = 'pax'
    year_column = 'year'

    # year value of interest
    year_value = '2013'
    # number of airports to be displayed
    number_of_airports = 10

    # create an object for the booking file
    bookings_file = BookingsFile(bookings_file_name)
    # call the function to display
    bookings_file.get_top_arrival_airports(airport_column, passenger_column,
                                           year_column, year_value, number_of_airports)


if __name__ == "__main__":
    main()
