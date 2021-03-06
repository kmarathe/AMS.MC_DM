import csv

# An object of class CSVFileReader will represent a CSV file. It supports a method which will print the
# count of number of lines in CSV file


class CSVFileReader(object):
    # constructor
    def __init__(self, filename):
        self.FileName = filename

    # number_of_lines: This function will print the number of lines in current file.
    # If file is not found it will display error message.
    def number_of_lines(self):
        count = 0
        # try block to handle the file not found exception
        try:
            with open(self.FileName, 'r') as csvfile:
                csvreader = csv.reader(csvfile, delimiter='^')
                # Iterate over the lines and increase the count by one
                for row in csvreader:
                    count += 1
                print 'Number of lines in ' + self.FileName + ' = ' + str(count)
        except IOError:
            # print the error message
            print("File not found - " + self.FileName)


def main():
    # path for the search file
    search_file_name = 'searches.csv'
    # path for the booking file
    bookings_file_name = 'bookings.csv'

    # objects for search and booking files
    search_file = CSVFileReader(search_file_name)
    bookings_file = CSVFileReader(bookings_file_name)

    # call the functions to display number of lines
    search_file.number_of_lines()
    bookings_file.number_of_lines()


if __name__ == "__main__":
    main()