"""
Sistema de métricas para monitoramento do consumer
"""
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Metricas:
    """
    Classe para rastrear métricas do consumer
    """
    def __init__(self):
        self.mensagens_recebidas = 0
        self.mensagens_sucesso = 0
        self.mensagens_erro = 0
        self.reconexoes = 0
        self.inicio_execucao = datetime.now()
        self.ultima_mensagem = None

    def registrar_recebida(self):
        """Incrementa contador de mensagens recebidas"""
        self.mensagens_recebidas += 1
        self.ultima_mensagem = datetime.now()

    def registrar_sucesso(self):
        """Incrementa contador de sucessos"""
        self.mensagens_sucesso += 1

    def registrar_erro(self):
        """Incrementa contador de erros"""
        self.mensagens_erro += 1

    def registrar_reconexao(self):
        """Incrementa contador de reconexões"""
        self.reconexoes += 1

    def obter_resumo(self):
        """Retorna um resumo das métricas"""
        tempo_execucao = datetime.now() - self.inicio_execucao
        return {
            'tempo_execucao': str(tempo_execucao),
            'mensagens_recebidas': self.mensagens_recebidas,
            'mensagens_sucesso': self.mensagens_sucesso,
            'mensagens_erro': self.mensagens_erro,
            'reconexoes': self.reconexoes,
            'taxa_sucesso': f"{(self.mensagens_sucesso / self.mensagens_recebidas * 100):.1f}%" if self.mensagens_recebidas > 0 else "0%",
            'ultima_mensagem': self.ultima_mensagem.strftime('%Y-%m-%d %H:%M:%S') if self.ultima_mensagem else "Nenhuma"
        }

    def exibir_resumo(self):
        """Exibe resumo formatado no log"""
        resumo = self.obter_resumo()
        logger.info("=" * 60)
        logger.info("RESUMO DE MÉTRICAS")
        logger.info("=" * 60)
        logger.info(f"Tempo de execução: {resumo['tempo_execucao']}")
        logger.info(f"Mensagens recebidas: {resumo['mensagens_recebidas']}")
        logger.info(f"Mensagens com sucesso: {resumo['mensagens_sucesso']}")
        logger.info(f"Mensagens com erro: {resumo['mensagens_erro']}")
        logger.info(f"Taxa de sucesso: {resumo['taxa_sucesso']}")
        logger.info(f"Reconexões: {resumo['reconexoes']}")
        logger.info(f"Última mensagem: {resumo['ultima_mensagem']}")
        logger.info("=" * 60)