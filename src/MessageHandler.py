from src.AssitantHandler import AssistantHandler


class MessageHandler:
    def __init__(self):
        self.messages = []
        
    def handle_message(self, message): #TODO: type the param
        """
        Handles incoming messages and stores them in the message list.
        
        Args:
            message (str): The message to be handled.
        """
        #TODO: Send it to GPT Assitant
        assitant_handler = AssistantHandler()
        
        response = assitant_handler.get_assistant_response(message)
        
        #TODO: Send the response to the user
        
        self.messages.append(message)
        return {"status": "success", "message": "Message received successfully."}