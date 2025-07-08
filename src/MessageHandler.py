from ChatHandler import ChatHandler
from src.AssitantHandler import AssistantHandler

class MessageHandler:
    def __init__(self):
        """
        Initializes the MessageHandler class.
        """
            
    def handle_message(self, message): #TODO: type the param
        """
        Handles incoming messages and stores them in the message list.
        
        Args:
            message (str): The message to be handled.
        """
        #Send the message to GPT Assitant
        assitant_handler = AssistantHandler()
        
        response = assitant_handler.get_assistant_response(message)
        
        #Send the response to the user
        chat_handler = ChatHandler()
        
        chat_handler.send_message(response, message['from'])
                
        
        return {"status": "success", "message": "Message received successfully."}