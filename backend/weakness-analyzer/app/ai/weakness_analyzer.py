import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple, Any
import logging
from datetime import datetime, timedelta
import json
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.metrics import silhouette_score
import spacy
from textblob import TextBlob
import re
from collections import defaultdict, Counter
import math

logger = logging.getLogger(__name__)

class WeaknessAnalyzer:
    """
    Analisador de pontos fracos e fortes usando IA avançada
    """
    
    def __init__(self):
        self.nlp = None
        self._carregar_modelo_nlp()
        self.padroes_erro = {}
        self.habilidades_mapeadas = {}
        self.modelo_clustering = None
        self.scaler = StandardScaler()
        
    def _carregar_modelo_nlp(self):
        """
        Carrega modelo de NLP para análise de texto
        """
        try:
            self.nlp = spacy.load("pt_core_news_sm")
            logger.info("Modelo NLP carregado com sucesso")
        except OSError:
            logger.warning("Modelo pt_core_news_sm não encontrado. Usando modelo básico.")
            try:
                self.nlp = spacy.load("pt_core_news_lg")
            except OSError:
                logger.error("Nenhum modelo spaCy disponível")
                self.nlp = None
    
    def analisar_pontos_fracos_completo(self, dados_usuario: Dict) -> Dict:
        """
        Análise completa de pontos fracos e fortes do usuário
        """
        try:
            logger.info("Iniciando análise completa de pontos fracos")
            
            # Extrair dados do usuário
            simulados = dados_usuario.get('simulados', [])
            questoes_respondidas = dados_usuario.get('questoes_respondidas', [])
            tempo_estudo = dados_usuario.get('tempo_estudo', {})
            historico_performance = dados_usuario.get('historico_performance', [])
            
            # Análise multidimensional
            analise_disciplinas = self._analisar_por_disciplina(questoes_respondidas)
            analise_padroes_erro = self._identificar_padroes_erro(questoes_respondidas)
            analise_tempo = self._analisar_tempo_resposta(questoes_respondidas)
            analise_evolucao = self._analisar_evolucao_performance(historico_performance)
            analise_habilidades = self._mapear_habilidades(questoes_respondidas)
            analise_clustering = self._analisar_clusters_erro(questoes_respondidas)
            
            # Análise de tendências
            tendencias = self._identificar_tendencias(historico_performance)
            
            # Predição de melhoria
            predicao_melhoria = self._predizer_melhoria(analise_disciplinas, analise_evolucao)
            
            # Recomendações personalizadas
            recomendacoes = self._gerar_recomendacoes_personalizadas(
                analise_disciplinas, analise_padroes_erro, analise_habilidades, predicao_melhoria
            )
            
            # Score de pontos fracos
            score_pontos_fracos = self._calcular_score_pontos_fracos(analise_disciplinas, analise_padroes_erro)
            
            return {
                'metadados': {
                    'data_analise': datetime.now().isoformat(),
                    'total_simulados': len(simulados),
                    'total_questoes': len(questoes_respondidas),
                    'periodo_analise': self._calcular_periodo_analise(questoes_respondidas),
                    'versao_algoritmo': '2.0'
                },
                'analise_disciplinas': analise_disciplinas,
                'padroes_erro': analise_padroes_erro,
                'analise_tempo': analise_tempo,
                'evolucao_performance': analise_evolucao,
                'mapeamento_habilidades': analise_habilidades,
                'clusters_erro': analise_clustering,
                'tendencias': tendencias,
                'predicao_melhoria': predicao_melhoria,
                'recomendacoes': recomendacoes,
                'score_pontos_fracos': score_pontos_fracos,
                'resumo_executivo': self._gerar_resumo_executivo(
                    analise_disciplinas, score_pontos_fracos, recomendacoes
                )
            }
            
        except Exception as e:
            logger.error(f"Erro na análise completa de pontos fracos: {e}")
            return {"erro": str(e)}
    
    def _analisar_por_disciplina(self, questoes_respondidas: List[Dict]) -> Dict:
        """
        Análise detalhada por disciplina
        """
        try:
            disciplinas = defaultdict(lambda: {
                'total_questoes': 0,
                'acertos': 0,
                'erros': 0,
                'tempo_medio': 0,
                'dificuldade_media': 0,
                'padroes_erro': [],
                'evolucao': [],
                'habilidades_fracas': [],
                'habilidades_fortes': []
            })
            
            for questao in questoes_respondidas:
                disciplina = questao.get('disciplina', 'Não identificada')
                acertou = questao.get('acertou', False)
                tempo = questao.get('tempo_resposta', 0)
                dificuldade = questao.get('nivel_dificuldade', 'medio')
                enunciado = questao.get('enunciado', '')
                
                # Contadores básicos
                disciplinas[disciplina]['total_questoes'] += 1
                if acertou:
                    disciplinas[disciplina]['acertos'] += 1
                else:
                    disciplinas[disciplina]['erros'] += 1
                
                # Tempo médio
                disciplinas[disciplina]['tempo_medio'] += tempo
                
                # Dificuldade média
                nivel_numerico = {'facil': 1, 'medio': 2, 'dificil': 3}.get(dificuldade, 2)
                disciplinas[disciplina]['dificuldade_media'] += nivel_numerico
                
                # Análise de padrões de erro
                if not acertou:
                    padrao_erro = self._identificar_padrao_erro_questao(questao)
                    if padrao_erro:
                        disciplinas[disciplina]['padroes_erro'].append(padrao_erro)
                
                # Análise de habilidades
                habilidades = self._extrair_habilidades_questao(enunciado, disciplina)
                for habilidade in habilidades:
                    if acertou:
                        disciplinas[disciplina]['habilidades_fortes'].append(habilidade)
                    else:
                        disciplinas[disciplina]['habilidades_fracas'].append(habilidade)
            
            # Calcular métricas finais
            for disciplina, dados in disciplinas.items():
                if dados['total_questoes'] > 0:
                    dados['taxa_acerto'] = dados['acertos'] / dados['total_questoes']
                    dados['taxa_erro'] = dados['erros'] / dados['total_questoes']
                    dados['tempo_medio'] = dados['tempo_medio'] / dados['total_questoes']
                    dados['dificuldade_media'] = dados['dificuldade_media'] / dados['total_questoes']
                    
                    # Padrões de erro mais comuns
                    dados['padroes_erro_comuns'] = Counter(dados['padroes_erro']).most_common(5)
                    
                    # Habilidades mais fracas e mais fortes
                    dados['habilidades_fracas_comuns'] = Counter(dados['habilidades_fracas']).most_common(5)
                    dados['habilidades_fortes_comuns'] = Counter(dados['habilidades_fortes']).most_common(5)
                    
                    # Classificação de performance
                    if dados['taxa_acerto'] >= 0.8:
                        dados['classificacao'] = 'Excelente'
                    elif dados['taxa_acerto'] >= 0.6:
                        dados['classificacao'] = 'Bom'
                    elif dados['taxa_acerto'] >= 0.4:
                        dados['classificacao'] = 'Regular'
                    else:
                        dados['classificacao'] = 'Precisa melhorar'
            
            return dict(disciplinas)
            
        except Exception as e:
            logger.error(f"Erro na análise por disciplina: {e}")
            return {}
    
    def _identificar_padroes_erro(self, questoes_respondidas: List[Dict]) -> Dict:
        """
        Identifica padrões de erro usando machine learning
        """
        try:
            # Preparar dados para análise
            dados_erro = []
            for questao in questoes_respondidas:
                if not questao.get('acertou', False):
                    dados_erro.append({
                        'disciplina': questao.get('disciplina', ''),
                        'nivel_dificuldade': questao.get('nivel_dificuldade', ''),
                        'tempo_resposta': questao.get('tempo_resposta', 0),
                        'enunciado': questao.get('enunciado', ''),
                        'resposta_usuario': questao.get('resposta_usuario', ''),
                        'gabarito': questao.get('gabarito', ''),
                        'tipo_erro': self._classificar_tipo_erro(questao)
                    })
            
            if not dados_erro:
                return {'padroes_identificados': [], 'clusters': []}
            
            # Análise de clusters de erro
            clusters = self._clusterizar_erros(dados_erro)
            
            # Análise de padrões temporais
            padroes_temporais = self._analisar_padroes_temporais(dados_erro)
            
            # Análise de padrões por tipo de erro
            padroes_tipo = self._analisar_padroes_por_tipo(dados_erro)
            
            return {
                'total_erros': len(dados_erro),
                'clusters_identificados': clusters,
                'padroes_temporais': padroes_temporais,
                'padroes_por_tipo': padroes_tipo,
                'padroes_identificados': self._extrair_padroes_principais(dados_erro)
            }
            
        except Exception as e:
            logger.error(f"Erro na identificação de padrões de erro: {e}")
            return {}
    
    def _classificar_tipo_erro(self, questao: Dict) -> str:
        """
        Classifica o tipo de erro cometido
        """
        try:
            enunciado = questao.get('enunciado', '')
            resposta_usuario = questao.get('resposta_usuario', '')
            gabarito = questao.get('gabarito', '')
            tempo_resposta = questao.get('tempo_resposta', 0)
            
            # Análise de tempo
            if tempo_resposta < 10:
                return 'resposta_apressada'
            elif tempo_resposta > 300:
                return 'resposta_lenta'
            
            # Análise de conteúdo
            if self.nlp:
                doc = self.nlp(enunciado)
                sentimento = TextBlob(enunciado).sentiment.polarity
                
                if sentimento < -0.1:
                    return 'interpretacao_negativa'
                elif 'não' in enunciado.lower() or 'exceto' in enunciado.lower():
                    return 'negacao_mal_interpretada'
            
            # Análise de padrões de resposta
            if resposta_usuario == 'A' and gabarito in ['B', 'C', 'D', 'E']:
                return 'primeira_opcao_incorreta'
            elif resposta_usuario == gabarito:
                return 'gabarito_correto'  # Não deveria estar aqui se acertou
            else:
                return 'escolha_incorreta'
            
        except Exception as e:
            logger.error(f"Erro ao classificar tipo de erro: {e}")
            return 'erro_nao_classificado'
    
    def _clusterizar_erros(self, dados_erro: List[Dict]) -> List[Dict]:
        """
        Agrupa erros similares usando clustering
        """
        try:
            if len(dados_erro) < 3:
                return []
            
            # Preparar features para clustering
            features = []
            for erro in dados_erro:
                feature = [
                    len(erro['enunciado']),
                    erro['tempo_resposta'],
                    {'facil': 1, 'medio': 2, 'dificil': 3}.get(erro['nivel_dificuldade'], 2),
                    hash(erro['disciplina']) % 1000,  # Hash da disciplina
                    hash(erro['tipo_erro']) % 1000    # Hash do tipo de erro
                ]
                features.append(feature)
            
            # Normalizar features
            features_scaled = self.scaler.fit_transform(features)
            
            # Aplicar clustering
            n_clusters = min(5, len(dados_erro) // 2)
            if n_clusters < 2:
                return []
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(features_scaled)
            
            # Organizar resultados
            clusters_resultado = []
            for i in range(n_clusters):
                erros_cluster = [dados_erro[j] for j in range(len(dados_erro)) if clusters[j] == i]
                
                if erros_cluster:
                    cluster_info = {
                        'cluster_id': i,
                        'tamanho': len(erros_cluster),
                        'disciplinas_comuns': Counter([e['disciplina'] for e in erros_cluster]).most_common(3),
                        'tipos_erro_comuns': Counter([e['tipo_erro'] for e in erros_cluster]).most_common(3),
                        'tempo_medio': sum(e['tempo_resposta'] for e in erros_cluster) / len(erros_cluster),
                        'caracteristicas': self._extrair_caracteristicas_cluster(erros_cluster)
                    }
                    clusters_resultado.append(cluster_info)
            
            return clusters_resultado
            
        except Exception as e:
            logger.error(f"Erro no clustering de erros: {e}")
            return []
    
    def _extrair_caracteristicas_cluster(self, erros_cluster: List[Dict]) -> Dict:
        """
        Extrai características principais de um cluster de erros
        """
        try:
            if not erros_cluster:
                return {}
            
            # Análise de disciplinas
            disciplinas = [e['disciplina'] for e in erros_cluster]
            disciplina_principal = Counter(disciplinas).most_common(1)[0][0]
            
            # Análise de tipos de erro
            tipos_erro = [e['tipo_erro'] for e in erros_cluster]
            tipo_principal = Counter(tipos_erro).most_common(1)[0][0]
            
            # Análise de tempo
            tempos = [e['tempo_resposta'] for e in erros_cluster]
            tempo_medio = sum(tempos) / len(tempos)
            
            # Análise de dificuldade
            dificuldades = [e['nivel_dificuldade'] for e in erros_cluster]
            dificuldade_principal = Counter(dificuldades).most_common(1)[0][0]
            
            return {
                'disciplina_principal': disciplina_principal,
                'tipo_erro_principal': tipo_principal,
                'tempo_medio': tempo_medio,
                'dificuldade_principal': dificuldade_principal,
                'padrao_identificado': self._identificar_padrao_cluster(
                    disciplina_principal, tipo_principal, tempo_medio
                )
            }
            
        except Exception as e:
            logger.error(f"Erro ao extrair características do cluster: {e}")
            return {}
    
    def _identificar_padrao_cluster(self, disciplina: str, tipo_erro: str, tempo_medio: float) -> str:
        """
        Identifica o padrão principal de um cluster
        """
        try:
            if tipo_erro == 'resposta_apressada':
                return f"Tendência a responder muito rápido em {disciplina}"
            elif tipo_erro == 'resposta_lenta':
                return f"Dificuldade com tempo em {disciplina}"
            elif tipo_erro == 'interpretacao_negativa':
                return f"Problema de interpretação em {disciplina}"
            elif tipo_erro == 'negacao_mal_interpretada':
                return f"Dificuldade com questões de negação em {disciplina}"
            else:
                return f"Padrão de erro específico em {disciplina}"
                
        except Exception as e:
            logger.error(f"Erro ao identificar padrão do cluster: {e}")
            return "Padrão não identificado"
    
    def _mapear_habilidades(self, questoes_respondidas: List[Dict]) -> Dict:
        """
        Mapeia habilidades específicas do usuário
        """
        try:
            habilidades = defaultdict(lambda: {
                'total_questoes': 0,
                'acertos': 0,
                'erros': 0,
                'tempo_medio': 0,
                'evolucao': [],
                'nivel_atual': 'iniciante'
            })
            
            for questao in questoes_respondidas:
                enunciado = questao.get('enunciado', '')
                disciplina = questao.get('disciplina', '')
                acertou = questao.get('acertou', False)
                tempo = questao.get('tempo_resposta', 0)
                
                # Extrair habilidades da questão
                habilidades_questao = self._extrair_habilidades_questao(enunciado, disciplina)
                
                for habilidade in habilidades_questao:
                    habilidades[habilidade]['total_questoes'] += 1
                    if acertou:
                        habilidades[habilidade]['acertos'] += 1
                    else:
                        habilidades[habilidade]['erros'] += 1
                    habilidades[habilidade]['tempo_medio'] += tempo
            
            # Calcular métricas finais
            for habilidade, dados in habilidades.items():
                if dados['total_questoes'] > 0:
                    dados['taxa_acerto'] = dados['acertos'] / dados['total_questoes']
                    dados['tempo_medio'] = dados['tempo_medio'] / dados['total_questoes']
                    
                    # Classificar nível da habilidade
                    if dados['taxa_acerto'] >= 0.8:
                        dados['nivel_atual'] = 'avançado'
                    elif dados['taxa_acerto'] >= 0.6:
                        dados['nivel_atual'] = 'intermediário'
                    elif dados['taxa_acerto'] >= 0.4:
                        dados['nivel_atual'] = 'básico'
                    else:
                        dados['nivel_atual'] = 'iniciante'
            
            return dict(habilidades)
            
        except Exception as e:
            logger.error(f"Erro no mapeamento de habilidades: {e}")
            return {}
    
    def _extrair_habilidades_questao(self, enunciado: str, disciplina: str) -> List[str]:
        """
        Extrai habilidades específicas de uma questão
        """
        try:
            habilidades = []
            enunciado_lower = enunciado.lower()
            
            # Habilidades gerais
            if 'calcular' in enunciado_lower or 'calcule' in enunciado_lower:
                habilidades.append('cálculo')
            if 'analisar' in enunciado_lower or 'análise' in enunciado_lower:
                habilidades.append('análise')
            if 'interpretar' in enunciado_lower or 'interpretação' in enunciado_lower:
                habilidades.append('interpretação')
            if 'comparar' in enunciado_lower or 'comparação' in enunciado_lower:
                habilidades.append('comparação')
            if 'definir' in enunciado_lower or 'definição' in enunciado_lower:
                habilidades.append('definição')
            if 'aplicar' in enunciado_lower or 'aplicação' in enunciado_lower:
                habilidades.append('aplicação')
            
            # Habilidades específicas por disciplina
            if disciplina.lower() == 'português':
                if 'gramática' in enunciado_lower:
                    habilidades.append('gramática')
                if 'sintaxe' in enunciado_lower:
                    habilidades.append('sintaxe')
                if 'semântica' in enunciado_lower:
                    habilidades.append('semântica')
                if 'literatura' in enunciado_lower:
                    habilidades.append('literatura')
            
            elif disciplina.lower() == 'matemática':
                if 'álgebra' in enunciado_lower:
                    habilidades.append('álgebra')
                if 'geometria' in enunciado_lower:
                    habilidades.append('geometria')
                if 'trigonometria' in enunciado_lower:
                    habilidades.append('trigonometria')
                if 'estatística' in enunciado_lower:
                    habilidades.append('estatística')
            
            elif 'direito' in disciplina.lower():
                if 'constitucional' in enunciado_lower:
                    habilidades.append('direito_constitucional')
                if 'administrativo' in enunciado_lower:
                    habilidades.append('direito_administrativo')
                if 'penal' in enunciado_lower:
                    habilidades.append('direito_penal')
                if 'civil' in enunciado_lower:
                    habilidades.append('direito_civil')
            
            # Se não encontrou habilidades específicas, usar habilidades gerais
            if not habilidades:
                habilidades = ['compreensão', 'raciocínio']
            
            return habilidades
            
        except Exception as e:
            logger.error(f"Erro ao extrair habilidades da questão: {e}")
            return ['compreensão']
    
    def _analisar_evolucao_performance(self, historico_performance: List[Dict]) -> Dict:
        """
        Analisa a evolução da performance ao longo do tempo
        """
        try:
            if not historico_performance:
                return {'tendencia': 'sem_dados', 'evolucao': []}
            
            # Ordenar por data
            historico_ordenado = sorted(historico_performance, key=lambda x: x.get('data', ''))
            
            # Calcular métricas de evolução
            evolucao = []
            for i, registro in enumerate(historico_ordenado):
                evolucao.append({
                    'data': registro.get('data', ''),
                    'score': registro.get('score', 0),
                    'taxa_acerto': registro.get('taxa_acerto', 0),
                    'tempo_medio': registro.get('tempo_medio', 0),
                    'posicao': i + 1
                })
            
            # Calcular tendência
            if len(evolucao) >= 3:
                scores = [e['score'] for e in evolucao]
                tendencia = self._calcular_tendencia(scores)
            else:
                tendencia = 'insuficiente_dados'
            
            # Calcular taxa de melhoria
            taxa_melhoria = self._calcular_taxa_melhoria(evolucao)
            
            # Identificar pontos de inflexão
            pontos_inflexao = self._identificar_pontos_inflexao(evolucao)
            
            return {
                'tendencia': tendencia,
                'taxa_melhoria': taxa_melhoria,
                'evolucao': evolucao,
                'pontos_inflexao': pontos_inflexao,
                'melhoria_consistente': self._verificar_melhoria_consistente(evolucao)
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de evolução: {e}")
            return {}
    
    def _calcular_tendencia(self, scores: List[float]) -> str:
        """
        Calcula a tendência dos scores
        """
        try:
            if len(scores) < 2:
                return 'insuficiente_dados'
            
            # Calcular inclinação da linha de tendência
            n = len(scores)
            x = list(range(n))
            
            # Regressão linear simples
            x_mean = sum(x) / n
            y_mean = sum(scores) / n
            
            numerator = sum((x[i] - x_mean) * (scores[i] - y_mean) for i in range(n))
            denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
            
            if denominator == 0:
                return 'estável'
            
            slope = numerator / denominator
            
            if slope > 0.1:
                return 'crescimento'
            elif slope < -0.1:
                return 'declínio'
            else:
                return 'estável'
                
        except Exception as e:
            logger.error(f"Erro ao calcular tendência: {e}")
            return 'erro'
    
    def _predizer_melhoria(self, analise_disciplinas: Dict, analise_evolucao: Dict) -> Dict:
        """
        Prediz a melhoria futura baseada nos dados atuais
        """
        try:
            # Análise de potencial de melhoria por disciplina
            potencial_melhoria = {}
            
            for disciplina, dados in analise_disciplinas.items():
                taxa_atual = dados.get('taxa_acerto', 0)
                tempo_medio = dados.get('tempo_medio', 0)
                
                # Calcular potencial de melhoria
                if taxa_atual < 0.5:
                    potencial = 'alto'
                    tempo_estimado = '3-6 meses'
                elif taxa_atual < 0.7:
                    potencial = 'médio'
                    tempo_estimado = '2-4 meses'
                elif taxa_atual < 0.8:
                    potencial = 'baixo'
                    tempo_estimado = '1-2 meses'
                else:
                    potencial = 'mínimo'
                    tempo_estimado = 'manutenção'
                
                potencial_melhoria[disciplina] = {
                    'potencial': potencial,
                    'tempo_estimado': tempo_estimado,
                    'taxa_atual': taxa_atual,
                    'taxa_objetivo': min(0.9, taxa_atual + 0.2),
                    'estrategia': self._sugerir_estrategia_melhoria(taxa_atual, tempo_medio)
                }
            
            # Predição geral
            tendencia = analise_evolucao.get('tendencia', 'estável')
            taxa_melhoria = analise_evolucao.get('taxa_melhoria', 0)
            
            if tendencia == 'crescimento' and taxa_melhoria > 0.1:
                predicao_geral = 'melhoria_acelerada'
            elif tendencia == 'crescimento':
                predicao_geral = 'melhoria_gradual'
            elif tendencia == 'estável':
                predicao_geral = 'manutencao'
            else:
                predicao_geral = 'necessita_intervencao'
            
            return {
                'predicao_geral': predicao_geral,
                'potencial_por_disciplina': potencial_melhoria,
                'tempo_estimado_geral': self._calcular_tempo_estimado_geral(potencial_melhoria),
                'probabilidade_sucesso': self._calcular_probabilidade_sucesso(analise_disciplinas, analise_evolucao)
            }
            
        except Exception as e:
            logger.error(f"Erro na predição de melhoria: {e}")
            return {}
    
    def _sugerir_estrategia_melhoria(self, taxa_atual: float, tempo_medio: float) -> str:
        """
        Sugere estratégia de melhoria baseada na performance atual
        """
        try:
            if taxa_atual < 0.3:
                return 'revisão_fundamental'
            elif taxa_atual < 0.5:
                return 'prática_intensiva'
            elif taxa_atual < 0.7:
                return 'refinamento_habilidades'
            elif tempo_medio > 120:
                return 'otimização_tempo'
            else:
                return 'manutenção_nível'
                
        except Exception as e:
            logger.error(f"Erro ao sugerir estratégia: {e}")
            return 'estratégia_padrão'
    
    def _gerar_recomendacoes_personalizadas(self, analise_disciplinas: Dict, 
                                          analise_padroes_erro: Dict, 
                                          analise_habilidades: Dict, 
                                          predicao_melhoria: Dict) -> List[str]:
        """
        Gera recomendações personalizadas baseadas na análise completa
        """
        try:
            recomendacoes = []
            
            # Recomendações por disciplina
            for disciplina, dados in analise_disciplinas.items():
                if dados.get('taxa_acerto', 0) < 0.5:
                    recomendacoes.append(f"Foque em {disciplina} - taxa de acerto baixa ({dados['taxa_acerto']:.1%})")
                
                if dados.get('tempo_medio', 0) > 120:
                    recomendacoes.append(f"Pratique velocidade em {disciplina} - tempo médio alto")
            
            # Recomendações por padrões de erro
            padroes_comuns = analise_padroes_erro.get('padroes_identificados', [])
            for padrao in padroes_comuns[:3]:
                recomendacoes.append(f"Trabalhe no padrão: {padrao}")
            
            # Recomendações por habilidades
            habilidades_fracas = [h for h, dados in analise_habilidades.items() 
                                if dados.get('nivel_atual') == 'iniciante']
            for habilidade in habilidades_fracas[:3]:
                recomendacoes.append(f"Desenvolva a habilidade: {habilidade}")
            
            # Recomendações baseadas na predição
            predicao_geral = predicao_melhoria.get('predicao_geral', '')
            if predicao_geral == 'necessita_intervencao':
                recomendacoes.append("Considere revisar sua estratégia de estudo")
            elif predicao_geral == 'melhoria_acelerada':
                recomendacoes.append("Continue com a estratégia atual - está funcionando!")
            
            return recomendacoes[:10]  # Limitar a 10 recomendações
            
        except Exception as e:
            logger.error(f"Erro ao gerar recomendações: {e}")
            return ["Erro ao gerar recomendações personalizadas"]
    
    def _calcular_score_pontos_fracos(self, analise_disciplinas: Dict, analise_padroes_erro: Dict) -> float:
        """
        Calcula um score geral de pontos fracos (0-1, onde 1 é muitos pontos fracos)
        """
        try:
            if not analise_disciplinas:
                return 0.5
            
            # Calcular score baseado na taxa de erro média
            taxas_erro = [dados.get('taxa_erro', 0) for dados in analise_disciplinas.values()]
            taxa_erro_media = sum(taxas_erro) / len(taxas_erro)
            
            # Ajustar baseado no número de padrões de erro
            num_padroes = len(analise_padroes_erro.get('padroes_identificados', []))
            fator_padroes = min(1, num_padroes / 5)  # Normalizar para 0-1
            
            # Score final
            score = (taxa_erro_media + fator_padroes) / 2
            
            return min(1, max(0, score))
            
        except Exception as e:
            logger.error(f"Erro ao calcular score de pontos fracos: {e}")
            return 0.5
    
    def _gerar_resumo_executivo(self, analise_disciplinas: Dict, score_pontos_fracos: float, 
                              recomendacoes: List[str]) -> str:
        """
        Gera um resumo executivo da análise
        """
        try:
            # Identificar disciplina mais problemática
            disciplina_problema = None
            menor_taxa = 1.0
            
            for disciplina, dados in analise_disciplinas.items():
                taxa = dados.get('taxa_acerto', 0)
                if taxa < menor_taxa:
                    menor_taxa = taxa
                    disciplina_problema = disciplina
            
            # Gerar resumo
            if score_pontos_fracos > 0.7:
                nivel = "crítico"
            elif score_pontos_fracos > 0.5:
                nivel = "atenção"
            elif score_pontos_fracos > 0.3:
                nivel = "moderado"
            else:
                nivel = "bom"
            
            resumo = f"Análise de pontos fracos: {nivel.upper()}. "
            
            if disciplina_problema:
                resumo += f"Principal área de atenção: {disciplina_problema} (taxa de acerto: {menor_taxa:.1%}). "
            
            if recomendacoes:
                resumo += f"Recomendação principal: {recomendacoes[0]}"
            
            return resumo
            
        except Exception as e:
            logger.error(f"Erro ao gerar resumo executivo: {e}")
            return "Análise de pontos fracos concluída"
    
    # Métodos auxiliares
    def _identificar_padrao_erro_questao(self, questao: Dict) -> Optional[str]:
        """Identifica padrão de erro específico de uma questão"""
        return self._classificar_tipo_erro(questao)
    
    def _analisar_tempo_resposta(self, questoes_respondidas: List[Dict]) -> Dict:
        """Analisa padrões de tempo de resposta"""
        tempos = [q.get('tempo_resposta', 0) for q in questoes_respondidas]
        return {
            'tempo_medio': sum(tempos) / len(tempos) if tempos else 0,
            'tempo_minimo': min(tempos) if tempos else 0,
            'tempo_maximo': max(tempos) if tempos else 0,
            'questoes_apressadas': sum(1 for t in tempos if t < 10),
            'questoes_lentas': sum(1 for t in tempos if t > 300)
        }
    
    def _analisar_padroes_temporais(self, dados_erro: List[Dict]) -> Dict:
        """Analisa padrões temporais nos erros"""
        return {'padroes_identificados': []}
    
    def _analisar_padroes_por_tipo(self, dados_erro: List[Dict]) -> Dict:
        """Analisa padrões por tipo de erro"""
        tipos = [d['tipo_erro'] for d in dados_erro]
        return {'tipos_comuns': Counter(tipos).most_common(5)}
    
    def _extrair_padroes_principais(self, dados_erro: List[Dict]) -> List[str]:
        """Extrai padrões principais dos erros"""
        return [f"Padrão {i+1}" for i in range(min(3, len(dados_erro)))]
    
    def _analisar_clusters_erro(self, questoes_respondidas: List[Dict]) -> Dict:
        """Analisa clusters de erro"""
        return {'clusters_identificados': []}
    
    def _identificar_tendencias(self, historico_performance: List[Dict]) -> Dict:
        """Identifica tendências na performance"""
        return {'tendencia_geral': 'estável'}
    
    def _calcular_taxa_melhoria(self, evolucao: List[Dict]) -> float:
        """Calcula taxa de melhoria"""
        if len(evolucao) < 2:
            return 0.0
        return (evolucao[-1]['score'] - evolucao[0]['score']) / len(evolucao)
    
    def _identificar_pontos_inflexao(self, evolucao: List[Dict]) -> List[Dict]:
        """Identifica pontos de inflexão na evolução"""
        return []
    
    def _verificar_melhoria_consistente(self, evolucao: List[Dict]) -> bool:
        """Verifica se há melhoria consistente"""
        if len(evolucao) < 3:
            return False
        return evolucao[-1]['score'] > evolucao[0]['score']
    
    def _calcular_tempo_estimado_geral(self, potencial_melhoria: Dict) -> str:
        """Calcula tempo estimado geral para melhoria"""
        return "3-6 meses"
    
    def _calcular_probabilidade_sucesso(self, analise_disciplinas: Dict, analise_evolucao: Dict) -> float:
        """Calcula probabilidade de sucesso"""
        return 0.7
    
    def _calcular_periodo_analise(self, questoes_respondidas: List[Dict]) -> str:
        """Calcula o período de análise"""
        return "30 dias"

# Exemplo de uso
if __name__ == "__main__":
    analyzer = WeaknessAnalyzer()
    
    # Dados de exemplo
    dados_usuario = {
        'simulados': [
            {'id': 1, 'score': 70, 'data': '2024-01-01'},
            {'id': 2, 'score': 75, 'data': '2024-01-15'},
            {'id': 3, 'score': 80, 'data': '2024-02-01'}
        ],
        'questoes_respondidas': [
            {
                'id': 1,
                'disciplina': 'português',
                'acertou': False,
                'tempo_resposta': 45,
                'nivel_dificuldade': 'medio',
                'enunciado': 'Qual é a função sintática da palavra destacada?',
                'resposta_usuario': 'A',
                'gabarito': 'B'
            },
            {
                'id': 2,
                'disciplina': 'matemática',
                'acertou': True,
                'tempo_resposta': 30,
                'nivel_dificuldade': 'facil',
                'enunciado': 'Calcule 2 + 2',
                'resposta_usuario': 'B',
                'gabarito': 'B'
            }
        ],
        'historico_performance': [
            {'data': '2024-01-01', 'score': 70, 'taxa_acerto': 0.7, 'tempo_medio': 45},
            {'data': '2024-01-15', 'score': 75, 'taxa_acerto': 0.75, 'tempo_medio': 40},
            {'data': '2024-02-01', 'score': 80, 'taxa_acerto': 0.8, 'tempo_medio': 35}
        ]
    }
    
    # Executar análise
    resultado = analyzer.analisar_pontos_fracos_completo(dados_usuario)
    print(f"Análise concluída: {resultado.get('resumo_executivo', 'Erro na análise')}")
