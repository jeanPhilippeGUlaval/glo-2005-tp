import os
from dotenv import load_dotenv


port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = os.environ.get('MAIL_USERNAME')  # Enter your address
password = os.environ.get('MAIL_PASSWORD')
