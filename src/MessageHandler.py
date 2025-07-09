import json

from src.ChatHandler import ChatHandler
from src.AssitantHandler import AssistantHandler

class MessageHandler:
    def __init__(self):
        """
        Initializes the MessageHandler class.
        """
           
    def initialize_conversation(self, to_phone_number: str):
        """
        Initializes a conversation by sending a welcome message.
        This method can be expanded to include more complex initialization logic.
        """
        
        assitant_handler = AssistantHandler()
        
        response = assitant_handler.get_initial_message()
        
        #Send the response to the user
        response = self.send_message(response, to_phone_number)
        
        return response
            
    def handle_message(self, data: str):
        """
        Handles incoming messages and stores them in the message list.
        
        Args:
            message (str): The message to be handled.
        """
        
        try:
            data_json = json.loads(data)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            return {"status": "error", "message": "Invalid JSON format."}
        
        message = data_json.get("message", "No message found")
        phone_from = data_json.get("from", "No phone found")
        
        #Send the message to GPT Assitant
        assitant_handler = AssistantHandler()
        
        response = assitant_handler.get_assistant_response(message)
        
        #Send the response to the user
        response = self.send_message(response, phone_from)

        return response
    
    def send_message(self, message: str, to_phone_number: str):
        """
        Sends a message to the specified phone number.
        
        Args:
            message (str): The message to be sent.
            to_phone_number (str): The phone number to send the message to.
        """
        
        chat_handler = ChatHandler()
        
        chat_handler.send_message(message, to_phone_number)
        
        return {"status": "success", "message": f"Message sent to {to_phone_number}."}