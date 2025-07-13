import psutil
import datetime
import xmltodict
from pydantic import BaseModel
from fastapi import FastAPI, Request

from src.objects import TwilioMessage
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
async def recive_message(request: TwilioMessage):
    print(request)
    message_handler = MessageHandler()
    response = message_handler.initialize_conversation(request.to)
    return {"response": response}

@app.post("/recive-message")
async def recive_message(request: TwilioMessage):
    print(request)
    message_handler = MessageHandler()
    response = message_handler.handle_message(request.body)
    return {"response": response}

@app.post("/recive_message")
async def recive_message(request: TwilioMessage):
    print(request)
    message_handler = MessageHandler()
    response = message_handler.handle_message(request.body)
    return {"response": response}