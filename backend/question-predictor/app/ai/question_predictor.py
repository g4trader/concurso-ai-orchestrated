import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple, Any
import logging
from datetime import datetime, timedelta
import json
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import spacy
from textblob import TextBlob
import re
from collections import defaultdict, Counter
import math
import pickle
import joblib

logger = logging.getLogger(__name__)

class QuestionPredictor:
    """
    Preditor de questões que cairão nas provas usando IA avançada
    """
    
    def __init__(self):
        self.nlp = None
        self._carregar_modelo_nlp()
        self.modelo_predicao = None
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='portuguese')
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.padroes_historicos = {}
        self.tendencias = {}
        self.modelo_treinado = False
        
    def _carregar_modelo_nlp(self):
        """Carrega modelo de NLP para análise de texto"""
        try:
            self.nlp = spacy.load("pt_core_news_sm")
            logger.info("Modelo NLP carregado com sucesso")
        except OSError:
            logger.warning("Modelo pt_core_news_sm não encontrado")
            self.nlp = None
    
    def treinar_modelo_predicao(self, dados_historicos: List[Dict]) -> Dict:
        """
        Treina o modelo de predição baseado em dados históricos
        """
        try:
            logger.info("Iniciando treinamento do modelo de predição")
            
            if not dados_historicos:
                return {"erro": "Nenhum dado histórico disponível"}
            
            # Preparar dados para treinamento
            X, y = self._preparar_dados_treinamento(dados_historicos)
            
            if len(X) < 50:
                return {"erro": "Dados insuficientes para treinamento (mínimo 50 questões)"}
            
            # Dividir dados
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            # Treinar modelo
            self.modelo_predicao = GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=6,
                random_state=42
            )
            
            self.modelo_predicao.fit(X_train, y_train)
            
            # Avaliar modelo
            y_pred = self.modelo_predicao.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            # Validação cruzada
            cv_scores = cross_val_score(self.modelo_predicao, X, y, cv=5)
            
            # Salvar modelo
            self._salvar_modelo()
            
            self.modelo_treinado = True
            
            logger.info(f"Modelo treinado com precisão: {accuracy:.3f}")
            
            return {
                'status': 'sucesso',
                'precisao': accuracy,
                'cv_scores': cv_scores.tolist(),
                'cv_media': cv_scores.mean(),
                'questoes_treinamento': len(X),
                'questoes_teste': len(X_test),
                'relatorio': classification_report(y_test, y_pred, output_dict=True)
            }
            
        except Exception as e:
            logger.error(f"Erro no treinamento do modelo: {e}")
            return {"erro": str(e)}
    
    def _preparar_dados_treinamento(self, dados_historicos: List[Dict]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Prepara dados para treinamento do modelo
        """
        try:
            features = []
            labels = []
            
            for questao in dados_historicos:
                # Extrair features da questão
                feature_vector = self._extrair_features_questao(questao)
                if feature_vector is not None:
                    features.append(feature_vector)
                    
                    # Label: se a questão caiu em provas recentes
                    label = self._determinar_label_questao(questao)
                    labels.append(label)
            
            # Converter para arrays numpy
            X = np.array(features)
            y = np.array(labels)
            
            # Normalizar features
            X = self.scaler.fit_transform(X)
            
            return X, y
            
        except Exception as e:
            logger.error(f"Erro na preparação dos dados: {e}")
            return np.array([]), np.array([])
    
    def _extrair_features_questao(self, questao: Dict) -> Optional[List[float]]:
        """
        Extrai features de uma questão para o modelo
        """
        try:
            features = []
            
            # Features básicas
            enunciado = questao.get('enunciado', '')
            disciplina = questao.get('disciplina', '')
            nivel_dificuldade = questao.get('nivel_dificuldade', 'medio')
            banca = questao.get('banca', '')
            ano = questao.get('ano', 2020)
            
            # Features de texto
            features.extend([
                len(enunciado),  # Comprimento do enunciado
                len(enunciado.split()),  # Número de palavras
                enunciado.count('?'),  # Número de perguntas
                enunciado.count('.'),  # Número de pontos
            ])
            
            # Features de opções
            opcoes = questao.get('opcoes', [])
            features.extend([
                len(opcoes),  # Número de opções
                sum(len(opcao) for opcao in opcoes) / len(opcoes) if opcoes else 0,  # Comprimento médio
            ])
            
            # Features de dificuldade
            nivel_numerico = {'facil': 1, 'medio': 2, 'dificil': 3}.get(nivel_dificuldade, 2)
            features.append(nivel_numerico)
            
            # Features de disciplina (one-hot encoding)
            disciplinas_principais = [
                'português', 'matemática', 'direito', 'administração', 
                'informática', 'história', 'geografia', 'atualidades'
            ]
            
            for disc in disciplinas_principais:
                features.append(1 if disc in disciplina.lower() else 0)
            
            # Features de banca
            bancas_principais = ['cespe', 'fgv', 'fcc', 'vunesp', 'cesgranrio']
            for b in bancas_principais:
                features.append(1 if b in banca.lower() else 0)
            
            # Features temporais
            features.extend([
                ano - 2020,  # Anos desde 2020
                self._calcular_tendencia_temporal(questao),  # Tendência temporal
            ])
            
            # Features de conteúdo
            features.extend(self._extrair_features_conteudo(enunciado))
            
            # Features de padrões
            features.extend(self._extrair_features_padroes(questao))
            
            return features
            
        except Exception as e:
            logger.error(f"Erro ao extrair features da questão: {e}")
            return None
    
    def _extrair_features_conteudo(self, enunciado: str) -> List[float]:
        """
        Extrai features de conteúdo do enunciado
        """
        try:
            features = []
            
            if self.nlp:
                doc = self.nlp(enunciado)
                
                # Features de NLP
                features.extend([
                    len(doc.ents),  # Número de entidades
                    len([token for token in doc if token.pos_ == 'NOUN']),  # Substantivos
                    len([token for token in doc if token.pos_ == 'VERB']),  # Verbos
                    len([token for token in doc if token.pos_ == 'ADJ']),  # Adjetivos
                ])
                
                # Análise de sentimento
                sentimento = TextBlob(enunciado).sentiment
                features.extend([sentimento.polarity, sentimento.subjectivity])
            else:
                features.extend([0, 0, 0, 0, 0, 0])
            
            # Features de padrões de texto
            features.extend([
                1 if 'não' in enunciado.lower() else 0,  # Negação
                1 if 'exceto' in enunciado.lower() else 0,  # Exceção
                1 if 'correto' in enunciado.lower() else 0,  # Correto
                1 if 'incorreto' in enunciado.lower() else 0,  # Incorreto
                1 if 'assinale' in enunciado.lower() else 0,  # Assinale
                1 if 'marque' in enunciado.lower() else 0,  # Marque
            ])
            
            return features
            
        except Exception as e:
            logger.error(f"Erro ao extrair features de conteúdo: {e}")
            return [0] * 12
    
    def _extrair_features_padroes(self, questao: Dict) -> List[float]:
        """
        Extrai features de padrões da questão
        """
        try:
            features = []
            
            # Padrões de estrutura
            enunciado = questao.get('enunciado', '')
            opcoes = questao.get('opcoes', [])
            
            # Padrão de alternativas
            padrao_alternativas = 0
            if opcoes:
                for opcao in opcoes:
                    if re.match(r'^[A-E]\)', opcao.strip()):
                        padrao_alternativas += 1
            features.append(padrao_alternativas / len(opcoes) if opcoes else 0)
            
            # Padrão de numeração
            features.append(1 if re.search(r'\d+\.', enunciado) else 0)
            
            # Padrão de citação
            features.append(1 if '"' in enunciado or "'" in enunciado else 0)
            
            # Padrão de lista
            features.append(1 if re.search(r'[a-z]\)', enunciado) else 0)
            
            return features
            
        except Exception as e:
            logger.error(f"Erro ao extrair features de padrões: {e}")
            return [0, 0, 0, 0]
    
    def _determinar_label_questao(self, questao: Dict) -> int:
        """
        Determina o label da questão (1 se caiu recentemente, 0 caso contrário)
        """
        try:
            # Verificar se a questão caiu em provas recentes
            data_questao = questao.get('data', '')
            if data_questao:
                try:
                    data = datetime.strptime(data_questao, '%Y-%m-%d')
                    # Considerar "recente" se foi nos últimos 2 anos
                    if data > datetime.now() - timedelta(days=730):
                        return 1
                except ValueError:
                    pass
            
            # Verificar frequência de aparição
            frequencia = questao.get('frequencia_aparição', 0)
            if frequencia > 2:  # Apareceu em mais de 2 provas
                return 1
            
            return 0
            
        except Exception as e:
            logger.error(f"Erro ao determinar label: {e}")
            return 0
    
    def _calcular_tendencia_temporal(self, questao: Dict) -> float:
        """
        Calcula tendência temporal da questão
        """
        try:
            # Análise de tendência baseada no ano e frequência
            ano = questao.get('ano', 2020)
            frequencia = questao.get('frequencia_aparição', 0)
            
            # Tendência positiva se questão é recente e frequente
            tendencia = (ano - 2020) * 0.1 + frequencia * 0.2
            
            return min(1.0, max(0.0, tendencia))
            
        except Exception as e:
            logger.error(f"Erro ao calcular tendência temporal: {e}")
            return 0.0
    
    def predizer_questoes_futuras(self, contexto: Dict) -> Dict:
        """
        Prediz questões que podem cair em futuras provas
        """
        try:
            if not self.modelo_treinado:
                return {"erro": "Modelo não foi treinado"}
            
            logger.info("Iniciando predição de questões futuras")
            
            # Extrair contexto
            banca_alvo = contexto.get('banca', '')
            disciplina_alvo = contexto.get('disciplina', '')
            nivel_alvo = contexto.get('nivel', 'medio')
            edital_alvo = contexto.get('edital', {})
            
            # Gerar questões candidatas
            questoes_candidatas = self._gerar_questoes_candidatas(
                banca_alvo, disciplina_alvo, nivel_alvo, edital_alvo
            )
            
            # Predizer probabilidade de cada questão
            questoes_preditas = []
            for questao in questoes_candidatas:
                probabilidade = self._predizer_probabilidade_questao(questao)
                if probabilidade > 0.3:  # Threshold mínimo
                    questoes_preditas.append({
                        'questao': questao,
                        'probabilidade': probabilidade,
                        'confianca': self._calcular_confianca_predicao(questao),
                        'razoes': self._explicar_predicao(questao, probabilidade)
                    })
            
            # Ordenar por probabilidade
            questoes_preditas.sort(key=lambda x: x['probabilidade'], reverse=True)
            
            # Análise de tendências
            tendencias = self._analisar_tendencias_predicao(questoes_preditas)
            
            # Recomendações
            recomendacoes = self._gerar_recomendacoes_predicao(
                questoes_preditas, contexto
            )
            
            return {
                'metadados': {
                    'data_predicao': datetime.now().isoformat(),
                    'banca_alvo': banca_alvo,
                    'disciplina_alvo': disciplina_alvo,
                    'total_candidatas': len(questoes_candidatas),
                    'total_preditas': len(questoes_preditas),
                    'versao_modelo': '1.0'
                },
                'questoes_preditas': questoes_preditas[:20],  # Top 20
                'tendencias': tendencias,
                'recomendacoes': recomendacoes,
                'estatisticas': self._calcular_estatisticas_predicao(questoes_preditas)
            }
            
        except Exception as e:
            logger.error(f"Erro na predição de questões: {e}")
            return {"erro": str(e)}
    
    def _gerar_questoes_candidatas(self, banca: str, disciplina: str, 
                                 nivel: str, edital: Dict) -> List[Dict]:
        """
        Gera questões candidatas baseadas no contexto
        """
        try:
            questoes_candidatas = []
            
            # Buscar questões similares no histórico
            questoes_similares = self._buscar_questoes_similares(
                banca, disciplina, nivel
            )
            
            # Gerar variações das questões similares
            for questao_base in questoes_similares:
                variacoes = self._gerar_variacoes_questao(questao_base, edital)
                questoes_candidatas.extend(variacoes)
            
            # Gerar questões baseadas em padrões
            questoes_padrao = self._gerar_questoes_por_padroes(
                banca, disciplina, nivel, edital
            )
            questoes_candidatas.extend(questoes_padrao)
            
            # Gerar questões baseadas em tendências
            questoes_tendencia = self._gerar_questoes_por_tendencias(
                banca, disciplina, nivel
            )
            questoes_candidatas.extend(questoes_tendencia)
            
            return questoes_candidatas
            
        except Exception as e:
            logger.error(f"Erro na geração de questões candidatas: {e}")
            return []
    
    def _buscar_questoes_similares(self, banca: str, disciplina: str, nivel: str) -> List[Dict]:
        """
        Busca questões similares no histórico
        """
        try:
            # Simular busca no banco de dados
            # Em implementação real, isso faria query no banco
            questoes_similares = [
                {
                    'id': 1,
                    'enunciado': 'Questão de exemplo em ' + disciplina,
                    'opcoes': ['A) Opção A', 'B) Opção B', 'C) Opção C', 'D) Opção D'],
                    'gabarito': 'B',
                    'disciplina': disciplina,
                    'nivel_dificuldade': nivel,
                    'banca': banca,
                    'ano': 2023
                }
            ]
            
            return questoes_similares
            
        except Exception as e:
            logger.error(f"Erro na busca de questões similares: {e}")
            return []
    
    def _gerar_variacoes_questao(self, questao_base: Dict, edital: Dict) -> List[Dict]:
        """
        Gera variações de uma questão base
        """
        try:
            variacoes = []
            
            # Variação 1: Mudança de contexto
            variacao1 = questao_base.copy()
            variacao1['enunciado'] = self._adaptar_enunciado_contexto(
                questao_base['enunciado'], edital
            )
            variacao1['id'] = f"{questao_base['id']}_var1"
            variacoes.append(variacao1)
            
            # Variação 2: Mudança de dificuldade
            variacao2 = questao_base.copy()
            variacao2['nivel_dificuldade'] = self._ajustar_dificuldade(
                questao_base['nivel_dificuldade']
            )
            variacao2['id'] = f"{questao_base['id']}_var2"
            variacoes.append(variacao2)
            
            # Variação 3: Mudança de opções
            variacao3 = questao_base.copy()
            variacao3['opcoes'] = self._gerar_opcoes_alternativas(
                questao_base['opcoes']
            )
            variacao3['id'] = f"{questao_base['id']}_var3"
            variacoes.append(variacao3)
            
            return variacoes
            
        except Exception as e:
            logger.error(f"Erro na geração de variações: {e}")
            return []
    
    def _gerar_questoes_por_padroes(self, banca: str, disciplina: str, 
                                  nivel: str, edital: Dict) -> List[Dict]:
        """
        Gera questões baseadas em padrões identificados
        """
        try:
            questoes = []
            
            # Padrões comuns por disciplina
            padroes = self._obter_padroes_disciplina(disciplina)
            
            for padrao in padroes:
                questao = self._criar_questao_por_padrao(padrao, banca, nivel)
                if questao:
                    questoes.append(questao)
            
            return questoes
            
        except Exception as e:
            logger.error(f"Erro na geração por padrões: {e}")
            return []
    
    def _gerar_questoes_por_tendencias(self, banca: str, disciplina: str, nivel: str) -> List[Dict]:
        """
        Gera questões baseadas em tendências identificadas
        """
        try:
            questoes = []
            
            # Tendências identificadas
            tendencias = self._identificar_tendencias_disciplina(disciplina)
            
            for tendencia in tendencias:
                questao = self._criar_questao_por_tendencia(tendencia, banca, nivel)
                if questao:
                    questoes.append(questao)
            
            return questoes
            
        except Exception as e:
            logger.error(f"Erro na geração por tendências: {e}")
            return []
    
    def _predizer_probabilidade_questao(self, questao: Dict) -> float:
        """
        Prediz a probabilidade de uma questão cair em futuras provas
        """
        try:
            if not self.modelo_treinado:
                return 0.5
            
            # Extrair features da questão
            features = self._extrair_features_questao(questao)
            if features is None:
                return 0.0
            
            # Normalizar features
            features_scaled = self.scaler.transform([features])
            
            # Predizer probabilidade
            probabilidade = self.modelo_predicao.predict_proba(features_scaled)[0][1]
            
            return float(probabilidade)
            
        except Exception as e:
            logger.error(f"Erro na predição de probabilidade: {e}")
            return 0.0
    
    def _calcular_confianca_predicao(self, questao: Dict) -> float:
        """
        Calcula a confiança na predição de uma questão
        """
        try:
            # Fatores que afetam a confiança
            confianca = 0.5  # Base
            
            # Confiança baseada na similaridade com questões históricas
            similaridade = self._calcular_similaridade_historica(questao)
            confianca += similaridade * 0.3
            
            # Confiança baseada na consistência do padrão
            consistencia = self._calcular_consistencia_padrao(questao)
            confianca += consistencia * 0.2
            
            return min(1.0, max(0.0, confianca))
            
        except Exception as e:
            logger.error(f"Erro no cálculo de confiança: {e}")
            return 0.5
    
    def _explicar_predicao(self, questao: Dict, probabilidade: float) -> List[str]:
        """
        Explica os motivos da predição
        """
        try:
            razoes = []
            
            # Razões baseadas na probabilidade
            if probabilidade > 0.7:
                razoes.append("Alta probabilidade baseada em padrões históricos")
            elif probabilidade > 0.5:
                razoes.append("Probabilidade moderada baseada em tendências")
            else:
                razoes.append("Probabilidade baixa, mas dentro do possível")
            
            # Razões baseadas nas features
            disciplina = questao.get('disciplina', '')
            if disciplina in ['português', 'matemática']:
                razoes.append("Disciplina com alta frequência em provas")
            
            nivel = questao.get('nivel_dificuldade', '')
            if nivel == 'medio':
                razoes.append("Nível de dificuldade comum em provas")
            
            banca = questao.get('banca', '')
            if banca in ['cespe', 'fgv']:
                razoes.append("Banca com padrões previsíveis")
            
            return razoes
            
        except Exception as e:
            logger.error(f"Erro na explicação da predição: {e}")
            return ["Erro na explicação"]
    
    def _analisar_tendencias_predicao(self, questoes_preditas: List[Dict]) -> Dict:
        """
        Analisa tendências nas predições
        """
        try:
            if not questoes_preditas:
                return {}
            
            # Análise por disciplina
            disciplinas = [q['questao'].get('disciplina', '') for q in questoes_preditas]
            disciplinas_comuns = Counter(disciplinas).most_common(5)
            
            # Análise por nível de dificuldade
            niveis = [q['questao'].get('nivel_dificuldade', '') for q in questoes_preditas]
            niveis_comuns = Counter(niveis).most_common(3)
            
            # Análise por banca
            bancas = [q['questao'].get('banca', '') for q in questoes_preditas]
            bancas_comuns = Counter(bancas).most_common(3)
            
            # Análise de probabilidades
            probabilidades = [q['probabilidade'] for q in questoes_preditas]
            prob_media = sum(probabilidades) / len(probabilidades)
            prob_max = max(probabilidades)
            prob_min = min(probabilidades)
            
            return {
                'disciplinas_tendencia': disciplinas_comuns,
                'niveis_tendencia': niveis_comuns,
                'bancas_tendencia': bancas_comuns,
                'probabilidade_media': prob_media,
                'probabilidade_maxima': prob_max,
                'probabilidade_minima': prob_min,
                'total_questoes': len(questoes_preditas)
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de tendências: {e}")
            return {}
    
    def _gerar_recomendacoes_predicao(self, questoes_preditas: List[Dict], 
                                    contexto: Dict) -> List[str]:
        """
        Gera recomendações baseadas nas predições
        """
        try:
            recomendacoes = []
            
            # Recomendações baseadas nas questões preditas
            if questoes_preditas:
                top_questao = questoes_preditas[0]
                recomendacoes.append(
                    f"Foque em questões similares a: {top_questao['questao'].get('enunciado', '')[:100]}..."
                )
            
            # Recomendações baseadas nas tendências
            tendencias = self._analisar_tendencias_predicao(questoes_preditas)
            if tendencias.get('disciplinas_tendencia'):
                disciplina_top = tendencias['disciplinas_tendencia'][0][0]
                recomendacoes.append(f"Priorize o estudo de {disciplina_top}")
            
            # Recomendações baseadas no contexto
            banca = contexto.get('banca', '')
            if banca:
                recomendacoes.append(f"Estude padrões específicos da banca {banca}")
            
            return recomendacoes
            
        except Exception as e:
            logger.error(f"Erro na geração de recomendações: {e}")
            return []
    
    def _calcular_estatisticas_predicao(self, questoes_preditas: List[Dict]) -> Dict:
        """
        Calcula estatísticas das predições
        """
        try:
            if not questoes_preditas:
                return {}
            
            probabilidades = [q['probabilidade'] for q in questoes_preditas]
            confiancas = [q['confianca'] for q in questoes_preditas]
            
            return {
                'probabilidade_media': sum(probabilidades) / len(probabilidades),
                'probabilidade_mediana': sorted(probabilidades)[len(probabilidades)//2],
                'confianca_media': sum(confiancas) / len(confiancas),
                'questoes_alta_probabilidade': sum(1 for p in probabilidades if p > 0.7),
                'questoes_media_probabilidade': sum(1 for p in probabilidades if 0.4 <= p <= 0.7),
                'questoes_baixa_probabilidade': sum(1 for p in probabilidades if p < 0.4)
            }
            
        except Exception as e:
            logger.error(f"Erro no cálculo de estatísticas: {e}")
            return {}
    
    def _salvar_modelo(self):
        """Salva o modelo treinado"""
        try:
            if self.modelo_predicao:
                joblib.dump(self.modelo_predicao, 'modelo_predicao_questoes.pkl')
                joblib.dump(self.scaler, 'scaler_predicao_questoes.pkl')
                logger.info("Modelo salvo com sucesso")
        except Exception as e:
            logger.error(f"Erro ao salvar modelo: {e}")
    
    def _carregar_modelo(self):
        """Carrega modelo salvo"""
        try:
            self.modelo_predicao = joblib.load('modelo_predicao_questoes.pkl')
            self.scaler = joblib.load('scaler_predicao_questoes.pkl')
            self.modelo_treinado = True
            logger.info("Modelo carregado com sucesso")
        except FileNotFoundError:
            logger.info("Modelo não encontrado, será treinado quando necessário")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo: {e}")
    
    # Métodos auxiliares
    def _adaptar_enunciado_contexto(self, enunciado: str, edital: Dict) -> str:
        """Adapta enunciado ao contexto do edital"""
        return enunciado  # Placeholder
    
    def _ajustar_dificuldade(self, nivel_atual: str) -> str:
        """Ajusta dificuldade da questão"""
        niveis = ['facil', 'medio', 'dificil']
        try:
            idx = niveis.index(nivel_atual)
            return niveis[min(idx + 1, len(niveis) - 1)]
        except ValueError:
            return 'medio'
    
    def _gerar_opcoes_alternativas(self, opcoes_originais: List[str]) -> List[str]:
        """Gera opções alternativas"""
        return opcoes_originais  # Placeholder
    
    def _obter_padroes_disciplina(self, disciplina: str) -> List[Dict]:
        """Obtém padrões comuns de uma disciplina"""
        return [{'tipo': 'padrao_exemplo', 'disciplina': disciplina}]
    
    def _criar_questao_por_padrao(self, padrao: Dict, banca: str, nivel: str) -> Optional[Dict]:
        """Cria questão baseada em padrão"""
        return {
            'id': f"padrao_{padrao['tipo']}",
            'enunciado': f"Questão baseada no padrão {padrao['tipo']}",
            'opcoes': ['A) Opção A', 'B) Opção B', 'C) Opção C', 'D) Opção D'],
            'gabarito': 'B',
            'disciplina': padrao['disciplina'],
            'nivel_dificuldade': nivel,
            'banca': banca
        }
    
    def _identificar_tendencias_disciplina(self, disciplina: str) -> List[Dict]:
        """Identifica tendências de uma disciplina"""
        return [{'tendencia': 'tendencia_exemplo', 'disciplina': disciplina}]
    
    def _criar_questao_por_tendencia(self, tendencia: Dict, banca: str, nivel: str) -> Optional[Dict]:
        """Cria questão baseada em tendência"""
        return {
            'id': f"tendencia_{tendencia['tendencia']}",
            'enunciado': f"Questão baseada na tendência {tendencia['tendencia']}",
            'opcoes': ['A) Opção A', 'B) Opção B', 'C) Opção C', 'D) Opção D'],
            'gabarito': 'C',
            'disciplina': tendencia['disciplina'],
            'nivel_dificuldade': nivel,
            'banca': banca
        }
    
    def _calcular_similaridade_historica(self, questao: Dict) -> float:
        """Calcula similaridade com questões históricas"""
        return 0.7  # Placeholder
    
    def _calcular_consistencia_padrao(self, questao: Dict) -> float:
        """Calcula consistência do padrão"""
        return 0.8  # Placeholder

# Exemplo de uso
if __name__ == "__main__":
    predictor = QuestionPredictor()
    
    # Dados históricos de exemplo
    dados_historicos = [
        {
            'id': 1,
            'enunciado': 'Qual é a capital do Brasil?',
            'opcoes': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador'],
            'gabarito': 'C',
            'disciplina': 'geografia',
            'nivel_dificuldade': 'facil',
            'banca': 'cespe',
            'ano': 2023,
            'data': '2023-01-15',
            'frequencia_aparição': 3
        },
        {
            'id': 2,
            'enunciado': 'Calcule a derivada de x²',
            'opcoes': ['x', '2x', 'x²', '2x²'],
            'gabarito': 'B',
            'disciplina': 'matemática',
            'nivel_dificuldade': 'medio',
            'banca': 'fgv',
            'ano': 2023,
            'data': '2023-02-20',
            'frequencia_aparição': 2
        }
    ]
    
    # Treinar modelo
    resultado_treinamento = predictor.treinar_modelo_predicao(dados_historicos)
    print(f"Treinamento: {resultado_treinamento}")
    
    # Predizer questões
    contexto = {
        'banca': 'cespe',
        'disciplina': 'português',
        'nivel': 'medio',
        'edital': {'disciplinas': ['português', 'matemática']}
    }
    
    predicoes = predictor.predizer_questoes_futuras(contexto)
    print(f"Predições: {predicoes.get('total_preditas', 0)} questões preditas")
