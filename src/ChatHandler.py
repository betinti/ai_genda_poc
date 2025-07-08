import os
import time

from twilio.rest import Client
from dotenv import load_dotenv

# Carrega o .env em um caminho específico
load_dotenv(dotenv_path="env/.env")

class ChatHandler:
    def __init__(self):
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        
        self.default_from_number = os.getenv('TWILIO_DEFAULT_WHATSAPP_FROM_NUMBER')
        
        self.client = Client(account_sid, auth_token)
        
    def send_message(self, body, number_to, number_from=None):
        if number_from is None:
            number_from = self.default_from_number
        message = self.client.messages.create(
            to=f"whatsapp:{number_to}",
            from_=f"whatsapp:{number_from}",
            body=body
        )
        return message.sid
    
    def get_messages(self, to=None, from_=None):
        if from_ is None:
            from_ = self.default_from_number
        messages = self.client.messages.list(to=to, from_=from_)
        return messages