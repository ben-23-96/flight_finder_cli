from argparse import ArgumentParser, ArgumentTypeError
from datetime import datetime, time
from argument_validator import ArgumentValidator
from flight_searcher import FlightSearch
from email_sender import EmailSender


def main():
    parser = ArgumentParser(description="Flight finder")
    # set the arguments for the CLI

    parser.add_argument("departure", help="Departure location eg. manchester")

    parser.add_argument("destination", nargs='+',
                        help="Destination location(s) eg. barcelona or for multiple possible destinations seperate list with space eg.barcelona dublin ")

    parser.add_argument("--date-from", type=lambda s: datetime.strptime(s, '%d-%m-%Y').date(), default=datetime.now(
    ).date(), help="Search for flights from this date (format: DD-MM-YYYY, default: today)")

    parser.add_argument("--date-to", type=lambda s: datetime.strptime(s, '%d-%m-%Y').date(), default=None,
                        help="Search for flights to this date (format: DD-MM-YYYY, default: one month from date from)")

    parser.add_argument("--departure-day", type=str,
                        help="Departure day eg. friday. Cannot be used alongside --weekend option.")

    parser.add_argument("--return-day", type=str,
                        help="Return day eg. sunday. Cannot be used alongside --weekend, --nights-in-dst-from or --nights-in-dst-to options.")

    parser.add_argument("--weekend", action='store_true',
                        help="Boolean flag to search for weekend flights only, leave on friday return on sunday. Cannot be used alongside --departure-day or --return-day options.")

    parser.add_argument("--dtime-from", type=lambda s: datetime.strptime(s, '%H').time(), default=time(9, 0),
                        help="Earliest departure time (format: HH), default: 09, note: a bigger dtime or rtime range may not return more results eg. 01 and 23, the api may end up prioritsing later cheaper flights, better to set to times you are actually wish to fly from.")

    parser.add_argument("--dtime-to", type=lambda s: datetime.strptime(s, '%H').time(),
                        help="Latest departure time (format: HH), default: 9 hours later than dtime-from")

    parser.add_argument("--rtime-from", type=lambda s: datetime.strptime(s, '%H').time(), default=time(9, 0),
                        help="Earliest departure time of returning flight (format: HH), default: 09")

    parser.add_argument("--rtime-to", type=lambda s: datetime.strptime(s, '%H').time(),
                        help="Latest departure time of returning flight (format: HH), default: 9 hours later than rtime-from")

    parser.add_argument("--nights-in-dst-from", type=int, default=None,
                        help="The minimum numbers of nights in  the holiday desination. Cannot be used with --return-day or --weekend options. If not specified when --nights-in-dst-to is used defaults to 1.")

    parser.add_argument("--nights-in-dst-to", type=int, default=None,
                        help="The maximum numbers of nights in  the holiday desination. Cannot be used with --return-day or --weekend options. If not specified when --nights-in-dst-from is used defaults to the same value as --nights-in-dst-from.")

    parser.add_argument("--max-price", type=int,
                        default=None, help="Maximum price for the flights")

    parser.add_argument("--email", type=str,
                        default=None, help="Email to send the flights too.")

    args = parser.parse_args()
    try:
        # check arguments are valid, can be used together and set some defaults
        argument_validator = ArgumentValidator(args)
        argument_validator.validate_arguments()
    except ArgumentTypeError as e:
        print(e)
        return
    flight_searcher = FlightSearch()

    # get the airport codes to be used in the search for flghts
    departure_location_code = flight_searcher.get_city_code(args.departure)
    destination_location_codes = flight_searcher.get_destination_codes(
        args.destination)

    print("Departure location:", args.departure)
    print("Destination locations:", ', '.join(args.destination))

    # print the argument values given, search params the object to be used in the api request to find the flights
    search_params = argument_validator.confirm_validated_arguments()
    search_params['fly_from'] = departure_location_code
    search_params['fly_to'] = destination_location_codes
    search_params['flight_type'] = 'round'
    search_params['ret_from_diff_city'] = False
    search_params['ret_to_diff_city'] = False
    search_params['max_stopovers'] = 0

    user_confirm = input("\nDo you want to search using thes values? Y/n   ")
    if user_confirm.lower() == 'y':
        print(search_params)
        # search for flights
        flights = flight_searcher.search_flights(search_params)
        if args.email:
            email_sender = EmailSender()
            email_sender.create_email(flights, args.email)
    else:
        return


if __name__ == "__main__":
    main()
