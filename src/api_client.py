"""
Cliente para comunicação com API externa (n8n webhook)
Inclui retry automático com Tenacity
"""
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
import logging
from .config import API_URL, API_TOKEN, MAX_RETRY_ATTEMPTS
import json

logger = logging.getLogger(__name__)

@retry(
    stop=stop_after_attempt(MAX_RETRY_ATTEMPTS),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(Exception)
)

def enviar_para_api(mensagem):
    """
    Envia a mensagem para a API externa
    """
    try:
        logger.info(f"Tentando enviar mensagem para API n8n...")

        if not API_URL:
            raise ValueError("API_URL não configurada no .env")
        if not API_TOKEN:
            raise ValueError("API_TOKEN não configurada no .env")

        headers = {
            'X-API-Key': API_TOKEN,
            'Content-Type': 'application/json',
        }

        response = requests.post(
            API_URL, 
            data=mensagem,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        logger.info(f"✓ Mensagem enviada com sucesso para n8n! Status: {response.status_code}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro na requisição HTTP: {e}")
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao enviar para API: {e}")
        raise
    
    return response