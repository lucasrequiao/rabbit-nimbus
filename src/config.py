import os 
from dotenv import load_dotenv

load_dotenv()

# Variáveis de ambiente
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT'))
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_VHOST = os.getenv('RABBITMQ_VHOST')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE')

# Configurações da API externa
API_URL = os.getenv('API_URL')
API_TOKEN = os.getenv('API_TOKEN')

# Configurações da aplicação
RECONNECT_DELAY = 5  
MAX_RETRY_ATTEMPTS = 5  