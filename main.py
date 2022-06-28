from data_manager import DataManager
from flight_search import FlightSearch
from datetime import datetime, timedelta
from notification_manager import NotificationManager
from users import Users


ORIGIN_CITY_IATA = 'SSA'
users = Users()
users.add_users()

time_now = datetime.now()
date_now = time_now.date().strftime('%d/%m/%Y')
date_in_six_months = (time_now + timedelta(days=180)).date().strftime('%d/%m/%Y')
date_in_7_days = (time_now + timedelta(days=7)).date().strftime('%d/%m/%Y')
date_in_28_days = (time_now + timedelta(days=28)).date().strftime('%d/%m/%Y')

data_manager = DataManager()
sheet_data = data_manager.get_destination_data()

flight_search = FlightSearch()

if sheet_data[0]['iataCode'] == "":
    for city in sheet_data:
        city['iataCode'] = flight_search.get_city_code(city['city'])
    data_manager.destination_data = sheet_data
    data_manager.update_destination_iata()

for city in sheet_data:
    flight = flight_search.search_for_flights(origin_code=ORIGIN_CITY_IATA,
                                                 destiny_code=city['iataCode'],
                                                 date_from=date_now, date_to=date_in_six_months)
    try:
        if flight.price < city['lowestPrice']:
            notification = NotificationManager()
            ready_message = f"Low price alert! Only {flight.price} R$ to fly" \
                            f" from {flight.origin_city}-{flight.origin_airport} to" \
                            f" {flight.destination_city}-{flight.destination_airport}, from " \
                            f"{flight.out_date} to {flight.return_date}"

            if flight.stop_overs > 0:
                ready_message += f'\nFlight has {flight.stop_overs} stop over, via {flight.via_city}'
            link = f"Link: {flight.deep_link}"
            notification.send_message(ready_message=ready_message)
            notification.send_email(mail_msg=f"{ready_message}\n{link}")

    except AttributeError:
        pass



