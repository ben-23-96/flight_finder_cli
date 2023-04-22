from requests import get
from datetime import datetime
import pprint


class FlightSearch:
    """
    A class used to search for flight information using the Tequila API.

    Attributes
    location_endpoint : str : The API endpoint for fetching location information.
    search_endpoint : str : The API endpoint for performing flight searches.
    api_key_header : dict : The API key header for authentication with the Tequila API.

    Methods
    get_city_code(city) : Retrieves the IATA code for a given city.
    get_destination_codes(list_of_destinations) : Retrieves the IATA codes for a list of destinations.
    """

    def __init__(self):
        self.location_endpoint = 'http://tequila-api.kiwi.com/locations/query?'
        self.search_endpoint = 'https://tequila-api.kiwi.com/v2/search?'
        self.api_key_header = {'apikey': 'JZMGFnnggdy5A1IPNsjRG2r4Q4F6FWK0'}

    def get_city_code(self, city):
        """
        Retrieves the IATA code for a given city.

        Parameters
        city : str : The name of the city to fetch the IATA code for eg. manchester.

        Returns
        city_code : str : The IATA code for the city, or None if an error occurs.
        """
        params = {'term': city}
        city_code = None
        try:
            response = get(self.location_endpoint, params=params,
                           headers=self.api_key_header)
            data = response.json()
            city_code = data['locations'][0]['code']
        except Exception as e:
            print(f'unable to get city code for {city} due to error: {e}')
        return city_code

    def get_destination_codes(self, list_of_destinations):
        """
        Retrieves the IATA codes for a list of destinations.

        Parameters
        list_of_destinations : list : A list of destination names to fetch the IATA codes for.

        Returns
        city_code_string : str : A comma-separated string of IATA codes for the given destinations.
        """
        list_of_city_codes = []

        for place in list_of_destinations:
            city_code = self.get_city_code(place)
            # if code found without error append the code to the list
            if city_code:
                list_of_city_codes.append(city_code)

        city_codes_string = ','.join(list_of_city_codes)

        return city_codes_string

    def search_flights(self, params):
        """
        Searches for flights based on the provided parameters.

        Parameters
        params : object : An object containing the search parameters, as according to the tequila search api.

        Returns
        flight_by_destination : obj : a dictionary with keys for each destination, the value of each key is a list containing all found flights for that destination.
        """

        try:
            response = get(self.search_endpoint,
                           headers=self.api_key_header, params=params)
            data = response.json()['data']
        except Exception as e:
            print(f'an error occured: {e}')
            print(response.json()['error'])
        else:
            if len(data) > 0:
                # if flights found
                flights_by_destination = {}
                for flight in data:
                    # convert departure and return datetime strings into datetime objects
                    departure = flight['route'][0]['local_departure']
                    departure_datetime = datetime.strptime(
                        departure, '%Y-%m-%dT%H:%M:%S.%fZ')
                    returning = flight['route'][1]['local_departure']
                    returning_datetime = datetime.strptime(
                        returning, '%Y-%m-%dT%H:%M:%S.%fZ')
                    destination = flight['cityTo']
                    # create a object with valid information about the found flight
                    info = {'price': flight['price'],
                            'city from': flight['cityFrom'],
                            'departure_date': departure_datetime.date().strftime('%d/%m/%Y'),
                            'departure_time': departure_datetime.time().strftime('%H:%M'),
                            'city to': destination,
                            'return date': returning_datetime.date().strftime('%d/%m/%Y'),
                            'return time': returning_datetime.time().strftime('%H:%M'),
                            'link': flight['deep_link']}
                    if destination not in flights_by_destination:
                        flights_by_destination[destination] = []
                    flights_by_destination[destination].append(info)
                    pprint.pprint(info, indent=2)
                return flights_by_destination
            else:
                print('no flights found')
                print(response.json())
