import csv

# An object of class BookingDetails will represent a csv file storing the booking details. Filename is the name of
# the file and Booking_Dict will be a kind of inverted index to find a booking entry with matching date, origin and
# destination


class BookingDetails(object):
    # constructor
    def __init__(self, filename):
        self.FileName = filename
        self.Booking_Dict = {}

    # get_booking_details: This function will create a dictionary of booking entries
    # for booking dictionary - key = date of booking, value = origin_dict
    # for origin_dict - key = origin, value = list of destinations from that origin
    def get_booking_details(self, date_column, origin_column, destination_column):
        try:
            # Load the csv file
            with open(self.FileName, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='^')
                first_row = next(csv_reader)

                # get the number of fields, destination column index, date column index and origin column index
                number_of_fields = len(first_row)
                destination_index = self.get_column_index(first_row, destination_column)
                date_index = self.get_column_index(first_row, date_column)
                origin_index = self.get_column_index(first_row, origin_column)

                # if all the columns are not present then return
                if destination_index == -1 or date_index == -1 or origin_index == -1:
                    return

                # create the booking dictionary
                self.Booking_Dict = self.create_booking_dict(csv_reader, number_of_fields, date_index,
                                                             origin_index, destination_index)

        except IOError:
            print("File not found - " + self.FileName)

    # create_booking_dict: This function will create the Booking dictionary from the booking file
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

                # update the origin dictionary entry for current date
                booking_dict[date] = self.add_origin_destination(booking_dict[date], origin, destination)
        return booking_dict

    # add_origin_destination: This function will add origin and destination to origin dictionary
    @staticmethod
    def add_origin_destination(origin_dict, origin, destination):
        # if origin is not in origin_dict then add it with empty list as its value
        if origin not in origin_dict:
            origin_dict[origin] = []

        # if destination is not in destination list for the origin then add it
        if destination not in origin_dict[origin]:
            origin_dict[origin].append(destination)
        return origin_dict

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
