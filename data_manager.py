import requests
from mysecrets import MySecrets

secrets = MySecrets()

SHEET_TOKEN = secrets.sheet_token
SHEET_ENDPOINT = secrets.sheet_endpoint
SHEET_USER_ENDPOINT = secrets.sheet_user_endpoint

SHEET_HEADER = {
    'Authorization': f'Bearer {SHEET_TOKEN}'
}


class DataManager:
    def __init__(self):
        self.destination_data = {}


    def get_destination_data(self):
        response = requests.get(url=SHEET_ENDPOINT)
        data = response.json()
        self.destination_data = data['prices']
        return self.destination_data

    def update_destination_iata(self):
        for city in self.destination_data:
            new_data = {
                'price': {
                    'iataCode': city['iataCode']
                }
            }
            response = requests.put(url=f"{SHEET_ENDPOINT}/{city['id']}", json=new_data)
            print(response.text)

    def get_user_data(self):
        response = requests.get(url=SHEET_USER_ENDPOINT)
        self.user_data = response.json()['users']
        return self.user_data


