import os

from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Carrega o .env em um caminho específico
load_dotenv(dotenv_path="env/.env")

engine = create_engine(os.getenv('CONNECTION_STRING'))
connection = engine.connect()
result = connection.execute(text("SELECT version();"))
print(result.fetchone())
connection.close()
