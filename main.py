import psutil
import datetime
import xmltodict
from pydantic import BaseModel
from fastapi import FastAPI, Request

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
async def recive_message(request: Request):
    print(request)
    body = await request.body()
    data = xmltodict.parse(body)
    # Adjust the path to 'to_phone_number' as per your XML structure
    to_phone_number = data.get('root', {}).get('to_phone_number')
    print(to_phone_number)
    message_handler = MessageHandler()
    response = message_handler.initialize_conversation(to_phone_number)
    return {"response": response}

@app.post("/recive-message")
async def recive_message(request: Request):
    print(request)
    body = await request.body()
    data = xmltodict.parse(body)
    # Adjust the path to 'message' as per your XML structure
    message = data.get('root', {}).get('message')
    print(message)
    message_handler = MessageHandler()
    response = message_handler.handle_message(message)
    return {"response": response}

@app.post("/recive_message")
async def recive_message(request: Request):
    print(request)
    body = await request.body()
    data = xmltodict.parse(body)
    # Adjust the path to 'message' as per your XML structure
    message = data.get('root', {}).get('message')
    print(message)
    message_handler = MessageHandler()
    response = message_handler.handle_message(message)
    return {"response": response}