import logging
import openai
import time
import os 

from src.QrcodeService import QrCodeService
from src.CommonHelper import file_to_string
from src.CalendarHandler import CalendarHandler
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# Carrega o .env em um caminho específico
load_dotenv(dotenv_path="env/.env")

class AssistantHandler:
    def __init__(self):
        openai.api_key = os.getenv('OPENAI_API_KEY')
        self.assistantId : str = os.getenv('OPENAI_ASSISTANT_ID')
        thread = openai.beta.threads.create()
        self.threadId = thread.id
        self.qrcode_service = QrCodeService()

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
        
        qrcode_url = None
        
        # Pulling the run status until it is completed to get the response
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=self.threadId,
                run_id=run.id
            )
            logging.info(f"Assitant status: '{run_status.status}'")
            if run_status.status == "completed":
                break
            elif run_status.status == "requires_action":
                qrcode_url = self.handle_required_action(run, run_status)
                break
            time.sleep(1)

        messages = openai.beta.threads.messages.list(thread_id = self.threadId)
        
        # Get the last message which is from the assistant
        
        return {
            'message': messages.data[0].content[0].text.value,
            'qrcode_url': qrcode_url
            }

    def handle_required_action(self, run, run_status):
        tool_call = run_status.required_action.submit_tool_outputs.tool_calls[0]
        model_dump = run_status.required_action.submit_tool_outputs.model_dump()

        calendar_handler = CalendarHandler()    
        
        if tool_call.function.name == "visit_scheduler":
            
            response = calendar_handler.schedule_visit(model_dump)
            
            self.retrieving_action(run.id, response['response'], tool_call.id)
            
            agenda_url = f"{os.getenv('RENDER_WEBSERVICE_URL')}/confirm_agenda_attendance?agenda_id={response['agenda']['id']}"
            qrcode_url = self.qrcode_service.qr_code_generator(agenda_url)['url']
            
            logging.info(f"QR Code URL created: {qrcode_url}")
            
            return qrcode_url

    def retrieving_action(self, runId, response, tool_call_id):
        """
        Processa a resposta do assistente e executa ações específicas
        """
        openai.beta.threads.runs.submit_tool_outputs(
            thread_id=self.threadId,
            run_id=runId,
            tool_outputs=[
                    {
                    "tool_call_id": tool_call_id,
                    "output": response
                    }
                ],
                stream=True
            )
    
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=self.threadId,
                run_id=runId
            )
            if run_status.status == "completed":
                print("Ação concluída com sucesso!")
                break

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