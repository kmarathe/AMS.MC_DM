import csv


class BookingDetails(object):
    def __init__(self, filename):
        self.FileName = filename
        self.Booking_Dict = {}

    # This function will create a dictionary of booking entries
    def get_booking_details(self, date_column, origin_column, destination_column):
        try:
            with open(self.FileName, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter='^')
                first_row = next(csv_reader)
                number_of_fields = len(first_row)
                destination_index = self.get_column_index(first_row, destination_column)
                date_index = self.get_column_index(first_row, date_column)
                origin_index = self.get_column_index(first_row, origin_column)

                if destination_index == -1 or date_index == -1 or origin_index == -1:
                    return

                self.Booking_Dict = self.create_booking_dict(csv_reader, number_of_fields, date_index,
                                                             origin_index, destination_index)
                print self.Booking_Dict
        except IOError:
            print("File not found - " + self.FileName)

    # This function will populate the Booking dictionary from the booking file
    def create_booking_dict(self, csv_reader, number_of_fields, date_index, origin_index, destination_index):
        booking_dict = {}
        for row in csv_reader:
            if len(row) == number_of_fields:
                date = row[date_index].split(" ")[0]
                origin = row[origin_index].strip()
                destination = row[destination_index].strip()
                if date not in booking_dict:
                    booking_dict[date] = {}

                booking_dict[date] = self.add_origin_destination(booking_dict[date], origin, destination)
        return booking_dict

    @staticmethod
    def add_origin_destination(origin_dict, origin, destination):
        if origin not in origin_dict:
            origin_dict[origin] = []

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


def main():
    bookings_file_name = 'sample_bookings.csv'
    origin_column = 'dep_port'
    destination_column = 'arr_port'
    date_column = 'act_date'

    bookings_file = BookingDetails(bookings_file_name)
    bookings_file.get_booking_details(date_column, origin_column, destination_column)

if __name__ == "__main__":
    main()
