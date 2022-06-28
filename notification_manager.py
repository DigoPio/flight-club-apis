from twilio.rest import Client
import smtplib
from data_manager import DataManager
from mysecrets import MySecrets

secrets = MySecrets()

account_sid = secrets.account_sid
auth_token = secrets.auth_token
smtp = 'smtp.gmail.com'
port = 587
MY_EMAIL = secrets.MY_EMAIL
MY_PASSWORD = secrets.MY_PASSWORD


class NotificationManager:
    def __init__(self):
        self.client = Client(account_sid, auth_token)


    def send_message(self, ready_message):
        message = self.client.messages.create(
                body=ready_message,
                from_= secrets.from_sms,
                to= secrets.to_sms
            )

    def send_email(self, mail_msg):
        data = DataManager()
        user_email = data.get_user_data()
        with smtplib.SMTP('smtp.gmail.com', port=port) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PASSWORD)
            for row in user_email:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=row['email'],
                    msg=f"Subject:Cheap flight alert!\n\nHi {row['firstName']}!!\n{mail_msg}")
                print('msg sent')

