# Flight Finder

A command-line interface (CLI) application to search for flights based on various criteria.

## Usage

python main.py departure destination [options]

### Positional arguments:

- `departure`: Departure location, e.g., Manchester
- `destination`: Destination location(s), e.g., Barcelona. For multiple possible destinations, separate the list with space, e.g., Barcelona Dublin.

### Optional arguments:

- `-h, --help`: Show the help message and exit.
- `--date-from DATE_FROM`: Search for flights from this date (format: YYYY-MM-DD, default: today).
- `--date-to DATE_TO`: Search for flights to this date (format: YYYY-MM-DD, default: one month from the date from).
- `--departure-day DEPARTURE_DAY`: Departure day, e.g., Friday. Cannot be used alongside --weekend option.
- `--return-day RETURN_DAY`: Return day, e.g., Sunday. Cannot be used alongside --weekend, --nights-in-dst-from, or --nights-in-dst-to options.
- `--weekend`: Boolean flag to search for weekend flights only, leave on Friday and return on Sunday. Cannot be used alongside --departure-day or --return-day options.
- `--dtime-from DTIME_FROM`: Earliest departure time (format: HH), default: 09. Note: a bigger dtime or rtime range may not return more results, e.g., 01 and 23. The API may prioritize later, cheaper flights. Better to set the times you actually wish to fly from.
- `--dtime-to DTIME_TO`: Latest departure time (format: HH), default: 9 hours later than dtime-from.
- `--rtime-from RTIME_FROM`: Earliest departure time of the returning flight (format: HH), default: 09.
- `--rtime-to RTIME_TO`: Latest departure time of the returning flight (format: HH), default: 9 hours later than rtime-from.
- `--nights-in-dst-from NIGHTS_IN_DST_FROM`: The minimum number of nights in the holiday destination. Cannot be used with --return-day or --weekend options. If not specified when --nights-in-dst-to is used, defaults to 1.
- `--nights-in-dst-to NIGHTS_IN_DST_TO`: The maximum number of nights in the holiday destination. Cannot be used with --return-day or --weekend options. If not specified when --nights-in-dst-from is used, defaults to the same value as --nights-in-dst-from.
- `--max-price MAX_PRICE`: Maximum price for the flights.
- `--email EMAIL`: Email to send the flight details to.







