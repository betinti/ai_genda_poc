import openai
import time
import os 

from CommonHelper import file_to_string
from dotenv import load_dotenv

# Carrega o .env em um caminho específico
load_dotenv(dotenv_path="env/.env")


class AssistantHandler:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.assistantId : str = os.getenv('OPENAI_ASSISTANT_ID')
        thread = openai.beta.threads.create()
        self.threadId = thread.id

    def get_assistant_response(self, message: str):
        # Add a message from the user
        openai.beta.threads.messages.create(
            thread_id=self.threadId,
            role="user",
            content=message
        )

        # Run the assistant on this thread
        run = openai.beta.threads.runs.create(
            thread_id=self.threadId,
            assistant_id=self.assistantId
        )
        
        # Pulling the run status until it is completed to get the response
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=self.threadId,
                run_id=run.id
            )
            if run_status.status == "completed":
                break
            elif run_status.status == "requires_action":
                self.handle_required_action(run, run_status)
                break
            time.sleep(1)

        messages = openai.beta.threads.messages.list(thread_id = self.threadId)
        
        # Get the last message which is from the assistant
        return messages.data[0].content[0].text.value
    
    

    def get_initial_message(self):
        """
        Retorna a mensagem inicial do assistente
        """

        messagePrompt = file_to_string("prompts/gpt_initial_messagem.txt")

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": messagePrompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        return response.choices[0].message.content