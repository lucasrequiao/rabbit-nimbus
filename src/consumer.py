"""
Consumer RabbitMQ - Nimbus Planejamento
Consome mensagens da fila e envia para API externa
"""
import pika
import logging
import time
import requests
from .config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD, RABBITMQ_VHOST, RABBITMQ_QUEUE, RECONNECT_DELAY
from .metricas import Metricas
from .api_client import enviar_para_api

# Sistema de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('consumer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

metricas = Metricas()

def callback(ch, method, properties, body):
    """
    Callback executado quando uma mensagem chega na fila
    Processa a mensagem e envia para API externa
    Confirma a mensagem após processamento
    Trata erros e reprocessa mensagens
    """
    try:
        metricas.registrar_recebida()

        logger.info("=" * 50)
        logger.info("Nova mensagem recebida!")

        mensagem = body.decode('utf-8')
        logger.info(f"Mensagem: {mensagem}")

        enviar_para_api(mensagem)
        metricas.registrar_sucesso()

        if metricas.mensagens_recebidas % 10 == 0:
            metricas.exibir_resumo()

        ch.basic_ack(delivery_tag=method.delivery_tag)
        logger.info("=" * 50)

    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao enviar mensagem para API: {e}")
        metricas.registrar_erro()
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except UnicodeDecodeError as e:
        logger.error(f"Erro ao decodificar mensagem: {e}")
        logger.error(f"Mensagem bruta: {body}")
        metricas.registrar_erro()
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {e}")
        logger.error(f"Mensagem que causou o erro: {body}")
        metricas.registrar_erro()
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    """
    Função principal do consumer
    Gerencia conexão e reconexão com RabbitMQ
    """
    logger.info(f"Configurações carregadas - Host: {RABBITMQ_HOST}, VHost: {RABBITMQ_VHOST}, Porta: {RABBITMQ_PORT}, Fila: {RABBITMQ_QUEUE}")
    tentativas = 0
    while True:
        try:
            tentativas += 1
            logger.info(f"Tentativa de conexão #{tentativas}")

            # Credenciais do RabbitMQ
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            parameters = pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials,
                virtual_host=RABBITMQ_VHOST,
            )
            logger.info(f"Tentando conectar no RabbitMQ...")
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()
            logger.info(f"✓ Conectado com sucesso!")
            logger.info(f"✓ Fila '{RABBITMQ_QUEUE}' pronta para consumir")

            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=False)
            logger.info("Aguardando mensagens... (Ctrl+C para sair)")
            channel.start_consuming()
            
        except KeyboardInterrupt:
            logger.info("Interrompido pelo usuário. Encerrando...")
            metricas.exibir_resumo()
            break
        except Exception as e:
            metricas.registrar_reconexao()
            logger.error(f"Erro de conexão: {e}")
            logger.info(f"Tentando reconectar em {RECONNECT_DELAY} segundos... (Tentativa #{tentativas})")
            time.sleep(RECONNECT_DELAY)
        finally:
            try:
                if 'connection' in locals() and connection.is_open:
                    connection.close()
                    logger.info("Conexão fechada")
            except:
                pass     

if __name__ == "__main__":
    main()