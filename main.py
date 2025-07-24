import psutil
import datetime
import logging

from fastapi.params import Form
from fastapi import FastAPI
from src.QrcodeService import QrCodeService
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

@app.get("/image_message_test")
def image_message_test():
    qrcode_service = QrCodeService()
    
    url = "ai-genda-poc-1.onrender.com/docs"
    print('Generating QR code for URL:', url)
    result = qrcode_service.qr_code_generator(url)
        
    if result['success']:
        logging.info(f"QR Code generated and uploaded successfully: {result['url']}")
    else:
        logging.error(f"Failed to generate or upload QR Code: {result.get('error', 'Unknown error')}")
    
    return {"response": result}

@app.post("/confirm_agenda_attendance")
async def confirm_agenda_attendance(agenda_id: str):
    """
    Endpoint to confirm agenda attendance.
    """
    logging.info(f"Agenda ID received: {agenda_id}")
    
    # Here you would typically handle the confirmation logic, e.g., updating a database record.
    
    return {"message": "Attendance confirmed", "agenda_id": agenda_id}
    

@app.post("/receive_message")
async def receive_message(
    Body: str = Form(None), 
    From: str = Form(None),
    NumMedia = Form(None)
    ):
    # Body contains the message text
    
    if NumMedia is not None:
        logging.info(f"Received media message with {NumMedia} media items.")
    
    message_handler = MessageHandler()
    response = message_handler.handle_message(Body, From)

    return response
