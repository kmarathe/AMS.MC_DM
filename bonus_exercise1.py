import os
from bonus_exercise_bookings import BookingDetails
from bonus_exercise_search import SearchDetails


def main():
    # name of files containing booking and search entries
    bookings_file_name = 'sample_bookings.csv'
    search_file_name = 'sample_searches.csv'

    # column headers for origin, destination and date columns in booking file
    booking_origin_column = 'dep_port'
    booking_destination_column = 'arr_port'
    booking_date_column = 'act_date'

    # column headers for origin, destination and date columns in search file
    search_origin_column = 'Origin'
    search_destination_column = 'Destination'
    search_date_column = 'Date'

    # desired path of result file
    result_file_name = 'search_success.csv'

    # if result file already exists, delete it
    if os.path.exists(result_file_name):
        os.remove(result_file_name)

    # create an object for booking file
    bookings_file = BookingDetails(bookings_file_name)
    # get the booking details in booking_dict
    bookings_file.get_booking_details(booking_date_column, booking_origin_column, booking_destination_column)

    # create an object for search file
    search_file = SearchDetails(search_file_name)
    # create result file
    search_file.create_search_success_file(bookings_file, result_file_name, search_date_column, search_origin_column,
                                           search_destination_column)


if __name__ == "__main__":
    main()
