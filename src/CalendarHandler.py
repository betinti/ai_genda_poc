import logging
import pytz
import os


from datetime import datetime, timedelta
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

# Carrega o .env em um caminho específico
load_dotenv(dotenv_path="env/.env")

class CalendarHandler:
    def __init__(self):
        secret_path = os.getenv('GOOGLE_SECRETS_PATH')
        self.service_account_file = f'{secret_path}service-account-key.json'
        self.service = None
        self.scopes = [os.getenv('GOOGLE_CALENDAR_SCOPE')]
        self.max_simultaneous_agendas = 5  # Limite de agendamentos simultâneos
        self._authenticate()
    
    def _authenticate(self):
        """Autentica usando Service Account"""
        try:
            from google.oauth2 import service_account
            
            if not os.path.exists(self.service_account_file):
                raise FileNotFoundError(f"Service account file não encontrado: {self.service_account_file}")
            
            # Carrega credenciais da service account
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file, scopes=self.scopes)
            
            # Inicializa serviços
            self.service = build('calendar', 'v3', credentials=credentials)
            
            logging.info("Service Account autenticada com sucesso")
            
        except Exception as e:
            logging.error(f"Erro na autenticação com Service Account: {e}")
            raise

    
    def schedule_visit(self, gptCall):
        """Para exemple: {'tool_calls': [{'id': 'call_Fp1BAtsH06fPEKkeHmuxFd18', 'function': {'arguments': '{"day": 10, "month": 10, "hour": 12}', 'name': 'visit_scheduler'}, 'type': 'function'}]}"""
        params = gptCall['tool_calls'][0]['function']['arguments']
        params = eval(params)  # Converte a string para dicionário

        day = params['day']
        month = params['month']
        hour = params['hour']
        
        # Define a data e hora de início e fim
        agenda = datetime.now().replace(hour=hour, day=day, month=month, minute=0, second=0, microsecond=0)
        agenda_end = agenda + timedelta(hours=0.5)  # Duração de 30 minutos
        
        agendas = self.check_agenda(agenda, agenda_end)

        if len(agendas) < self.max_simultaneous_agendas:
            # Criar nova agenda
            response = self.criar_agenda(
                title="Visita técnica agendada",
                date_begin=agenda,
                date_end=agenda_end,
                description="Visita técnica agendada pelo assistente virtual",
                local="Sua concessionária BYD"
                )

            body = {
                "response": "Responda que a visita foi agendada com sucesso no horário informado!. Pergunte se o usuário precisa de mais alguma coisa ou se deseja encerrar a conversa.",
                "agenda": response
            }
            return body
        else :
            return "Responda que o horário está indisponível, peça com educação para que o usuário escolha outro horário de sua prefência."

    def get_all_agendas(self, calendar_id='primary'):
        """
        Retorna todas as agendas do calendário
        
        Args:
            calendar_id (str): ID do calendário (padrão: 'primary')
        
        Returns:
            list: Lista de eventos encontrados com informações básicas
        """
        try:
            # Busca todos os eventos
            events_result = self.service.events().list(
                calendarId=calendar_id,
                singleEvents=True,
                orderBy='startTime',
                maxResults=100  # Limite para evitar problemas
            ).execute()
            
            events = events_result.get('items', [])
            
            if len(events) == 0:
                return []
            
            # Formata os eventos para retorno
            agendas = []
            for event in events:
                start_datetime = event['start'].get('dateTime')
                start_date = event['start'].get('date')
                end_datetime = event['end'].get('dateTime')
                end_date = event['end'].get('date')
                
                start = start_datetime if start_datetime else start_date
                end = end_datetime if end_datetime else end_date
                
                agenda = {
                    'id': event['id'],
                    'titulo': event.get('summary', 'Sem título'),
                    'descricao': event.get('description', ''),
                    'inicio': start,
                    'fim': end,
                    'local': event.get('location', ''),
                    'criador': event.get('creator', {}).get('email', ''),
                    'status': event.get('status', ''),
                    'tipo_evento': 'dia_inteiro' if start_date else 'horario_especifico'
                }
                agendas.append(agenda)
            
            return agendas
            
        except Exception as error:
            print(f"Erro ao consultar agendas: {error}")
            print(f"Tipo do erro: {type(error).__name__}")
            return []    
        
    def check_agenda(self, date_begin, date_end=None, calendar_id='primary'):
        """
        Consulta agendas em uma data e horário específico
        
        Args:
            data_inicio (datetime): Data e hora de início da consulta
            data_fim (datetime, optional): Data e hora de fim da consulta. 
                                        Se não informado, usa data_inicio + 1 dia
            calendar_id (str): ID do calendário (padrão: 'primary')
        
        Returns:
            list: Lista de eventos encontrados com informações básicas
        """
        try:
            # Se não informou data_fim, consulta o dia inteiro
            if date_end is None:
                date_end = date_begin.replace(hour=23, minute=59, second=59)
            
            # Garante que as datas tenham timezone (UTC se não especificado)
            if date_begin.tzinfo is None:
                # Assume timezone do Brasil (UTC-3)
                brasilia_tz = pytz.timezone('America/Sao_Paulo')
                date_begin = brasilia_tz.localize(date_begin)
            
            if date_end.tzinfo is None:
                brasilia_tz = pytz.timezone('America/Sao_Paulo')
                date_end = brasilia_tz.localize(date_end)
            
            # Converte para formato ISO (remove o 'Z' pois já temos timezone)
            time_min = date_begin.isoformat()
            time_max = date_end.isoformat()
            
            # Busca eventos no período
            events_result = self.service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime',
                maxResults=self.max_simultaneous_agendas  # Adiciona limite para evitar problemas
            ).execute()
            
            events = events_result.get('items', [])
            
            if len(events) == 0:
                return []
            
            # Formata os eventos para retorno
            agendas = []
            for event in events:
                # Melhor tratamento das datas
                start_datetime = event['start'].get('dateTime')
                start_date = event['start'].get('date')
                end_datetime = event['end'].get('dateTime')
                end_date = event['end'].get('date')
                
                # Usa dateTime se disponível, senão usa date
                start = start_datetime if start_datetime else start_date
                end = end_datetime if end_datetime else end_date
                
                agenda = {
                    'id': event['id'],
                    'titulo': event.get('summary', 'Sem título'),
                    'descricao': event.get('description', ''),
                    'inicio': start,
                    'fim': end,
                    'local': event.get('location', ''),
                    'criador': event.get('creator', {}).get('email', ''),
                    'status': event.get('status', ''),
                    'tipo_evento': 'dia_inteiro' if start_date else 'horario_especifico'
                }
                agendas.append(agenda)
            
            return agendas
            
        except Exception as error:
            print(f"Erro ao consultar agendas: {error}")
            print(f"Tipo do erro: {type(error).__name__}")
            return []
    
    def criar_agenda(self, title, date_begin, date_end, description="", 
                    local="", calendar_id='primary'):
        """
        Cria uma nova agenda em data e horário específico
        
        Args:
            titulo (str): Título do evento
            data_inicio (datetime): Data e hora de início
            data_fim (datetime): Data e hora de fim
            descricao (str, optional): Descrição do evento
            local (str, optional): Local do evento
            calendar_id (str): ID do calendário (padrão: 'primary')
        
        Returns:
            dict: Dados do evento criado ou None se houve erro
        """
        try:
            # Garante que as datas tenham timezone (UTC se não especificado)
            if date_begin.tzinfo is None:
                # Assume timezone do Brasil (UTC-3)
                brasilia_tz = pytz.timezone('America/Sao_Paulo')
                date_begin = brasilia_tz.localize(date_begin)
            
            if date_end.tzinfo is None:
                brasilia_tz = pytz.timezone('America/Sao_Paulo')
                date_end = brasilia_tz.localize(date_end)
            
            # Monta o evento
            event = {
                'summary': title,
                'location': local,
                'description': description,
                'start': {
                    'dateTime': date_begin.isoformat(),
                    'timeZone': 'America/Sao_Paulo',
                },
                'end': {
                    'dateTime': date_end.isoformat(),
                    'timeZone': 'America/Sao_Paulo',
                },
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'popup', 'minutes': 10},  # Lembrete 10 min antes
                    ],
                },
            }
            
            # Cria o evento
            event_created = self.service.events().insert(
                calendarId=calendar_id, 
                body=event
            ).execute()
            
            # Formata resposta
            agenda_created = {
                'id': event_created['id'],
                'titulo': event_created['summary'],
                'inicio': event_created['start']['dateTime'],
                'fim': event_created['end']['dateTime'],
                'link': event_created.get('htmlLink', ''),
                'status': 'criado'
            }
            
            return agenda_created
            
        except HttpError as error:
            print(f"Erro ao criar agenda: {error}")
            return None
        
        except Exception as error:
            print(f"Erro ao criar agendas: {error}")
            print(f"Tipo do erro: {type(error).__name__}")
            return None
