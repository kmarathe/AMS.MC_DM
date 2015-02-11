import csv

# An object of class BookingsFile represents a file which stores the booking entries


class BookingsFile(object):
    def __init__(self, filename):
        self.FileName = filename

    # This function will find the number of arriving passengers at each airport in the year of 2013 and
    # will print top n airports with the passenger count
    def get_top_arrival_airports(self, airport_column, passenger_column, year_column, year_value, n):
        try:
            with open(self.FileName, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='^')
                first_row = next(csv_reader)
                number_of_fields = len(first_row)

                # get the index of airport column, passenger column and year column from the first row
                airport_index = self.get_column_index(first_row, airport_column)
                passenger_index = self.get_column_index(first_row, passenger_column)
                year_index = self.get_column_index(first_row, year_column)

                # check if all the columns are present in the file
                if airport_index == -1 or passenger_index == -1 or year_index == -1:
                    return

                airport_dict = self.get_arrival_count(csv_reader, airport_index, passenger_index,
                                                      year_index, number_of_fields, year_value)
                self.print_top_n_airports(airport_dict, n)
        except IOError:
            print("File not found - " + self.FileName)

    # This function will return the index of column_name from the first_row. If column does not exist in the first row
    # it will return -1
    @staticmethod
    def get_column_index(first_row, column_name):
        # Trim the column headers
        for i in range(0, len(first_row)):
            first_row[i] = first_row[i].strip()

        if column_name not in first_row:
            print 'Column ' + column_name + ' does not exist in the file'
            return -1

        return first_row.index(column_name)

    # This function will print the top n airports by passenger value in the airport_dict
    @staticmethod
    def print_top_n_airports(airport_dict, n):
        # sort the dictionary by value in a list
        sorted_airport_list = sorted(airport_dict.items(), key=lambda x: x[1], reverse=True)
        list_length = len(sorted_airport_list)
        i = 1
        # check if number of airports to be displayed are more than total number of airports
        if list_length < n:
            print 'Only ' + str(list_length) + ' airports are present in the file'
            n = list_length

        print 'Top ' + str(n) + ' arrival airports are:'
        for port in sorted_airport_list:
            print str(i) + '. ' + port[0] + ' ' + str(port[1])
            if i == n:
                break
            i += 1

    # This function will return the number of passengers arriving at each airport in the year of 'year_value'
    # as a dictionary with key = airport, value = number of passengers
    @staticmethod
    def get_arrival_count(csv_reader, airport_index, passenger_index,
                          year_index, number_of_fields, year_value):
        airport_dict = {}
        for row in csv_reader:
            # check if all the columns are present in booking entry and year of booking is 'year_value'
            if len(row) == number_of_fields and row[year_index] == year_value:
                airport = row[airport_index].strip()
                passengers = int(row[passenger_index].strip())
                if airport in airport_dict:
                    airport_dict[airport] += passengers
                else:
                    airport_dict[airport] = passengers

        return airport_dict


def main():
    bookings_file_name = 'bookings.csv'
    airport_column = 'off_port'
    passenger_column = 'pax'
    year_column = 'year'
    year_value = '2013'
    number_of_airports = 10

    bookings_file = BookingsFile(bookings_file_name)
    bookings_file.get_top_arrival_airports(airport_column, passenger_column,
                                           year_column, year_value, number_of_airports)


if __name__ == "__main__":
    main()
