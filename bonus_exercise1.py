import csv
import os

# An object of class BookingDetails will represent a csv file storing the booking details. Filename is the name of
# the file and Booking_Dict will be a kind of inverted index to find the booking.as


class BookingDetails(object):
    def __init__(self, filename):
        self.FileName = filename
        self.Booking_Dict = {}

    # This function will create a dictionary of booking entries
    # for booking dictionary key will a date on which the booking has been made, value will be a origin dictionary
    # for origin dictionary key will the origin of the booking and value will be a list of destinations from that origin
    def get_booking_details(self, date_column, origin_column, destination_column):
        try:
            # Load the csv file
            with open(self.FileName, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='^')
                first_row = next(csv_reader)
                number_of_fields = len(first_row)

                # get the indices of destination column, date column and origin column
                destination_index = self.get_column_index(first_row, destination_column)
                date_index = self.get_column_index(first_row, date_column)
                origin_index = self.get_column_index(first_row, origin_column)

                # if columns are not present then return
                if destination_index == -1 or date_index == -1 or origin_index == -1:
                    return

                # create the booking dictionary
                self.Booking_Dict = self.create_booking_dict(csv_reader, number_of_fields, date_index,
                                                             origin_index, destination_index)
                # print self.Booking_Dict
        except IOError:
            print("File not found - " + self.FileName)

    # This function will create the Booking dictionary from the booking file
    def create_booking_dict(self, csv_reader, number_of_fields, date_index, origin_index, destination_index):
        booking_dict = {}
        # check if the row has all the fields present else skip the row
        for row in csv_reader:
            if len(row) == number_of_fields:
                # get the date, origin and destination of the booking
                date = row[date_index].split(" ")[0]
                origin = row[origin_index].strip()
                destination = row[destination_index].strip()
                # If the date is not present in booking dict then add it, with empty dictionary as its value
                if date not in booking_dict:
                    booking_dict[date] = {}

                # update the booking dictionary entry for current date
                booking_dict[date] = self.add_origin_destination(booking_dict[date], origin, destination)
        return booking_dict

    # This function will add origin and destination to origin dictionary
    @staticmethod
    def add_origin_destination(origin_dict, origin, destination):
        # if origin is not in origin_dict then add it with empty list as its value
        if origin not in origin_dict:
            origin_dict[origin] = []

        # if destination is not in destination list for the origin then add it
        if destination not in origin_dict[origin]:
            origin_dict[origin].append(destination)
        return origin_dict

    # This function will return the index of column_name from the first_row. If column does not exist in the first row
    # it will return -1
    @staticmethod
    def get_column_index(first_row, column_name):
        for i in range (0, len(first_row)):
            first_row[i] = first_row[i].strip()

        if column_name not in first_row:
            print 'Column ' + column_name + ' does not exist in the file'
            return -1

        return first_row.index(column_name)


# An object of class SearchDetails will represent a file which stores the search details.

class SearchDetails(object):
    def __init__(self, filename):
        self.FileName = filename

    # This function will accept an object type BookingDetails (representing a booking file) and will create a success
    # file with an additional column to represent whether the search resulted in a booking or not
    def create_search_success_file(self, booking_file, success_file_name, date_column,
                                   origin_column, destination_column):
        try:
            # open the result file in write mode
            with open(success_file_name, 'w') as success_file:
                csv_writer = csv.writer(success_file, delimiter='^')
                self.populate_success_file(csv_writer, booking_file, date_column, origin_column, destination_column)
        except IOError:
            print("Error creating result file - " + success_file_name)

    # This function will open the current search file and get the indices of date, destination and origin columns
    def populate_success_file(self, csv_writer, booking_file, date_column, origin_column, destination_column):
        try:
            # open the current search file in read mode
            with open(self.FileName, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='^')
                first_row = next(csv_reader)
                number_of_fields = len(first_row)
                # get the indices for date, origin and destionation columns
                destination_index = self.get_column_index(first_row, destination_column)
                date_index = self.get_column_index(first_row, date_column)
                origin_index = self.get_column_index(first_row, origin_column)

                # return if columns are not found
                if destination_index == -1 or date_index == -1 or origin_index == -1:
                    return

                # add the column_headers to the result file with an additional 'WasSearchSuccessful' column
                first_row.append('WasSearchSuccessful')
                csv_writer.writerow(first_row)

                # iterate over search entries
                self.populate_success_file_entries(csv_reader, csv_writer, booking_file.Booking_Dict, number_of_fields,
                                                   date_index, origin_index, destination_index)

        except IOError:
            print("File not found - " + self.FileName)

    # This function will iterate over all the search entries one by one and figure out if that search resulted
    # in a booking or not.
    @staticmethod
    def populate_success_file_entries(csv_reader, csv_writer, booking_dict, number_of_fields, date_index,
                                      origin_index, destination_index):
        # An entry will be skipped if it has missing data
        skipped = 0

        # iterate over each row
        for row in csv_reader:
            if len(row) == number_of_fields:
                # get the date, origin and destination
                date = row[date_index].split(" ")[0]
                origin = row[origin_index].strip()
                destination = row[destination_index].strip()

                # pass the date, origin, destination and dictionary to the to the helper function
                result = SearchDetails.check_if_booking_exists(booking_dict, date, origin, destination)
                # append the result to the row
                row.append(result)
                # write the row in result file
                csv_writer.writerow(row)
            else:
                skipped += 1
        print 'skipped rows = ' + str(skipped)

    @staticmethod
    def check_if_booking_exists(booking_dict, date, origin, destination):
        # if date is not present in booking dictionary, return 0
        if date not in booking_dict:
            return '0'
        # get the origin dictionary corresponding to the date
        origin_dict = booking_dict[date]

        # if origin is not in origin dictionary, return 0
        if origin not in origin_dict:
            return '0'
        # get the list of destinations from the origin
        destination_list = origin_dict[origin]

        # if destination is not in the list, return 0
        if destination not in destination_list:
            return '0'

        # destination is present in the list, return 1
        return '1'

    # This function will return the index of column_name from the first_row. If column does not exist in the first row
    # it will return -1
    @staticmethod
    def get_column_index(first_row, column_name):
        for i in range (0, len(first_row)):
            first_row[i] = first_row[i].strip()

        if column_name not in first_row:
            print 'Column ' + column_name + ' does not exist in the file'
            return -1

        return first_row.index(column_name)


def main():
    bookings_file_name = 'bookings.csv'
    search_file_name = 'searches.csv'
    booking_origin_column = 'dep_port'
    booking_destination_column = 'arr_port'
    booking_date_column = 'act_date'
    search_origin_column = 'Origin'
    search_destination_column = 'Destination'
    search_date_column = 'Date'
    result_file_name = 'search_success.csv'

    if os.path.exists(result_file_name):
        os.remove(result_file_name)

    bookings_file = BookingDetails(bookings_file_name)
    bookings_file.get_booking_details(booking_date_column, booking_origin_column, booking_destination_column)
    if not bookings_file.Booking_Dict:
        print 'Error reading booking records file, exiting..'
        return

    search_file = SearchDetails(search_file_name)
    search_file.create_search_success_file(bookings_file, result_file_name, search_date_column,
                                           search_origin_column, search_destination_column)

if __name__ == "__main__":
    main()
