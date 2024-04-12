import os
from dotenv import load_dotenv

# Configuration pour le server SMTP
load_dotenv(override=True)
port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = os.environ.get('MAIL_USERNAME')  # Enter your address
password = os.environ.get('MAIL_PASSWORD')
