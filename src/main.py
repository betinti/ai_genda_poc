from fastapi import FastAPI
from typing import Union
from MessageHandler import MessageHandler

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/recive-message/")
def recive_message(message):
    message_handler = MessageHandler()
    response = message_handler.handle_message(message)
    return {"response": response}