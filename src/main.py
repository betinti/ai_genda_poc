import psutil
import datetime

from fastapi import FastAPI
from MessageHandler import MessageHandler

app = FastAPI()

@app.get("/health")
def health():
    return {
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat(),
        'cpu': f"{psutil.cpu_percent()}%",
        'memory': f"{psutil.virtual_memory().percent}%"
    }

@app.post("/recive-message")
def recive_message(message):
    message_handler = MessageHandler()
    response = message_handler.handle_message(message)
    return {"response": response}