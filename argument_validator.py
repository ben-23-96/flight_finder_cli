from argparse import ArgumentTypeError
from datetime import datetime, timedelta, time


class ArgumentValidator:
    """
    A class to validate command line arguments for a flight search application.

    Attributes
    args : object : The command line arguments to be validated.
    search_params : object : A dictionary to store validated search parameters.

    Methods
    validate_arguements : Validates all command line arguments and returns the updated arguments.
    validate_flight_dates(date_from, date_to) : Validates the flight search date range and returns the updated date range.
    validate_flight_hours(time_from, time_to) : Validates the flight hours and returns the times as strings.
    validate_days_options(weekend, departure_day, return_day, nights_in_dst_from, nights_in_dst_to) : Validates the days options for the flight search.
    validate_flight_day(day) : Validates the flight day returns the day index.
    work_out_nights_between(departure_day_index, return_day_index) : Calculates the number of nights between the departure and return days.
    confirm_validated_arguments : Prints and stores the validated arguments into the search_params dictionary.
    """

    def __init__(self, args):
        """
        Parameters
        args : obj : the parsed command line arguments to be validated
        """
        self.args = args
        self.search_params = {}

    def validate_arguments(self):
        """
        Validates all command line arguments and returns the updated arguments.

        Returns
        self.args : The validated command line arguments.
        """
        # Validate flight date range
        self.args.date_from, self.args.date_to, self.args.return_from, self.args.return_to = self.validate_flight_dates(
            self.args.date_from, self.args.date_to)

        # Validate departure and return flight hours
        self.args.dtime_from, self.args.dtime_to = self.validate_flight_hours(
            self.args.dtime_from, self.args.dtime_to)
        self.args.rtime_from, self.args.rtime_to = self.validate_flight_hours(
            self.args.rtime_from, self.args.rtime_to)

        # Validate departure and return days, and number of nights at destination
        self.args.departure_day_index, self.args.return_day_index, self.args.nights_in_dst_from, self.args.nights_in_dst_to = self.validate_days_options(
            self.args.weekend, self.args.departure_day, self.args.return_day, self.args.nights_in_dst_from, self.args.nights_in_dst_to)

        return self.args

    def validate_flight_dates(self, date_from, date_to):
        """
        Validates the flight search date range and returns the updated date range.

        Parameters:
        date_from : date : The start date of the range of dates to search in for departing flights.
        date_to : date : The end date of the range of dates to search in for departing flights.

        Returns:
        date_from, date_to, return_from, return_to : tuple : str : The validated date ranges to search for flights in as strings dd/mm/yyyy, date are for departing flights, return are for returning flights. 

        Raises:
        argparse.ArgumentTypeError: If the date range is invalid.
        """
        today = datetime.now().date()

        if not date_to and date_from:
            # set date_to to 1 month after date_from if not set
            date_to = date_from + timedelta(days=30)

        # check dates are not in the past
        if date_from < today:
            raise ArgumentTypeError(
                "Date from cannot be in the past.")

        if date_to < today:
            raise ArgumentTypeError("Date to cannot be in the past.")

        # check date from is earlier than date to
        if date_to <= date_from:
            raise ArgumentTypeError(
                "Date to must be later than date from.")

        # change dates to strings in form dd/mm/yyyy, set return from and to
        return_from = (date_from + timedelta(days=1)).strftime("%d/%m/%Y")
        date_from = date_from.strftime("%d/%m/%Y")
        return_to = (date_to + timedelta(days=7)).strftime("%d/%m/%Y")
        date_to = date_to.strftime("%d/%m/%Y")
        return date_from, date_to, return_from, return_to

    def validate_flight_hours(self, time_from, time_to):
        """
        Validates the flight hours and returns the times as strings.

        Parameters:
        from_time : time : The earliest hour to fly.
        to_time : time : The latest hour to fly.

        Returns:
        tuple: str : the validated time from and time to as strings in format HH:MM

        Raises:
        argparse.ArgumentTypeError: If the time range is invalid.
        """
        # if time_to is not provided, set it to a default of 9 hours later than time_from, or 23:00 if less than 9 hours til midnight
        if not time_to:
            if time_from >= time(15, 0):
                time_to = time(23, 0)
            else:
                time_to = (datetime.combine(datetime.today(),
                           time_from) + timedelta(hours=9)).time()

        # check time_from is earlier than time_to
        if time_from >= time_to:
            raise ArgumentTypeError(
                'time-from must be earlier than time-to')

        return time_from.strftime('%H:%M'), time_to.strftime('%H:%M')

    def validate_days_options(self, weekend, departure_day, return_day, nights_in_dst_from, nights_in_dst_to):
        """
        Validates the days options for the flight search.

        Paramters:
        weekend (bool): Whether the user wants a weekend trip.
        departure_day (str): The departure day.
        return_day (str): The return day.
        nights_in_dst_from (int): The minimum number of nights in the destination.
        nights_in_dst_to (int): The maximum number of nights in the destination.

        Returns:
        tuple: int: The validated day options (departure_day_index, return_day_index, nights_in_dst_from, nights_in_dst_to).

        Raises:
        argparse.ArgumentTypeError: If the day options are invalid.
        """
        # check weekend option does not clash with other options
        if weekend and (departure_day or return_day or nights_in_dst_from or nights_in_dst_to):
            raise ArgumentTypeError(
                "Cannot provide departure day or return day or nights in destination when weekend option is set to true.")

        # check night_in_dst options do not clash and set defaults if nessacary
        if nights_in_dst_from or nights_in_dst_to:
            if return_day:
                raise ArgumentTypeError(
                    "Cannot provide return day alongside nights in destination options.")
            # set as supplied value or default 1
            nights_in_dst_from = nights_in_dst_from or 1
            # set as supplied value or default equal to nights_in_dst_from
            nights_in_dst_to = nights_in_dst_to or nights_in_dst_from

        # check nights_in_dst_from is not greater than nights_in_dst_to
        if nights_in_dst_to and nights_in_dst_from and nights_in_dst_from > nights_in_dst_to:
            raise ArgumentTypeError(
                "Nights in destination from cannot be greater than nights in destination to.")

        # validate departure and return days are days, day index is set eg sunday = 0
        departure_day_index = self.validate_flight_day(
            departure_day) if departure_day else None
        return_day_index = self.validate_flight_day(
            return_day) if return_day else None

        # Calculate nights in destination based on departure and return days
        if departure_day_index and return_day_index:
            nights_in_dst_from = self.work_out_nights_between(
                departure_day_index, return_day_index)
            nights_in_dst_to = nights_in_dst_from

        return departure_day_index, return_day_index, nights_in_dst_from, nights_in_dst_to

    def validate_flight_day(self, day):
        """
        Validates the flight day returns the day index.

        Parameters:
        day : str : The flight day to validate.

        Returns:
        int: The index of the validated flight day in the list of days. eg sunday = 0

        Raises:
        argparse.ArgumentTypeError: If the flight day is invalid.
        """
        days = ['sunday', 'monday', 'tuesday',
                'wednesday', 'thursday', 'friday', 'saturday']
        if day.lower() not in days:
            raise ArgumentTypeError(
                f"{day} is not a valid day. Use full day name eg. monday")
        return days.index(day)

    def work_out_nights_between(self, departure_day_index, return_day_index):
        """
        Calculates the number of nights between the departure and return days.

        Paramters:
        departure_day_index : int : The index of the departure day in the list of days. where sunday = 0
        return_day_index : int : The index of the return day in the list of days.

        Returns:
        int: The number of nights between the departure and return days.
        """
        nights = return_day_index - departure_day_index
        if nights <= 0:
            nights += 7
        return nights

    def confirm_validated_arguments(self):
        """
        Prints and stores the validated arguments into the search_params dictionary.

        Returns:
        dict: The updated search_params dictionary with the confirmed arguments.
        """
        if self.args.date_from:
            print("Date range from:", self.args.date_from)
            self.search_params['date_from'] = self.args.date_from
            self.search_params['return_from'] = self.args.return_from
        if self.args.date_to:
            print("Date range to:", self.args.date_to)
            self.search_params['date_to'] = self.args.date_to
            self.search_params['return_to'] = self.args.return_to
        if self.args.departure_day:
            print("Departure day:", self.args.departure_day)
            self.search_params['fly_days'] = self.args.departure_day_index
        if self.args.return_day:
            print("Return day:", self.args.return_day)
            self.search_params['return_fly_days'] = self.args.return_day_index
        if self.args.weekend:
            print("Search for weekend flights only")
            self.search_params['fly_days'] = 5
            self.search_params['return_fly_days'] = 0
            self.search_params['nights_in_dst_from'] = 2
            self.search_params['nights_in_dst_to'] = 2
        if self.args.dtime_from:
            print('Earliest departure time:', self.args.dtime_from)
            self.search_params['dtime_from'] = self.args.dtime_from
        if self.args.dtime_to:
            print('Latest departure time:', self.args.dtime_to)
            self.search_params['dtime_to'] = self.args.dtime_to
        if self.args.rtime_from:
            print('Earliest departure time of returning flight:',
                  self.args.rtime_from)
            self.search_params['ret_dtime_from'] = self.args.rtime_from
        if self.args.rtime_to:
            print('Latest departure time of returning flight:',
                  self.args.rtime_to)
            self.search_params['ret_dtime_to'] = self.args.rtime_to
        if self.args.nights_in_dst_from:
            print("The minimum number of nights in the destination:",
                  self.args.nights_in_dst_from)
            self.search_params['nights_in_dst_from'] = self.args.nights_in_dst_from
        if self.args.nights_in_dst_to:
            print("The maximum number of nights in the destination:",
                  self.args.nights_in_dst_to)
            self.search_params['nights_in_dst_to'] = self.args.nights_in_dst_to
        if self.args.max_price:
            print("Maximum price:", self.args.max_price)
            self.search_params['price_to'] = self.args.max_price
        if self.args.email:
            print("Email:", self.args.email)

        return self.search_params
