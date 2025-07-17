from typing import Optional
from fastapi.params import Form
import psutil
import datetime
import logging



from pydantic import BaseModel
from fastapi import FastAPI, Request, Response
from src.models.TwilioMessageModel import TwilioMessageModel
from src.MessageHandler import MessageHandler

app = FastAPI()

logging.basicConfig(level=logging.INFO)

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
async def receive_message(Body: str = Form(None), From: str = Form(None)):
    # Body contains the message text
    logging.info(f"Received Body '{Body}' and From '{From}'")
    
    message_handler = MessageHandler()
    response = message_handler.handle_message(Body, From)
    
    return {"response": response}