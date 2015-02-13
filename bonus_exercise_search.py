import csv

# An object of class SearchDetails will represent a file which stores the search details.


class SearchDetails(object):
    # constructor
    def __init__(self, filename):
        self.FileName = filename

    # create_search_success_file: This function will accept an object type BookingDetails (representing a booking file)
    # and will create a success file with an additional column to represent whether
    # the search resulted in a booking or not
    def create_search_success_file(self, booking_file, success_file_name, date_column,
                                   origin_column, destination_column):
        # if booking dictionary is empty, return
        if not booking_file.Booking_Dict:
            print 'Error reading booking records file, exiting..'
            return

        try:
            # open the result file in write mode
            with open(success_file_name, 'w') as success_file:
                csv_writer = csv.writer(success_file, delimiter='^')
                self.populate_success_file(csv_writer, booking_file, date_column, origin_column, destination_column)
        except IOError:
            print("Error creating result file - " + success_file_name)

    # populate_success_file: This function will open the current search file and populate the result file with
    # appropriate result
    def populate_success_file(self, csv_writer, booking_file, date_column, origin_column, destination_column):
        try:
            # open the current search file in read mode
            with open(self.FileName, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='^')
                first_row = next(csv_reader)

                # get the number of fields, date column index, origin column index and destination column index
                number_of_fields = len(first_row)
                destination_index = self.get_column_index(first_row, destination_column)
                date_index = self.get_column_index(first_row, date_column)
                origin_index = self.get_column_index(first_row, origin_column)

                # return if columns are not found
                if destination_index == -1 or date_index == -1 or origin_index == -1:
                    return

                # add the column_headers to the result file with an additional 'WasSearchSuccessful' column
                first_row.append('WasSearchSuccessful')
                csv_writer.writerow(first_row)

                # iterate over search entries and populate the success file accordingly
                self.populate_success_file_entries(csv_reader, csv_writer, booking_file.Booking_Dict, number_of_fields,
                                                   date_index, origin_index, destination_index)

        except IOError:
            print("File not found - " + self.FileName)

    # populate_success_file_entries: This function will iterate over all the search entries one by one and
    # figure out if that search resulted in a booking or not.
    @staticmethod
    def populate_success_file_entries(csv_reader, csv_writer, booking_dict, number_of_fields, date_index,
                                      origin_index, destination_index):
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

    # check_if_booking_exists: This function will check if an entry in booking_dict is present or not for
    # a booking from 'origin' to 'destination' on 'date'
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
