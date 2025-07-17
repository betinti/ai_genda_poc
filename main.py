from fastapi.params import Form
import psutil
import datetime
import logging

from fastapi import FastAPI
from src.AssitantHandler import AssistantHandler
from src.MessageHandler import MessageHandler

app = FastAPI()

logging.basicConfig(level=logging.INFO)

@app.get("/health")
def health():
    return {
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'cpu': f"{psutil.cpu_percent()}%",
        'memory': f"{psutil.virtual_memory().percent}%"
    }

@app.post("/send-initial-message")
def recive_message(request: str):
    print("Received request:", request)
    message_handler = MessageHandler()
    response = message_handler.initialize_conversation(request)
    return {"response": response}

@app.post("/recive_message")
async def receive_message(Body: str = Form(None), From: str = Form(None)):
    # Body contains the message text
    
    from_ = From.split(":")[1]  # The phone number of the sender 
    logging.info(f"Received Body '{Body}' and From '{from_}'")
    
    message_handler = MessageHandler()
    response = message_handler.handle_message(Body, from_)

    return response
