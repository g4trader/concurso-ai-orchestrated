import asyncio
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import schedule
import time
from threading import Thread

from ..scrapers.prova_scraper import CESPEProvaScraper, FGVProvaScraper
from ..models.prova import (
    Banca, Prova, Questao, ProcessamentoProva, QualidadeQuestao, 
    EstatisticaProva, ScrapingProvaLog
)
from ..database import get_db

logger = logging.getLogger(__name__)

class ProvaOrchestrator:
    """
    Orquestrador que coordena a busca e processamento de provas
    """
    
    def __init__(self):
        self.scrapers = {
            'CESPE': CESPEProvaScraper(),
            'FGV': FGVProvaScraper(),
            # Adicionar outros scrapers aqui
        }
        self.db = next(get_db())
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.running = False
        
    def iniciar_busca_automatica(self):
        """
        Inicia a busca automática de provas em background
        """
        if self.running:
            logger.warning("Busca automática de provas já está rodando")
            return
        
        self.running = True
        
        # Configurar agendamento
        schedule.every(6).hours.do(self.executar_busca_completa)
        schedule.every(2).hours.do(self.verificar_novas_provas)
        
        # Iniciar thread de agendamento
        scheduler_thread = Thread(target=self._executar_scheduler, daemon=True)
        scheduler_thread.start()
        
        logger.info("Busca automática de provas iniciada")
    
    def _executar_scheduler(self):
        """Executa o scheduler em loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(300)  # Verificar a cada 5 minutos
    
    def parar_busca_automatica(self):
        """Para a busca automática de provas"""
        self.running = False
        logger.info("Busca automática de provas parada")
    
    async def executar_busca_completa(self) -> Dict[str, List[Dict]]:
        """
        Executa busca completa de provas de todas as bancas
        """
        logger.info("Iniciando busca completa de provas")
        resultados = {}
        
        # Executar scrapers em paralelo
        futures = []
        for nome, scraper in self.scrapers.items():
            future = self.executor.submit(self._executar_scraper_provas, nome, scraper)
            futures.append(future)
        
        # Coletar resultados
        for future in as_completed(futures):
            try:
                nome, provas = future.result()
                resultados[nome] = provas
                logger.info(f"Scraper {nome} encontrou {len(provas)} provas")
            except Exception as e:
                logger.error(f"Erro no scraper de provas: {e}")
        
        # Salvar resultados no banco
        await self._salvar_provas(resultados)
        
        logger.info("Busca completa de provas finalizada")
        return resultados
    
    def _executar_scraper_provas(self, nome: str, scraper) -> tuple:
        """
        Executa um scraper de provas específico
        """
        try:
            inicio = datetime.now()
            
            # Buscar provas
            provas = scraper.buscar_provas(limite=20)
            
            # Log da execução
            tempo_execucao = (datetime.now() - inicio).total_seconds()
            self._log_scraping_provas(nome, len(provas), tempo_execucao, "sucesso")
            
            return nome, provas
            
        except Exception as e:
            logger.error(f"Erro no scraper de provas {nome}: {e}")
            self._log_scraping_provas(nome, 0, 0, "erro", str(e))
            return nome, []
    
    def _log_scraping_provas(self, banca: str, provas_encontradas: int, 
                           tempo_execucao: float, status: str, erro: str = None):
        """
        Registra log de scraping de provas
        """
        try:
            log = ScrapingProvaLog(
                banca=banca,
                url=self.scrapers[banca].base_url if banca in self.scrapers else "",
                status=status,
                provas_encontradas=provas_encontradas,
                questoes_extraidas=0,  # Será atualizado depois
                erro_detalhes=erro,
                tempo_execucao=int(tempo_execucao)
            )
            
            self.db.add(log)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Erro ao salvar log de scraping de provas: {e}")
    
    async def processar_prova_completa(self, url_prova: str, banca: str) -> Dict:
        """
        Processa uma prova completa: extrai questões, valida e salva
        """
        try:
            logger.info(f"Processando prova: {url_prova}")
            
            # Verificar se a prova já foi processada
            prova_existente = self.db.query(Prova).filter(
                Prova.url_original == url_prova
            ).first()
            
            if prova_existente and prova_existente.status_processamento == "processado":
                logger.info("Prova já foi processada")
                return {"status": "ja_processada", "prova_id": prova_existente.id}
            
            # Criar registro de processamento
            if not prova_existente:
                prova = Prova(
                    banca_id=self._obter_banca_id(banca),
                    titulo=f"Prova {banca} - {datetime.now().strftime('%Y-%m-%d')}",
                    url_original=url_prova,
                    status_processamento="processando"
                )
                self.db.add(prova)
                self.db.commit()
                self.db.refresh(prova)
            else:
                prova = prova_existente
                prova.status_processamento = "processando"
                self.db.commit()
            
            # Criar log de processamento
            processamento = ProcessamentoProva(
                prova_id=prova.id,
                status="iniciado",
                progresso=0
            )
            self.db.add(processamento)
            self.db.commit()
            
            # Extrair questões
            scraper = self.scrapers.get(banca)
            if not scraper:
                raise ValueError(f"Scraper não encontrado para banca: {banca}")
            
            questoes_raw = scraper.extrair_questoes_prova(url_prova)
            
            # Atualizar progresso
            processamento.status = "processando"
            processamento.questoes_total = len(questoes_raw)
            self.db.commit()
            
            # Processar e salvar questões
            questoes_salvas = 0
            for i, questao_raw in enumerate(questoes_raw):
                try:
                    questao_processada = scraper._processar_questao(questao_raw)
                    if questao_processada:
                        questao = Questao(
                            prova_id=prova.id,
                            numero=questao_processada['numero'],
                            enunciado=questao_processada['enunciado'],
                            opcoes=questao_processada['opcoes'],
                            gabarito=questao_processada['gabarito'],
                            disciplina=questao_processada['disciplina'],
                            nivel_dificuldade=questao_processada['nivel_dificuldade'],
                            explicacao=questao_processada.get('explicacao', ''),
                            fonte=questao_processada['fonte'],
                            ano_original=questao_processada.get('ano'),
                            banca_original=questao_processada['fonte'],
                            tags=questao_processada.get('tags', [])
                        )
                        
                        self.db.add(questao)
                        questoes_salvas += 1
                        
                        # Avaliar qualidade da questão
                        self._avaliar_qualidade_questao(questao)
                        
                except Exception as e:
                    logger.error(f"Erro ao processar questão {i + 1}: {e}")
                    continue
                
                # Atualizar progresso
                processamento.questoes_processadas = i + 1
                processamento.progresso = int((i + 1) / len(questoes_raw) * 100)
                self.db.commit()
            
            # Finalizar processamento
            prova.status_processamento = "processado"
            processamento.status = "concluido"
            processamento.progresso = 100
            processamento.tempo_processamento = int((datetime.now() - processamento.created_at).total_seconds())
            
            self.db.commit()
            
            # Gerar estatísticas da prova
            await self._gerar_estatisticas_prova(prova.id)
            
            logger.info(f"Prova processada com sucesso: {questoes_salvas} questões salvas")
            
            return {
                "status": "sucesso",
                "prova_id": prova.id,
                "questoes_salvas": questoes_salvas,
                "questoes_total": len(questoes_raw)
            }
            
        except Exception as e:
            logger.error(f"Erro ao processar prova: {e}")
            
            # Marcar como erro
            if 'prova' in locals():
                prova.status_processamento = "erro"
                self.db.commit()
            
            return {"status": "erro", "erro": str(e)}
    
    def _obter_banca_id(self, nome_banca: str) -> int:
        """
        Obtém o ID da banca no banco de dados
        """
        banca = self.db.query(Banca).filter(Banca.nome == nome_banca).first()
        
        if not banca:
            # Criar nova banca
            banca = Banca(
                nome=nome_banca,
                sigla=nome_banca[:4].upper(),
                ativa=True
            )
            self.db.add(banca)
            self.db.commit()
            self.db.refresh(banca)
        
        return banca.id
    
    def _avaliar_qualidade_questao(self, questao: Questao):
        """
        Avalia a qualidade de uma questão
        """
        try:
            criterios = {}
            problemas = []
            sugestoes = []
            
            # Critério: Clareza do enunciado
            if len(questao.enunciado) < 50:
                criterios['clareza'] = 0.3
                problemas.append("Enunciado muito curto")
                sugestoes.append("Expandir o enunciado")
            elif len(questao.enunciado) > 1000:
                criterios['clareza'] = 0.6
                problemas.append("Enunciado muito longo")
                sugestoes.append("Simplificar o enunciado")
            else:
                criterios['clareza'] = 0.9
            
            # Critério: Número de opções
            if len(questao.opcoes) < 4:
                criterios['opcoes'] = 0.5
                problemas.append("Número insuficiente de opções")
                sugestoes.append("Adicionar mais opções")
            elif len(questao.opcoes) > 5:
                criterios['opcoes'] = 0.7
                problemas.append("Muitas opções")
                sugestoes.append("Reduzir número de opções")
            else:
                criterios['opcoes'] = 1.0
            
            # Critério: Disciplina identificada
            if questao.disciplina and questao.disciplina != 'geral':
                criterios['disciplina'] = 1.0
            else:
                criterios['disciplina'] = 0.5
                problemas.append("Disciplina não identificada")
                sugestoes.append("Classificar disciplina")
            
            # Critério: Gabarito válido
            if questao.gabarito and questao.gabarito in ['A', 'B', 'C', 'D', 'E']:
                criterios['gabarito'] = 1.0
            else:
                criterios['gabarito'] = 0.0
                problemas.append("Gabarito inválido")
                sugestoes.append("Corrigir gabarito")
            
            # Calcular score geral
            score_qualidade = sum(criterios.values()) / len(criterios)
            
            # Criar avaliação de qualidade
            qualidade = QualidadeQuestao(
                questao_id=questao.id,
                score_qualidade=score_qualidade,
                criterios_avaliacao=criterios,
                problemas_identificados=problemas,
                sugestoes_melhoria=sugestoes,
                aprovada=score_qualidade >= 0.7,
                revisada_por="sistema"
            )
            
            self.db.add(qualidade)
            
        except Exception as e:
            logger.error(f"Erro ao avaliar qualidade da questão: {e}")
    
    async def _gerar_estatisticas_prova(self, prova_id: int):
        """
        Gera estatísticas de uma prova
        """
        try:
            prova = self.db.query(Prova).filter(Prova.id == prova_id).first()
            if not prova:
                return
            
            questoes = self.db.query(Questao).filter(Questao.prova_id == prova_id).all()
            
            if not questoes:
                return
            
            # Calcular estatísticas
            total_questoes = len(questoes)
            
            # Questões por disciplina
            disciplinas = {}
            for questao in questoes:
                disciplina = questao.disciplina or 'Não identificada'
                disciplinas[disciplina] = disciplinas.get(disciplina, 0) + 1
            
            # Nível de dificuldade médio
            niveis = {'facil': 1, 'medio': 2, 'dificil': 3}
            dificuldade_media = sum(niveis.get(q.nivel_dificuldade, 2) for q in questoes) / total_questoes
            
            # Questões mais difíceis e mais fáceis
            questoes_ordenadas = sorted(questoes, key=lambda q: niveis.get(q.nivel_dificuldade, 2))
            mais_faceis = [q.id for q in questoes_ordenadas[:5]]
            mais_dificeis = [q.id for q in questoes_ordenadas[-5:]]
            
            # Criar estatísticas
            estatisticas = EstatisticaProva(
                prova_id=prova_id,
                total_questoes=total_questoes,
                questoes_por_disciplina=disciplinas,
                nivel_dificuldade_medio=dificuldade_media,
                tempo_medio_resolucao=30,  # Estimativa
                taxa_acerto_historica=0.0,  # Será calculada com dados históricos
                questoes_mais_dificeis=mais_dificeis,
                questoes_mais_faceis=mais_faceis,
                analise_tendencias={}
            )
            
            self.db.add(estatisticas)
            self.db.commit()
            
        except Exception as e:
            logger.error(f"Erro ao gerar estatísticas da prova: {e}")
    
    async def _salvar_provas(self, resultados: Dict[str, List[Dict]]):
        """
        Salva as provas encontradas no banco de dados
        """
        try:
            for banca, provas in resultados.items():
                for prova_data in provas:
                    await self._salvar_prova(prova_data, banca)
            
            self.db.commit()
            logger.info("Provas salvas no banco de dados")
            
        except Exception as e:
            logger.error(f"Erro ao salvar provas: {e}")
            self.db.rollback()
    
    async def _salvar_prova(self, prova_data: Dict, banca: str):
        """
        Salva uma prova no banco de dados
        """
        try:
            # Verificar se a prova já existe
            prova_existente = self.db.query(Prova).filter(
                Prova.url_original == prova_data.get('url')
            ).first()
            
            if prova_existente:
                # Atualizar dados existentes
                prova_existente.updated_at = datetime.now()
                return
            
            # Criar nova prova
            prova = Prova(
                banca_id=self._obter_banca_id(banca),
                titulo=prova_data.get('titulo', ''),
                url_original=prova_data.get('url', ''),
                status_processamento="pendente",
                metadados=prova_data
            )
            
            self.db.add(prova)
            
        except Exception as e:
            logger.error(f"Erro ao salvar prova: {e}")
    
    def obter_estatisticas_provas(self) -> Dict:
        """
        Obtém estatísticas das provas
        """
        try:
            # Estatísticas gerais
            total_provas = self.db.query(Prova).count()
            provas_processadas = self.db.query(Prova).filter(
                Prova.status_processamento == "processado"
            ).count()
            
            total_questoes = self.db.query(Questao).count()
            
            # Estatísticas por banca
            bancas_stats = {}
            for banca in self.scrapers.keys():
                provas_banca = self.db.query(Prova).join(Banca).filter(
                    Banca.nome == banca
                ).count()
                bancas_stats[banca] = provas_banca
            
            # Estatísticas de qualidade
            questoes_aprovadas = self.db.query(QualidadeQuestao).filter(
                QualidadeQuestao.aprovada == True
            ).count()
            
            qualidade_media = self.db.query(QualidadeQuestao).with_entities(
                QualidadeQuestao.score_qualidade
            ).all()
            
            qualidade_media = sum(q[0] for q in qualidade_media) / len(qualidade_media) if qualidade_media else 0
            
            return {
                'total_provas': total_provas,
                'provas_processadas': provas_processadas,
                'total_questoes': total_questoes,
                'questoes_aprovadas': questoes_aprovadas,
                'qualidade_media': qualidade_media,
                'provas_por_banca': bancas_stats,
                'bancas_ativas': list(self.scrapers.keys())
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas de provas: {e}")
            return {}
    
    async def verificar_novas_provas(self) -> Dict[str, List[Dict]]:
        """
        Verifica se há novas provas desde a última verificação
        """
        logger.info("Verificando novas provas")
        novas_provas = {}
        
        for nome, scraper in self.scrapers.items():
            try:
                # Buscar provas
                provas = scraper.buscar_provas(limite=10)
                
                # Verificar quais são novas
                provas_novas = []
                for prova in provas:
                    existe = self.db.query(Prova).filter(
                        Prova.url_original == prova['url']
                    ).first()
                    
                    if not existe:
                        provas_novas.append(prova)
                
                if provas_novas:
                    novas_provas[nome] = provas_novas
                    logger.info(f"Encontradas {len(provas_novas)} novas provas em {nome}")
                
            except Exception as e:
                logger.error(f"Erro ao verificar novas provas em {nome}: {e}")
        
        return novas_provas

# Instância global do orquestrador
prova_orchestrator = ProvaOrchestrator()
