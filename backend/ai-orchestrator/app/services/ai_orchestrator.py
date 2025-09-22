import asyncio
import logging
from typing import List, Dict, Optional, Any
from datetime import datetime, timedelta
import json
import httpx
from celery import Celery
from celery.result import AsyncResult
import redis
from pydantic import BaseModel
import uuid

logger = logging.getLogger(__name__)

# Configuração do Celery
celery_app = Celery('ai_orchestrator')
celery_app.config_from_object({
    'broker_url': 'redis://localhost:6379/0',
    'result_backend': 'redis://localhost:6379/0',
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'UTC',
    'enable_utc': True,
})

# Configuração do Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

class AIServiceConfig(BaseModel):
    """Configuração de um serviço de IA"""
    name: str
    url: str
    port: int
    health_endpoint: str
    status: str = "unknown"
    last_health_check: Optional[datetime] = None
    response_time: Optional[float] = None
    error_count: int = 0
    success_count: int = 0

class TaskResult(BaseModel):
    """Resultado de uma tarefa"""
    task_id: str
    service: str
    status: str
    result: Optional[Dict] = None
    error: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    duration: Optional[float] = None

class AIOrchestrator:
    """
    Orquestrador principal que coordena todos os serviços de IA
    """
    
    def __init__(self):
        self.services = {
            'edital_scraper': AIServiceConfig(
                name='edital_scraper',
                url='http://localhost',
                port=8001,
                health_endpoint='/health'
            ),
            'edital_analyzer': AIServiceConfig(
                name='edital_analyzer',
                url='http://localhost',
                port=8002,
                health_endpoint='/health'
            ),
            'prova_scraper': AIServiceConfig(
                name='prova_scraper',
                url='http://localhost',
                port=8003,
                health_endpoint='/health'
            ),
            'proficiency_test': AIServiceConfig(
                name='proficiency_test',
                url='http://localhost',
                port=8004,
                health_endpoint='/health'
            ),
            'weakness_analyzer': AIServiceConfig(
                name='weakness_analyzer',
                url='http://localhost',
                port=8005,
                health_endpoint='/health'
            ),
            'study_plan_generator': AIServiceConfig(
                name='study_plan_generator',
                url='http://localhost',
                port=8006,
                health_endpoint='/health'
            ),
            'question_predictor': AIServiceConfig(
                name='question_predictor',
                url='http://localhost',
                port=8007,
                health_endpoint='/health'
            )
        }
        
        self.active_tasks = {}
        self.task_history = []
        self.pipeline_configs = {}
        self.monitoring_enabled = True
        
    async def iniciar_orquestracao(self):
        """
        Inicia o sistema de orquestração
        """
        try:
            logger.info("Iniciando sistema de orquestração de IA")
            
            # Iniciar monitoramento de saúde
            asyncio.create_task(self._monitorar_saude_servicos())
            
            # Iniciar limpeza de tarefas antigas
            asyncio.create_task(self._limpar_tarefas_antigas())
            
            # Carregar configurações de pipeline
            await self._carregar_configuracoes_pipeline()
            
            logger.info("Sistema de orquestração iniciado com sucesso")
            
        except Exception as e:
            logger.error(f"Erro ao iniciar orquestração: {e}")
    
    async def _monitorar_saude_servicos(self):
        """
        Monitora a saúde de todos os serviços
        """
        while self.monitoring_enabled:
            try:
                for service_name, config in self.services.items():
                    await self._verificar_saude_servico(service_name, config)
                
                await asyncio.sleep(30)  # Verificar a cada 30 segundos
                
            except Exception as e:
                logger.error(f"Erro no monitoramento de saúde: {e}")
                await asyncio.sleep(60)
    
    async def _verificar_saude_servico(self, service_name: str, config: AIServiceConfig):
        """
        Verifica a saúde de um serviço específico
        """
        try:
            start_time = datetime.now()
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{config.url}:{config.port}{config.health_endpoint}"
                )
                
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                
                if response.status_code == 200:
                    config.status = "healthy"
                    config.success_count += 1
                    config.response_time = response_time
                else:
                    config.status = "unhealthy"
                    config.error_count += 1
                
                config.last_health_check = end_time
                
        except Exception as e:
            config.status = "unhealthy"
            config.error_count += 1
            config.last_health_check = datetime.now()
            logger.warning(f"Serviço {service_name} não está respondendo: {e}")
    
    async def _limpar_tarefas_antigas(self):
        """
        Limpa tarefas antigas do histórico
        """
        while self.monitoring_enabled:
            try:
                # Manter apenas as últimas 1000 tarefas
                if len(self.task_history) > 1000:
                    self.task_history = self.task_history[-1000:]
                
                # Limpar tarefas ativas antigas (mais de 1 hora)
                cutoff_time = datetime.now() - timedelta(hours=1)
                tasks_to_remove = []
                
                for task_id, task in self.active_tasks.items():
                    if task.start_time < cutoff_time:
                        tasks_to_remove.append(task_id)
                
                for task_id in tasks_to_remove:
                    del self.active_tasks[task_id]
                
                await asyncio.sleep(300)  # Limpar a cada 5 minutos
                
            except Exception as e:
                logger.error(f"Erro na limpeza de tarefas: {e}")
                await asyncio.sleep(300)
    
    async def _carregar_configuracoes_pipeline(self):
        """
        Carrega configurações de pipeline do Redis
        """
        try:
            # Configurações padrão de pipeline
            default_pipelines = {
                'analise_completa_usuario': {
                    'steps': [
                        {'service': 'weakness_analyzer', 'endpoint': '/analyze', 'async': True},
                        {'service': 'study_plan_generator', 'endpoint': '/generate', 'depends_on': ['weakness_analyzer']},
                        {'service': 'question_predictor', 'endpoint': '/predict', 'depends_on': ['weakness_analyzer']}
                    ],
                    'timeout': 300
                },
                'processamento_edital': {
                    'steps': [
                        {'service': 'edital_scraper', 'endpoint': '/scrape', 'async': True},
                        {'service': 'edital_analyzer', 'endpoint': '/analyze', 'depends_on': ['edital_scraper']}
                    ],
                    'timeout': 180
                },
                'coleta_provas': {
                    'steps': [
                        {'service': 'prova_scraper', 'endpoint': '/scrape', 'async': True},
                        {'service': 'proficiency_test', 'endpoint': '/update_bank', 'depends_on': ['prova_scraper']}
                    ],
                    'timeout': 240
                }
            }
            
            for pipeline_name, config in default_pipelines.items():
                await self._salvar_configuracao_pipeline(pipeline_name, config)
            
            logger.info("Configurações de pipeline carregadas")
            
        except Exception as e:
            logger.error(f"Erro ao carregar configurações de pipeline: {e}")
    
    async def _salvar_configuracao_pipeline(self, pipeline_name: str, config: Dict):
        """
        Salva configuração de pipeline no Redis
        """
        try:
            key = f"pipeline_config:{pipeline_name}"
            redis_client.setex(key, 3600, json.dumps(config))  # Expira em 1 hora
        except Exception as e:
            logger.error(f"Erro ao salvar configuração de pipeline: {e}")
    
    async def executar_pipeline(self, pipeline_name: str, dados: Dict) -> str:
        """
        Executa um pipeline de serviços
        """
        try:
            task_id = str(uuid.uuid4())
            
            # Carregar configuração do pipeline
            config = await self._carregar_configuracao_pipeline(pipeline_name)
            if not config:
                raise ValueError(f"Pipeline {pipeline_name} não encontrado")
            
            # Criar tarefa
            task = TaskResult(
                task_id=task_id,
                service=pipeline_name,
                status="started",
                start_time=datetime.now()
            )
            
            self.active_tasks[task_id] = task
            
            # Executar pipeline em background
            asyncio.create_task(self._executar_pipeline_async(task_id, config, dados))
            
            return task_id
            
        except Exception as e:
            logger.error(f"Erro ao executar pipeline: {e}")
            raise
    
    async def _executar_pipeline_async(self, task_id: str, config: Dict, dados: Dict):
        """
        Executa pipeline de forma assíncrona
        """
        try:
            task = self.active_tasks[task_id]
            steps = config.get('steps', [])
            timeout = config.get('timeout', 300)
            
            # Executar steps em sequência
            resultados = {}
            for step in steps:
                step_result = await self._executar_step(step, dados, resultados)
                resultados[step['service']] = step_result
                
                # Verificar timeout
                if (datetime.now() - task.start_time).total_seconds() > timeout:
                    raise TimeoutError("Pipeline excedeu o tempo limite")
            
            # Finalizar tarefa
            task.status = "completed"
            task.end_time = datetime.now()
            task.duration = (task.end_time - task.start_time).total_seconds()
            task.result = resultados
            
            # Mover para histórico
            self.task_history.append(task)
            del self.active_tasks[task_id]
            
            logger.info(f"Pipeline {task_id} executado com sucesso")
            
        except Exception as e:
            task = self.active_tasks.get(task_id)
            if task:
                task.status = "failed"
                task.end_time = datetime.now()
                task.duration = (task.end_time - task.start_time).total_seconds()
                task.error = str(e)
                
                # Mover para histórico
                self.task_history.append(task)
                del self.active_tasks[task_id]
            
            logger.error(f"Erro na execução do pipeline {task_id}: {e}")
    
    async def _executar_step(self, step: Dict, dados: Dict, resultados: Dict) -> Dict:
        """
        Executa um step do pipeline
        """
        try:
            service_name = step['service']
            endpoint = step['endpoint']
            depends_on = step.get('depends_on', [])
            is_async = step.get('async', False)
            
            # Verificar dependências
            for dep in depends_on:
                if dep not in resultados:
                    raise ValueError(f"Dependência {dep} não foi executada")
            
            # Preparar dados para o serviço
            service_data = self._preparar_dados_servico(dados, resultados, depends_on)
            
            # Executar chamada para o serviço
            if is_async:
                # Executar de forma assíncrona
                result = await self._chamar_servico_async(service_name, endpoint, service_data)
            else:
                # Executar de forma síncrona
                result = await self._chamar_servico_sync(service_name, endpoint, service_data)
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na execução do step: {e}")
            raise
    
    def _preparar_dados_servico(self, dados_originais: Dict, resultados: Dict, depends_on: List[str]) -> Dict:
        """
        Prepara dados para um serviço específico
        """
        try:
            service_data = dados_originais.copy()
            
            # Adicionar resultados das dependências
            for dep in depends_on:
                if dep in resultados:
                    service_data[f"{dep}_result"] = resultados[dep]
            
            return service_data
            
        except Exception as e:
            logger.error(f"Erro na preparação de dados: {e}")
            return dados_originais
    
    async def _chamar_servico_async(self, service_name: str, endpoint: str, dados: Dict) -> Dict:
        """
        Chama um serviço de forma assíncrona
        """
        try:
            config = self.services.get(service_name)
            if not config:
                raise ValueError(f"Serviço {service_name} não encontrado")
            
            if config.status != "healthy":
                raise ValueError(f"Serviço {service_name} não está saudável")
            
            # Executar tarefa assíncrona
            task = celery_app.send_task(
                'chamar_servico',
                args=[service_name, endpoint, dados],
                queue=f'service_{service_name}'
            )
            
            # Aguardar resultado
            result = task.get(timeout=300)
            
            return result
            
        except Exception as e:
            logger.error(f"Erro na chamada assíncrona do serviço {service_name}: {e}")
            raise
    
    async def _chamar_servico_sync(self, service_name: str, endpoint: str, dados: Dict) -> Dict:
        """
        Chama um serviço de forma síncrona
        """
        try:
            config = self.services.get(service_name)
            if not config:
                raise ValueError(f"Serviço {service_name} não encontrado")
            
            if config.status != "healthy":
                raise ValueError(f"Serviço {service_name} não está saudável")
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{config.url}:{config.port}{endpoint}",
                    json=dados
                )
                
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            logger.error(f"Erro na chamada síncrona do serviço {service_name}: {e}")
            raise
    
    async def _carregar_configuracao_pipeline(self, pipeline_name: str) -> Optional[Dict]:
        """
        Carrega configuração de pipeline do Redis
        """
        try:
            key = f"pipeline_config:{pipeline_name}"
            config_json = redis_client.get(key)
            
            if config_json:
                return json.loads(config_json)
            
            return None
            
        except Exception as e:
            logger.error(f"Erro ao carregar configuração de pipeline: {e}")
            return None
    
    def obter_status_tarefa(self, task_id: str) -> Optional[TaskResult]:
        """
        Obtém o status de uma tarefa
        """
        # Verificar tarefas ativas
        if task_id in self.active_tasks:
            return self.active_tasks[task_id]
        
        # Verificar histórico
        for task in self.task_history:
            if task.task_id == task_id:
                return task
        
        return None
    
    def obter_estatisticas_servicos(self) -> Dict:
        """
        Obtém estatísticas de todos os serviços
        """
        try:
            stats = {}
            
            for service_name, config in self.services.items():
                stats[service_name] = {
                    'status': config.status,
                    'last_health_check': config.last_health_check.isoformat() if config.last_health_check else None,
                    'response_time': config.response_time,
                    'error_count': config.error_count,
                    'success_count': config.success_count,
                    'success_rate': config.success_count / (config.success_count + config.error_count) if (config.success_count + config.error_count) > 0 else 0
                }
            
            return {
                'services': stats,
                'total_services': len(self.services),
                'healthy_services': sum(1 for s in self.services.values() if s.status == "healthy"),
                'unhealthy_services': sum(1 for s in self.services.values() if s.status == "unhealthy"),
                'active_tasks': len(self.active_tasks),
                'completed_tasks': len(self.task_history)
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {}
    
    def obter_historico_tarefas(self, limit: int = 100) -> List[TaskResult]:
        """
        Obtém histórico de tarefas
        """
        try:
            return self.task_history[-limit:] if self.task_history else []
        except Exception as e:
            logger.error(f"Erro ao obter histórico: {e}")
            return []
    
    async def parar_orquestracao(self):
        """
        Para o sistema de orquestração
        """
        try:
            logger.info("Parando sistema de orquestração")
            
            self.monitoring_enabled = False
            
            # Aguardar tarefas ativas terminarem
            while self.active_tasks:
                await asyncio.sleep(1)
            
            logger.info("Sistema de orquestração parado")
            
        except Exception as e:
            logger.error(f"Erro ao parar orquestração: {e}")

# Tarefas do Celery
@celery_app.task(bind=True)
def chamar_servico(self, service_name: str, endpoint: str, dados: Dict):
    """
    Tarefa Celery para chamar serviços de forma assíncrona
    """
    try:
        import httpx
        import asyncio
        
        async def _chamar():
            config = {
                'edital_scraper': {'url': 'http://localhost:8001'},
                'edital_analyzer': {'url': 'http://localhost:8002'},
                'prova_scraper': {'url': 'http://localhost:8003'},
                'proficiency_test': {'url': 'http://localhost:8004'},
                'weakness_analyzer': {'url': 'http://localhost:8005'},
                'study_plan_generator': {'url': 'http://localhost:8006'},
                'question_predictor': {'url': 'http://localhost:8007'}
            }
            
            service_config = config.get(service_name)
            if not service_config:
                raise ValueError(f"Serviço {service_name} não encontrado")
            
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{service_config['url']}{endpoint}",
                    json=dados
                )
                
                response.raise_for_status()
                return response.json()
        
        # Executar de forma síncrona
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_chamar())
            return result
        finally:
            loop.close()
            
    except Exception as e:
        logger.error(f"Erro na tarefa Celery: {e}")
        raise

# Instância global do orquestrador
ai_orchestrator = AIOrchestrator()

# Exemplo de uso
if __name__ == "__main__":
    async def main():
        # Iniciar orquestração
        await ai_orchestrator.iniciar_orquestracao()
        
        # Executar pipeline de exemplo
        dados_usuario = {
            'user_id': '123',
            'simulados': [],
            'questoes_respondidas': []
        }
        
        task_id = await ai_orchestrator.executar_pipeline('analise_completa_usuario', dados_usuario)
        print(f"Pipeline iniciado: {task_id}")
        
        # Aguardar um pouco
        await asyncio.sleep(5)
        
        # Verificar status
        status = ai_orchestrator.obter_status_tarefa(task_id)
        print(f"Status da tarefa: {status}")
        
        # Obter estatísticas
        stats = ai_orchestrator.obter_estatisticas_servicos()
        print(f"Estatísticas: {stats}")
    
    # Executar exemplo
    asyncio.run(main())
