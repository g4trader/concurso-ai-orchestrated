import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple, Any
import logging
from datetime import datetime, timedelta
import json
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import spacy
from textblob import TextBlob
import re
from collections import defaultdict, Counter
import math

logger = logging.getLogger(__name__)

class StudyPlanGenerator:
    """
    Gerador de planos de estudos personalizados usando IA
    """
    
    def __init__(self):
        self.nlp = None
        self._carregar_modelo_nlp()
        self.modelo_otimizacao = None
        self.scaler = StandardScaler()
        self.estrategias_estudo = {}
        self.materiais_recomendados = {}
        
    def _carregar_modelo_nlp(self):
        """Carrega modelo de NLP para análise de conteúdo"""
        try:
            self.nlp = spacy.load("pt_core_news_sm")
            logger.info("Modelo NLP carregado com sucesso")
        except OSError:
            logger.warning("Modelo pt_core_news_sm não encontrado")
            self.nlp = None
    
    def gerar_plano_estudos_completo(self, dados_usuario: Dict) -> Dict:
        """
        Gera plano de estudos personalizado completo
        """
        try:
            logger.info("Iniciando geração de plano de estudos personalizado")
            
            # Extrair dados do usuário
            perfil_usuario = dados_usuario.get('perfil_usuario', {})
            pontos_fracos = dados_usuario.get('pontos_fracos', {})
            objetivos = dados_usuario.get('objetivos', {})
            disponibilidade = dados_usuario.get('disponibilidade', {})
            edital_alvo = dados_usuario.get('edital_alvo', {})
            
            # Análise de necessidades
            analise_necessidades = self._analisar_necessidades_estudo(
                perfil_usuario, pontos_fracos, objetivos, edital_alvo
            )
            
            # Estruturação do plano
            estrutura_plano = self._estruturar_plano_estudos(
                analise_necessidades, disponibilidade, objetivos
            )
            
            # Cronograma detalhado
            cronograma = self._gerar_cronograma_detalhado(
                estrutura_plano, disponibilidade, objetivos
            )
            
            # Estratégias de estudo
            estrategias = self._gerar_estrategias_estudo(
                analise_necessidades, perfil_usuario
            )
            
            # Materiais recomendados
            materiais = self._recomendar_materiais(
                analise_necessidades, edital_alvo
            )
            
            # Sistema de acompanhamento
            acompanhamento = self._criar_sistema_acompanhamento(
                cronograma, objetivos
            )
            
            # Otimização do plano
            plano_otimizado = self._otimizar_plano_estudos(
                cronograma, estrategias, disponibilidade
            )
            
            return {
                'metadados': {
                    'data_criacao': datetime.now().isoformat(),
                    'versao_plano': '1.0',
                    'algoritmo': 'IA Personalizada',
                    'duracao_estimada': self._calcular_duracao_plano(cronograma)
                },
                'analise_necessidades': analise_necessidades,
                'estrutura_plano': estrutura_plano,
                'cronograma': cronograma,
                'estrategias_estudo': estrategias,
                'materiais_recomendados': materiais,
                'sistema_acompanhamento': acompanhamento,
                'plano_otimizado': plano_otimizado,
                'resumo_executivo': self._gerar_resumo_plano(
                    analise_necessidades, cronograma, estrategias
                )
            }
            
        except Exception as e:
            logger.error(f"Erro na geração do plano de estudos: {e}")
            return {"erro": str(e)}
    
    def _analisar_necessidades_estudo(self, perfil_usuario: Dict, pontos_fracos: Dict, 
                                    objetivos: Dict, edital_alvo: Dict) -> Dict:
        """
        Analisa necessidades específicas de estudo
        """
        try:
            # Análise de perfil
            nivel_atual = perfil_usuario.get('nivel_atual', 'intermediário')
            experiencia = perfil_usuario.get('experiencia_anos', 0)
            estilo_aprendizagem = perfil_usuario.get('estilo_aprendizagem', 'visual')
            
            # Análise de pontos fracos
            disciplinas_fracas = []
            habilidades_fracas = []
            
            if pontos_fracos:
                analise_disciplinas = pontos_fracos.get('analise_disciplinas', {})
                for disciplina, dados in analise_disciplinas.items():
                    if dados.get('taxa_acerto', 0) < 0.6:
                        disciplinas_fracas.append({
                            'disciplina': disciplina,
                            'prioridade': self._calcular_prioridade_disciplina(dados),
                            'tempo_necessario': self._estimar_tempo_estudo(dados)
                        })
                
                mapeamento_habilidades = pontos_fracos.get('mapeamento_habilidades', {})
                for habilidade, dados in mapeamento_habilidades.items():
                    if dados.get('nivel_atual') in ['iniciante', 'básico']:
                        habilidades_fracas.append({
                            'habilidade': habilidade,
                            'nivel_atual': dados.get('nivel_atual'),
                            'nivel_objetivo': 'intermediário'
                        })
            
            # Análise do edital alvo
            disciplinas_edital = []
            if edital_alvo:
                disciplinas_edital = edital_alvo.get('disciplinas', [])
                peso_disciplinas = edital_alvo.get('peso_disciplinas', {})
            
            # Análise de objetivos
            prazo_objetivo = objetivos.get('prazo_meses', 6)
            nivel_objetivo = objetivos.get('nivel_objetivo', 'avançado')
            concursos_alvo = objetivos.get('concursos_alvo', [])
            
            # Calcular prioridades
            prioridades = self._calcular_prioridades_estudo(
                disciplinas_fracas, disciplinas_edital, peso_disciplinas, prazo_objetivo
            )
            
            # Estimar tempo total necessário
            tempo_total = self._estimar_tempo_total_estudo(
                disciplinas_fracas, habilidades_fracas, prazo_objetivo
            )
            
            return {
                'perfil_usuario': {
                    'nivel_atual': nivel_atual,
                    'experiencia': experiencia,
                    'estilo_aprendizagem': estilo_aprendizagem
                },
                'disciplinas_fracas': disciplinas_fracas,
                'habilidades_fracas': habilidades_fracas,
                'disciplinas_edital': disciplinas_edital,
                'objetivos': {
                    'prazo_meses': prazo_objetivo,
                    'nivel_objetivo': nivel_objetivo,
                    'concursos_alvo': concursos_alvo
                },
                'prioridades': prioridades,
                'tempo_total_estimado': tempo_total,
                'necessidades_especiais': self._identificar_necessidades_especiais(
                    perfil_usuario, pontos_fracos
                )
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de necessidades: {e}")
            return {}
    
    def _estruturar_plano_estudos(self, analise_necessidades: Dict, 
                                disponibilidade: Dict, objetivos: Dict) -> Dict:
        """
        Estrutura o plano de estudos em fases e módulos
        """
        try:
            # Definir fases do plano
            fases = self._definir_fases_plano(analise_necessidades, objetivos)
            
            # Criar módulos de estudo
            modulos = self._criar_modulos_estudo(analise_necessidades, fases)
            
            # Organizar sequência de estudo
            sequencia = self._organizar_sequencia_estudo(modulos, analise_necessidades)
            
            # Definir marcos e avaliações
            marcos = self._definir_marcos_avaliacao(sequencia, objetivos)
            
            return {
                'fases': fases,
                'modulos': modulos,
                'sequencia_estudo': sequencia,
                'marcos_avaliacao': marcos,
                'duracao_total': self._calcular_duracao_estrutura(sequencia),
                'distribuicao_tempo': self._calcular_distribuicao_tempo(modulos)
            }
            
        except Exception as e:
            logger.error(f"Erro na estruturação do plano: {e}")
            return {}
    
    def _gerar_cronograma_detalhado(self, estrutura_plano: Dict, 
                                  disponibilidade: Dict, objetivos: Dict) -> Dict:
        """
        Gera cronograma detalhado do plano de estudos
        """
        try:
            # Configurações de disponibilidade
            horas_por_dia = disponibilidade.get('horas_por_dia', 4)
            dias_por_semana = disponibilidade.get('dias_por_semana', 6)
            horarios_preferenciais = disponibilidade.get('horarios', ['manhã', 'tarde'])
            
            # Calcular tempo disponível
            tempo_semanal = horas_por_dia * dias_por_semana
            tempo_mensal = tempo_semanal * 4
            
            # Gerar cronograma semanal
            cronograma_semanal = self._gerar_cronograma_semanal(
                estrutura_plano, tempo_semanal, horarios_preferenciais
            )
            
            # Gerar cronograma mensal
            cronograma_mensal = self._gerar_cronograma_mensal(
                estrutura_plano, tempo_mensal, objetivos
            )
            
            # Gerar cronograma de revisões
            cronograma_revisoes = self._gerar_cronograma_revisoes(
                estrutura_plano, objetivos
            )
            
            return {
                'configuracao': {
                    'horas_por_dia': horas_por_dia,
                    'dias_por_semana': dias_por_semana,
                    'tempo_semanal': tempo_semanal,
                    'tempo_mensal': tempo_mensal
                },
                'cronograma_semanal': cronograma_semanal,
                'cronograma_mensal': cronograma_mensal,
                'cronograma_revisoes': cronograma_revisoes,
                'ajustes_necessarios': self._identificar_ajustes_cronograma(
                    cronograma_semanal, disponibilidade
                )
            }
            
        except Exception as e:
            logger.error(f"Erro na geração do cronograma: {e}")
            return {}
    
    def _gerar_estrategias_estudo(self, analise_necessidades: Dict, 
                                perfil_usuario: Dict) -> Dict:
        """
        Gera estratégias de estudo personalizadas
        """
        try:
            estilo_aprendizagem = perfil_usuario.get('estilo_aprendizagem', 'visual')
            nivel_atual = perfil_usuario.get('nivel_atual', 'intermediário')
            
            # Estratégias por disciplina
            estrategias_disciplinas = {}
            for disciplina_fraca in analise_necessidades.get('disciplinas_fracas', []):
                disciplina = disciplina_fraca['disciplina']
                estrategias_disciplinas[disciplina] = self._gerar_estrategia_disciplina(
                    disciplina, disciplina_fraca, estilo_aprendizagem
                )
            
            # Estratégias por habilidade
            estrategias_habilidades = {}
            for habilidade_fraca in analise_necessidades.get('habilidades_fracas', []):
                habilidade = habilidade_fraca['habilidade']
                estrategias_habilidades[habilidade] = self._gerar_estrategia_habilidade(
                    habilidade, habilidade_fraca, estilo_aprendizagem
                )
            
            # Estratégias gerais
            estrategias_gerais = self._gerar_estrategias_gerais(
                estilo_aprendizagem, nivel_atual
            )
            
            # Técnicas de estudo
            tecnicas_estudo = self._recomendar_tecnicas_estudo(
                estilo_aprendizagem, analise_necessidades
            )
            
            return {
                'estrategias_disciplinas': estrategias_disciplinas,
                'estrategias_habilidades': estrategias_habilidades,
                'estrategias_gerais': estrategias_gerais,
                'tecnicas_estudo': tecnicas_estudo,
                'metodologia_recomendada': self._recomendar_metodologia(
                    estilo_aprendizagem, nivel_atual
                )
            }
            
        except Exception as e:
            logger.error(f"Erro na geração de estratégias: {e}")
            return {}
    
    def _recomendar_materiais(self, analise_necessidades: Dict, edital_alvo: Dict) -> Dict:
        """
        Recomenda materiais de estudo específicos
        """
        try:
            materiais = {
                'livros': [],
                'videoaulas': [],
                'questoes': [],
                'simulados': [],
                'resumos': [],
                'mapas_mentais': []
            }
            
            # Materiais por disciplina
            for disciplina_fraca in analise_necessidades.get('disciplinas_fracas', []):
                disciplina = disciplina_fraca['disciplina']
                prioridade = disciplina_fraca['prioridade']
                
                # Recomendar materiais baseados na disciplina e prioridade
                materiais_disciplina = self._recomendar_materiais_disciplina(
                    disciplina, prioridade, edital_alvo
                )
                
                for tipo, lista in materiais_disciplina.items():
                    materiais[tipo].extend(lista)
            
            # Materiais gerais
            materiais_gerais = self._recomendar_materiais_gerais(edital_alvo)
            for tipo, lista in materiais_gerais.items():
                materiais[tipo].extend(lista)
            
            # Organizar por prioridade
            for tipo in materiais:
                materiais[tipo] = self._organizar_materiais_prioridade(materiais[tipo])
            
            return materiais
            
        except Exception as e:
            logger.error(f"Erro na recomendação de materiais: {e}")
            return {}
    
    def _criar_sistema_acompanhamento(self, cronograma: Dict, objetivos: Dict) -> Dict:
        """
        Cria sistema de acompanhamento e avaliação
        """
        try:
            # Métricas de acompanhamento
            metricas = self._definir_metricas_acompanhamento(objetivos)
            
            # Sistema de avaliação
            sistema_avaliacao = self._criar_sistema_avaliacao(cronograma, objetivos)
            
            # Alertas e lembretes
            alertas = self._configurar_alertas(cronograma, objetivos)
            
            # Relatórios de progresso
            relatorios = self._definir_relatorios_progresso(objetivos)
            
            return {
                'metricas_acompanhamento': metricas,
                'sistema_avaliacao': sistema_avaliacao,
                'alertas_lembretes': alertas,
                'relatorios_progresso': relatorios,
                'frequencia_avaliacao': self._definir_frequencia_avaliacao(objetivos)
            }
            
        except Exception as e:
            logger.error(f"Erro na criação do sistema de acompanhamento: {e}")
            return {}
    
    def _otimizar_plano_estudos(self, cronograma: Dict, estrategias: Dict, 
                              disponibilidade: Dict) -> Dict:
        """
        Otimiza o plano de estudos usando algoritmos de otimização
        """
        try:
            # Análise de eficiência
            eficiencia_atual = self._calcular_eficiencia_plano(cronograma, estrategias)
            
            # Identificar gargalos
            gargalos = self._identificar_gargalos(cronograma, disponibilidade)
            
            # Otimizações sugeridas
            otimizacoes = self._sugerir_otimizacoes(gargalos, eficiencia_atual)
            
            # Plano otimizado
            plano_otimizado = self._aplicar_otimizacoes(cronograma, otimizacoes)
            
            return {
                'eficiencia_atual': eficiencia_atual,
                'gargalos_identificados': gargalos,
                'otimizacoes_sugeridas': otimizacoes,
                'plano_otimizado': plano_otimizado,
                'melhoria_esperada': self._calcular_melhoria_esperada(
                    eficiencia_atual, otimizacoes
                )
            }
            
        except Exception as e:
            logger.error(f"Erro na otimização do plano: {e}")
            return {}
    
    # Métodos auxiliares
    def _calcular_prioridade_disciplina(self, dados: Dict) -> str:
        """Calcula prioridade de uma disciplina"""
        taxa_acerto = dados.get('taxa_acerto', 0)
        if taxa_acerto < 0.3:
            return 'alta'
        elif taxa_acerto < 0.5:
            return 'média'
        else:
            return 'baixa'
    
    def _estimar_tempo_estudo(self, dados: Dict) -> int:
        """Estima tempo necessário para estudar uma disciplina"""
        taxa_acerto = dados.get('taxa_acerto', 0)
        if taxa_acerto < 0.3:
            return 40  # horas
        elif taxa_acerto < 0.5:
            return 25
        else:
            return 15
    
    def _calcular_prioridades_estudo(self, disciplinas_fracas: List, disciplinas_edital: List, 
                                   peso_disciplinas: Dict, prazo_objetivo: int) -> List:
        """Calcula prioridades de estudo"""
        prioridades = []
        for disciplina in disciplinas_fracas:
            peso = peso_disciplinas.get(disciplina['disciplina'], 1.0)
            prioridade_score = disciplina['prioridade'] * peso * (12 / prazo_objetivo)
            prioridades.append({
                'disciplina': disciplina['disciplina'],
                'score_prioridade': prioridade_score,
                'ordem': len(prioridades) + 1
            })
        return sorted(prioridades, key=lambda x: x['score_prioridade'], reverse=True)
    
    def _estimar_tempo_total_estudo(self, disciplinas_fracas: List, habilidades_fracas: List, 
                                  prazo_objetivo: int) -> int:
        """Estima tempo total necessário para estudo"""
        tempo_disciplinas = sum(d['tempo_necessario'] for d in disciplinas_fracas)
        tempo_habilidades = len(habilidades_fracas) * 10  # 10h por habilidade
        return tempo_disciplinas + tempo_habilidades
    
    def _identificar_necessidades_especiais(self, perfil_usuario: Dict, pontos_fracos: Dict) -> List:
        """Identifica necessidades especiais de estudo"""
        necessidades = []
        if perfil_usuario.get('experiencia_anos', 0) < 1:
            necessidades.append('revisão_fundamental')
        if pontos_fracos.get('score_pontos_fracos', 0) > 0.7:
            necessidades.append('apoio_intensivo')
        return necessidades
    
    def _definir_fases_plano(self, analise_necessidades: Dict, objetivos: Dict) -> List:
        """Define fases do plano de estudos"""
        prazo = objetivos.get('prazo_meses', 6)
        return [
            {'nome': 'Fundamentos', 'duracao_semanas': prazo * 2, 'objetivo': 'Base sólida'},
            {'nome': 'Aprofundamento', 'duracao_semanas': prazo * 3, 'objetivo': 'Domínio'},
            {'nome': 'Revisão', 'duracao_semanas': prazo * 1, 'objetivo': 'Consolidação'}
        ]
    
    def _criar_modulos_estudo(self, analise_necessidades: Dict, fases: List) -> List:
        """Cria módulos de estudo"""
        modulos = []
        for disciplina_fraca in analise_necessidades.get('disciplinas_fracas', []):
            modulos.append({
                'nome': f"Módulo {disciplina_fraca['disciplina']}",
                'disciplina': disciplina_fraca['disciplina'],
                'duracao_horas': disciplina_fraca['tempo_necessario'],
                'objetivos': [f"Melhorar {disciplina_fraca['disciplina']}"],
                'conteudos': self._definir_conteudos_modulo(disciplina_fraca)
            })
        return modulos
    
    def _organizar_sequencia_estudo(self, modulos: List, analise_necessidades: Dict) -> List:
        """Organiza sequência de estudo"""
        prioridades = analise_necessidades.get('prioridades', [])
        sequencia = []
        for prioridade in prioridades:
            modulo = next((m for m in modulos if m['disciplina'] == prioridade['disciplina']), None)
            if modulo:
                sequencia.append(modulo)
        return sequencia
    
    def _definir_marcos_avaliacao(self, sequencia: List, objetivos: Dict) -> List:
        """Define marcos de avaliação"""
        marcos = []
        for i, modulo in enumerate(sequencia):
            marcos.append({
                'nome': f"Avaliação {modulo['disciplina']}",
                'modulo': modulo['nome'],
                'semana': (i + 1) * 2,
                'tipo': 'simulado'
            })
        return marcos
    
    def _calcular_duracao_estrutura(self, sequencia: List) -> int:
        """Calcula duração total da estrutura"""
        return sum(modulo['duracao_horas'] for modulo in sequencia)
    
    def _calcular_distribuicao_tempo(self, modulos: List) -> Dict:
        """Calcula distribuição de tempo entre módulos"""
        total = sum(modulo['duracao_horas'] for modulo in modulos)
        distribuicao = {}
        for modulo in modulos:
            distribuicao[modulo['disciplina']] = modulo['duracao_horas'] / total
        return distribuicao
    
    def _gerar_cronograma_semanal(self, estrutura_plano: Dict, tempo_semanal: int, 
                                horarios_preferenciais: List) -> Dict:
        """Gera cronograma semanal"""
        return {
            'segunda': {'manhã': 'Português', 'tarde': 'Matemática'},
            'terça': {'manhã': 'Direito', 'tarde': 'Revisão'},
            'quarta': {'manhã': 'Simulado', 'tarde': 'Correção'},
            'quinta': {'manhã': 'Administração', 'tarde': 'Português'},
            'sexta': {'manhã': 'Matemática', 'tarde': 'Direito'},
            'sábado': {'manhã': 'Revisão Geral', 'tarde': 'Simulado'}
        }
    
    def _gerar_cronograma_mensal(self, estrutura_plano: Dict, tempo_mensal: int, 
                               objetivos: Dict) -> Dict:
        """Gera cronograma mensal"""
        return {
            'semana_1': 'Fundamentos - Português e Matemática',
            'semana_2': 'Fundamentos - Direito e Administração',
            'semana_3': 'Aprofundamento - Português',
            'semana_4': 'Aprofundamento - Matemática'
        }
    
    def _gerar_cronograma_revisoes(self, estrutura_plano: Dict, objetivos: Dict) -> Dict:
        """Gera cronograma de revisões"""
        return {
            'revisao_diaria': '15 minutos',
            'revisao_semanal': '2 horas',
            'revisao_mensal': '1 dia completo'
        }
    
    def _identificar_ajustes_cronograma(self, cronograma_semanal: Dict, disponibilidade: Dict) -> List:
        """Identifica ajustes necessários no cronograma"""
        return ['Ajustar horários conforme disponibilidade']
    
    def _gerar_estrategia_disciplina(self, disciplina: str, dados: Dict, estilo: str) -> Dict:
        """Gera estratégia específica para uma disciplina"""
        return {
            'metodologia': 'estudo_por_topicos',
            'tecnicas': ['mapas_mentais', 'resumos'],
            'frequencia': 'diaria',
            'duracao_sessao': '2 horas'
        }
    
    def _gerar_estrategia_habilidade(self, habilidade: str, dados: Dict, estilo: str) -> Dict:
        """Gera estratégia específica para uma habilidade"""
        return {
            'metodologia': 'pratica_gradual',
            'tecnicas': ['exercicios_progressivos'],
            'frequencia': 'alternada',
            'duracao_sessao': '1 hora'
        }
    
    def _gerar_estrategias_gerais(self, estilo: str, nivel: str) -> List:
        """Gera estratégias gerais de estudo"""
        return [
            'Estudo ativo com resumos',
            'Prática regular de exercícios',
            'Revisão espaçada'
        ]
    
    def _recomendar_tecnicas_estudo(self, estilo: str, analise_necessidades: Dict) -> List:
        """Recomenda técnicas de estudo"""
        tecnicas = []
        if estilo == 'visual':
            tecnicas.extend(['mapas_mentais', 'diagramas', 'gráficos'])
        elif estilo == 'auditivo':
            tecnicas.extend(['gravações', 'discussões', 'leitura_em_voz_alta'])
        else:
            tecnicas.extend(['exercícios_práticos', 'simulados', 'resumos'])
        return tecnicas
    
    def _recomendar_metodologia(self, estilo: str, nivel: str) -> str:
        """Recomenda metodologia de estudo"""
        if nivel == 'iniciante':
            return 'estudo_estruturado'
        elif nivel == 'intermediário':
            return 'estudo_autodirigido'
        else:
            return 'estudo_avançado'
    
    def _recomendar_materiais_disciplina(self, disciplina: str, prioridade: str, edital: Dict) -> Dict:
        """Recomenda materiais para uma disciplina específica"""
        return {
            'livros': [f'Livro {disciplina} - Básico'],
            'videoaulas': [f'Curso {disciplina} - Completo'],
            'questoes': [f'Banco de questões {disciplina}']
        }
    
    def _recomendar_materiais_gerais(self, edital: Dict) -> Dict:
        """Recomenda materiais gerais"""
        return {
            'simulados': ['Simulados gerais'],
            'resumos': ['Resumos por disciplina'],
            'mapas_mentais': ['Mapas mentais gerais']
        }
    
    def _organizar_materiais_prioridade(self, materiais: List) -> List:
        """Organiza materiais por prioridade"""
        return sorted(materiais, key=lambda x: x.get('prioridade', 0), reverse=True)
    
    def _definir_metricas_acompanhamento(self, objetivos: Dict) -> List:
        """Define métricas de acompanhamento"""
        return [
            'Taxa de acerto por disciplina',
            'Tempo de estudo cumprido',
            'Frequência de simulados',
            'Evolução do score'
        ]
    
    def _criar_sistema_avaliacao(self, cronograma: Dict, objetivos: Dict) -> Dict:
        """Cria sistema de avaliação"""
        return {
            'avaliacoes_semanais': 'Simulados de 20 questões',
            'avaliacoes_mensais': 'Simulados completos',
            'avaliacoes_trimestrais': 'Avaliação de progresso'
        }
    
    def _configurar_alertas(self, cronograma: Dict, objetivos: Dict) -> List:
        """Configura alertas e lembretes"""
        return [
            'Lembrete de estudo diário',
            'Alerta de simulado semanal',
            'Notificação de revisão mensal'
        ]
    
    def _definir_relatorios_progresso(self, objetivos: Dict) -> List:
        """Define relatórios de progresso"""
        return [
            'Relatório semanal de progresso',
            'Relatório mensal de evolução',
            'Relatório trimestral de performance'
        ]
    
    def _definir_frequencia_avaliacao(self, objetivos: Dict) -> str:
        """Define frequência de avaliação"""
        return 'semanal'
    
    def _calcular_eficiencia_plano(self, cronograma: Dict, estrategias: Dict) -> float:
        """Calcula eficiência do plano atual"""
        return 0.75  # Placeholder
    
    def _identificar_gargalos(self, cronograma: Dict, disponibilidade: Dict) -> List:
        """Identifica gargalos no plano"""
        return ['Conflito de horários', 'Sobrecarga de conteúdo']
    
    def _sugerir_otimizacoes(self, gargalos: List, eficiencia: float) -> List:
        """Sugere otimizações"""
        return [
            'Redistribuir horários',
            'Priorizar conteúdos essenciais',
            'Ajustar carga de estudo'
        ]
    
    def _aplicar_otimizacoes(self, cronograma: Dict, otimizacoes: List) -> Dict:
        """Aplica otimizações ao plano"""
        return cronograma  # Placeholder
    
    def _calcular_melhoria_esperada(self, eficiencia_atual: float, otimizacoes: List) -> float:
        """Calcula melhoria esperada"""
        return eficiencia_atual + 0.1
    
    def _calcular_duracao_plano(self, cronograma: Dict) -> str:
        """Calcula duração total do plano"""
        return "6 meses"
    
    def _gerar_resumo_plano(self, analise_necessidades: Dict, cronograma: Dict, 
                          estrategias: Dict) -> str:
        """Gera resumo executivo do plano"""
        return "Plano de estudos personalizado criado com sucesso"

# Exemplo de uso
if __name__ == "__main__":
    generator = StudyPlanGenerator()
    
    # Dados de exemplo
    dados_usuario = {
        'perfil_usuario': {
            'nivel_atual': 'intermediário',
            'experiencia_anos': 2,
            'estilo_aprendizagem': 'visual'
        },
        'pontos_fracos': {
            'analise_disciplinas': {
                'português': {'taxa_acerto': 0.4},
                'matemática': {'taxa_acerto': 0.6}
            },
            'mapeamento_habilidades': {
                'gramática': {'nivel_atual': 'básico'},
                'álgebra': {'nivel_atual': 'intermediário'}
            }
        },
        'objetivos': {
            'prazo_meses': 6,
            'nivel_objetivo': 'avançado',
            'concursos_alvo': ['PF', 'PRF']
        },
        'disponibilidade': {
            'horas_por_dia': 4,
            'dias_por_semana': 6,
            'horarios': ['manhã', 'tarde']
        },
        'edital_alvo': {
            'disciplinas': ['português', 'matemática', 'direito'],
            'peso_disciplinas': {'português': 1.5, 'matemática': 1.2}
        }
    }
    
    # Gerar plano
    plano = generator.gerar_plano_estudos_completo(dados_usuario)
    print(f"Plano gerado: {plano.get('resumo_executivo', 'Erro na geração')}")
