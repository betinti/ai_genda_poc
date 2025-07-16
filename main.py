import psutil
import datetime
import json

from pydantic import BaseModel
from fastapi import FastAPI
from src.models.TwilioMessageModel import TwilioMessageModel
from src.MessageHandler import MessageHandler

app = FastAPI()

class PhoneNumberRequest(BaseModel):
    to_phone_number: str

class MessageRequest(BaseModel):
    message: str

@app.get("/health")
def health():
    return {
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'cpu': f"{psutil.cpu_percent()}%",
        'memory': f"{psutil.virtual_memory().percent}%"
    }

@app.post("/send-initial-message")
def recive_message(request):
    print("Received request:", request)
    message_handler = MessageHandler()
    response = message_handler.initialize_conversation(request.to)
    return {"response": response}

@app.post("/recive_message")
def recive_message(request):
    print("Received request:", request)
    data = json.loads(request)
    print("Parsed data body:", data['body'])
    message = TwilioMessageModel.parse_obj(data)
    
    message_handler = MessageHandler()
    response = message_handler.handle_message(message.body)
    return {"response": response}