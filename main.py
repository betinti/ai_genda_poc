import psutil
import datetime

from fastapi import FastAPI
from src.MessageHandler import MessageHandler

app = FastAPI()

@app.get("/health")
def health():
    return {
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'cpu': f"{psutil.cpu_percent()}%",
        'memory': f"{psutil.virtual_memory().percent}%"
    }

@app.post("/send-initial-message")
def recive_message(to_phone_number):
    print(to_phone_number)
    message_handler = MessageHandler()
    response = message_handler.initialize_conversation(to_phone_number)
    return {"response": response}

@app.post("/recive-message")
def recive_message(message):
    print(message)
    message_handler = MessageHandler()
    response = message_handler.handle_message(message)
    return {"response": response}