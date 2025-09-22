import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import schedule
import time
from threading import Thread

from ..scrapers.cespe_scraper import CESPEscraper
from ..scrapers.fgv_scraper import FGVScraper
from ..models.edital import Concurso, Edital, ScrapingLog, ConfiguracaoScraping
from ..database import get_db

logger = logging.getLogger(__name__)

class ScrapingOrchestrator:
    """
    Orquestrador que coordena todos os scrapers de editais
    """
    
    def __init__(self):
        self.scrapers = {
            'CESPE': CESPEscraper(),
            'FGV': FGVScraper(),
            # Adicionar outros scrapers aqui
        }
        self.db = next(get_db())
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.running = False
        
    def iniciar_scraping_automatico(self):
        """
        Inicia o scraping automático em background
        """
        if self.running:
            logger.warning("Scraping automático já está rodando")
            return
        
        self.running = True
        
        # Configurar agendamento
        schedule.every(1).hours.do(self.executar_scraping_completo)
        schedule.every(30).minutes.do(self.verificar_novos_concursos)
        
        # Iniciar thread de agendamento
        scheduler_thread = Thread(target=self._executar_scheduler, daemon=True)
        scheduler_thread.start()
        
        logger.info("Scraping automático iniciado")
    
    def _executar_scheduler(self):
        """Executa o scheduler em loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Verificar a cada minuto
    
    def parar_scraping_automatico(self):
        """Para o scraping automático"""
        self.running = False
        logger.info("Scraping automático parado")
    
    async def executar_scraping_completo(self) -> Dict[str, List[Dict]]:
        """
        Executa scraping completo de todas as fontes
        """
        logger.info("Iniciando scraping completo")
        resultados = {}
        
        # Executar scrapers em paralelo
        futures = []
        for nome, scraper in self.scrapers.items():
            future = self.executor.submit(self._executar_scraper, nome, scraper)
            futures.append(future)
        
        # Coletar resultados
        for future in as_completed(futures):
            try:
                nome, concursos = future.result()
                resultados[nome] = concursos
                logger.info(f"Scraper {nome} encontrou {len(concursos)} concursos")
            except Exception as e:
                logger.error(f"Erro no scraper: {e}")
        
        # Salvar resultados no banco
        await self._salvar_resultados(resultados)
        
        logger.info("Scraping completo finalizado")
        return resultados
    
    def _executar_scraper(self, nome: str, scraper) -> tuple:
        """
        Executa um scraper específico
        """
        try:
            inicio = datetime.now()
            
            # Buscar concursos
            concursos = scraper.buscar_concursos_ativos()
            
            # Log da execução
            tempo_execucao = (datetime.now() - inicio).total_seconds()
            self._log_scraping(nome, len(concursos), tempo_execucao, "sucesso")
            
            return nome, concursos
            
        except Exception as e:
            logger.error(f"Erro no scraper {nome}: {e}")
            self._log_scraping(nome, 0, 0, "erro", str(e))
            return nome, []
    
    def _log_scraping(self, fonte: str, concursos_encontrados: int, 
                     tempo_execucao: float, status: str, erro: str = None):
        """
        Registra log de scraping
        """
        try:
            log = ScrapingLog(
                fonte=fonte,
                url=self.scrapers[fonte].base_url if fonte in self.scrapers else "",
                status=status,
                conteudo_encontrado={"concursos": concursos_encontrados},
                erro_detalhes=erro,
                tempo_execucao=int(tempo_execucao)
            )
            
            self.db.add(log)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Erro ao salvar log de scraping: {e}")
    
    async def verificar_novos_concursos(self) -> Dict[str, List[Dict]]:
        """
        Verifica apenas novos concursos desde a última verificação
        """
        logger.info("Verificando novos concursos")
        novos_concursos = {}
        
        for nome, scraper in self.scrapers.items():
            try:
                # Buscar última verificação
                ultima_verificacao = self._obter_ultima_verificacao(nome)
                
                # Verificar novos concursos
                novos = scraper.verificar_novos_concursos(ultima_verificacao)
                
                if novos:
                    novos_concursos[nome] = novos
                    logger.info(f"Encontrados {len(novos)} novos concursos em {nome}")
                    
                    # Notificar sobre novos concursos
                    await self._notificar_novos_concursos(nome, novos)
                
            except Exception as e:
                logger.error(f"Erro ao verificar novos concursos em {nome}: {e}")
        
        return novos_concursos
    
    def _obter_ultima_verificacao(self, fonte: str) -> datetime:
        """
        Obtém a data da última verificação para uma fonte
        """
        try:
            config = self.db.query(ConfiguracaoScraping).filter(
                ConfiguracaoScraping.fonte == fonte
            ).first()
            
            if config and config.ultima_busca:
                return config.ultima_busca
            else:
                # Se não há registro, retornar data de 24 horas atrás
                return datetime.now() - timedelta(hours=24)
                
        except Exception as e:
            logger.error(f"Erro ao obter última verificação: {e}")
            return datetime.now() - timedelta(hours=24)
    
    async def _notificar_novos_concursos(self, fonte: str, concursos: List[Dict]):
        """
        Notifica sobre novos concursos encontrados
        """
        try:
            # Aqui seria implementada a lógica de notificação
            # Por exemplo: email, push notification, webhook, etc.
            
            for concurso in concursos:
                logger.info(f"Novo concurso encontrado em {fonte}: {concurso['titulo']}")
                
                # TODO: Implementar notificações
                # - Enviar email para usuários interessados
                # - Push notification
                # - Webhook para sistemas externos
                
        except Exception as e:
            logger.error(f"Erro ao notificar novos concursos: {e}")
    
    async def _salvar_resultados(self, resultados: Dict[str, List[Dict]]):
        """
        Salva os resultados do scraping no banco de dados
        """
        try:
            for fonte, concursos in resultados.items():
                for concurso_data in concursos:
                    await self._salvar_concurso(concurso_data)
            
            self.db.commit()
            logger.info("Resultados salvos no banco de dados")
            
        except Exception as e:
            logger.error(f"Erro ao salvar resultados: {e}")
            self.db.rollback()
    
    async def _salvar_concurso(self, concurso_data: Dict):
        """
        Salva um concurso no banco de dados
        """
        try:
            # Verificar se o concurso já existe
            concurso_existente = self.db.query(Concurso).filter(
                Concurso.url_edital == concurso_data.get('link')
            ).first()
            
            if concurso_existente:
                # Atualizar dados existentes
                concurso_existente.updated_at = datetime.now()
                return
            
            # Criar novo concurso
            concurso = Concurso(
                nome=concurso_data.get('titulo', ''),
                orgao=concurso_data.get('informacoes', {}).get('orgao', ''),
                banca_organizadora=concurso_data.get('fonte', ''),
                url_edital=concurso_data.get('link', ''),
                status=concurso_data.get('status', 'ativo')
            )
            
            self.db.add(concurso)
            
        except Exception as e:
            logger.error(f"Erro ao salvar concurso: {e}")
    
    def obter_estatisticas_scraping(self) -> Dict:
        """
        Obtém estatísticas do scraping
        """
        try:
            # Estatísticas dos últimos 7 dias
            data_inicio = datetime.now() - timedelta(days=7)
            
            logs = self.db.query(ScrapingLog).filter(
                ScrapingLog.created_at >= data_inicio
            ).all()
            
            estatisticas = {
                'total_execucoes': len(logs),
                'sucessos': len([l for l in logs if l.status == 'sucesso']),
                'erros': len([l for l in logs if l.status == 'erro']),
                'concursos_encontrados': sum(
                    l.conteudo_encontrado.get('concursos', 0) for l in logs 
                    if l.conteudo_encontrado
                ),
                'tempo_medio_execucao': sum(l.tempo_execucao for l in logs) / len(logs) if logs else 0,
                'fontes_ativas': list(self.scrapers.keys())
            }
            
            return estatisticas
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def configurar_scraper(self, fonte: str, config: Dict):
        """
        Configura um scraper específico
        """
        try:
            config_existente = self.db.query(ConfiguracaoScraping).filter(
                ConfiguracaoScraping.fonte == fonte
            ).first()
            
            if config_existente:
                # Atualizar configuração existente
                for key, value in config.items():
                    setattr(config_existente, key, value)
                config_existente.updated_at = datetime.now()
            else:
                # Criar nova configuração
                nova_config = ConfiguracaoScraping(
                    fonte=fonte,
                    **config
                )
                self.db.add(nova_config)
            
            self.db.commit()
            logger.info(f"Configuração do scraper {fonte} atualizada")
            
        except Exception as e:
            logger.error(f"Erro ao configurar scraper {fonte}: {e}")
            self.db.rollback()

# Instância global do orquestrador
orchestrator = ScrapingOrchestrator()
