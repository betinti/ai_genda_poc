import psutil
import datetime
from pydantic import BaseModel

from fastapi import FastAPI
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
def recive_message(request: PhoneNumberRequest):
    print(request.to_phone_number)
    message_handler = MessageHandler()
    response = message_handler.initialize_conversation(request.to_phone_number)
    return {"response": response}

@app.post("/recive-message")
def recive_message(request: MessageRequest):
    print(request)
    message_handler = MessageHandler()
    response = message_handler.handle_message(request.message)
    return {"response": response}

@app.post("/recive_message")
def recive_message(request: MessageRequest):
    print(request)
    message_handler = MessageHandler()
    response = message_handler.handle_message(request.message)
    return {"response": response}