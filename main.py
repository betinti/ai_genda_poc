from typing import Optional
from fastapi.params import Form
import psutil
import datetime
import json
import xmltodict
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
async def whatsapp_webhook_1(Body: str = Form(...)):
    # Body contains the message text
    logging.info(f"Received form data: {Body}")
    
    message_handler = MessageHandler()
    response = message_handler.handle_message(Body)
    
    return {"response": response}

@app.post("/webhook_2")
async def whatsapp_webhook_2(request: Request):
    form_data = await request.form()
    message_body = form_data.get("Body", "")
    from_number = form_data.get("From", "")
    
    return {"status": message_body}

@app.post("/webhook_3")
async def whatsapp_webhook_3(request: Request):
    form_data = await request.form()
    logging.info(f"Received form data: {dict(form_data)}")
    
    body = form_data.get("Body", "")
    return {"status": "received"}

# def recive_message(request: str):
#     print("Received request:", request)
    
#     data_dict = xmltodict.parse(request)
#     print("Parsed XML data:", data_dict)
#     print("My message:", data_dict['Response']['Message']['Body'])
#     # data = json.loads(request)
#     # print("Parsed data body:", data['body'])
#     # message = TwilioMessageModel.parse_obj(data)
    
#     # message_handler = MessageHandler()
#     # response = message_handler.handle_message(message.body)
    
#     return {"response": data_dict['Response']['Message']['Body']}
