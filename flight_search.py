import requests
from flight_data import FlightData
from pprint import pprint
from mysecrets import MySecrets


secrets = MySecrets()

TEQUILA_ID = secrets.TEQUILA_ID
TEQUILA_KEY = secrets.TEQUILA_KEY
TEQUILA_ENDPOINT = 'https://tequila-api.kiwi.com'
TEQUILA_LOCATIONS = '/locations/query'
TEQUILA_SEARCH = '/v2/search'

class FlightSearch:

    def get_city_code(self, city):
        headers = {
            'apikey': TEQUILA_KEY,
        }
        params = {
            'term': city,
            'location_types': 'city'
        }
        response = requests.get(url=f'{TEQUILA_ENDPOINT+TEQUILA_LOCATIONS}', params=params, headers=headers)
        data = response.json()
        city_code = data['locations'][0]['code']
        return city_code

    def search_for_flights(self, origin_code, destiny_code, date_from, date_to):
        tequila_header = {
            'apikey': TEQUILA_KEY
        }

        tequila_params = {
            'fly_from': origin_code,
            'fly_to': destiny_code,
            'dateFrom': date_from,
            'dateTo': date_to,
            'flight_type': 'round',
            'one_for_city': 1,
            'curr': 'BRL',
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            'max_stopovers': 0,


        }

        tequila_response = requests.get(url=f'{TEQUILA_ENDPOINT+TEQUILA_SEARCH}',
                                        params=tequila_params,
                                        headers=tequila_header)

        try:
            tequila_data = tequila_response.json()['data'][0]
        except IndexError:
            print('Exception activated')
            tequila_params['max_stopovers'] = 1
            tequila_response = requests.get(url=f'{TEQUILA_ENDPOINT + TEQUILA_SEARCH}',
                                            params=tequila_params,
                                            headers=tequila_header)
            try:
                tequila_data = tequila_response.json()['data'][0]

            except IndexError:
                return None
            else:
                if tequila_data['route'][0]['cityCodeTo'] == destiny_code:
                    flight_data = FlightData(price=tequila_data['price'], origin_city=tequila_data['route'][0]['cityFrom'],
                                             origin_airport=tequila_data['route'][0]['flyFrom'],
                                             destination_city=tequila_data['route'][0]['cityTo'],
                                             destination_airport=tequila_data['route'][0]['flyTo'],
                                             out_date=tequila_data['route'][0]['local_departure'].split('T')[0],
                                             return_date=tequila_data['route'][2]['local_departure'].split('T')[0],
                                             stop_overs=1, via_city=tequila_data['route'][1]['cityTo'],
                                             deep_link=tequila_data['deep_link'])
                    print(f'{flight_data.destination_city}: R${flight_data.price}')
                    return flight_data
                elif tequila_data['route'][0]['cityCodeTo'] != destiny_code:
                    flight_data = FlightData(price=tequila_data['price'],
                                             origin_city=tequila_data['route'][0]['cityFrom'],
                                             origin_airport=tequila_data['route'][0]['flyFrom'],
                                             destination_city=tequila_data['route'][1]['cityTo'],
                                             destination_airport=tequila_data['route'][1]['flyTo'],
                                             out_date=tequila_data['route'][0]['local_departure'].split('T')[0],
                                             return_date=tequila_data['route'][2]['local_departure'].split('T')[0],
                                             stop_overs=1, via_city=tequila_data['route'][0]['cityTo'],
                                             deep_link=tequila_data['deep_link'])
                    print(f'{flight_data.destination_city}: R${flight_data.price}')
                    return flight_data
        else:
            flight_data = FlightData(price=tequila_data['price'], origin_city=tequila_data['route'][0]['cityFrom'],
                                     origin_airport=tequila_data['route'][0]['flyFrom'],
                                     destination_city=tequila_data['route'][0]['cityTo'],
                                     destination_airport=tequila_data['route'][0]['flyTo'],
                                     out_date=tequila_data['route'][0]['local_departure'].split('T')[0],
                                     return_date=tequila_data['route'][1]['local_departure'].split('T')[0],
                                     deep_link=tequila_data['deep_link'])

            print(f'{flight_data.destination_city}: R${flight_data.price}')
            return flight_data











