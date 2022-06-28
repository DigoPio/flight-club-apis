import requests

SHEET_TOKEN = 'sdsdksiqhnaoam86629lmsn'
SHEET_ENDPOINT = 'https://api.sheety.co/1b13221e230fde4ea7488241e97c9e41/flightDeals/users'


SHEET_HEADER = {
    'Authorization': f'Bearer {SHEET_TOKEN}'
}

class Users:

    def __init__(self):
        self.user_data = {}
        print("Welcome to DigoPio's Flight Club.\nWe will find the best flight deals and email you.")
        self.user_first_name = input('What is your first name?\n').title()
        self.user_last_name = input('What is your last name?\n').title()
        self.user_email = input('What is your email\n')
        self.user_email_confirmation = input('Confirm your email\n')

    def add_users(self):
        if self.user_email == self.user_email_confirmation:
            self.user_data = {
                'user': {
                    'firstName': self.user_first_name,
                    'lastName': self.user_last_name,
                    'email': self.user_email
                }
            }
        response = requests.post(url=SHEET_ENDPOINT, json=self.user_data)
        print(response.text)





