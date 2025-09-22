import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
import logging
from datetime import datetime
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import math

logger = logging.getLogger(__name__)

class AdaptiveTestingEngine:
    """
    Motor de teste adaptativo para avaliação de proficiência
    """
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        self.question_bank = []
        self.user_responses = []
        self.difficulty_levels = ['facil', 'medio', 'dificil']
        self.confidence_threshold = 0.8
        self.max_questions = 50
        self.min_questions = 10
        
    def carregar_banco_questoes(self, questoes: List[Dict]):
        """
        Carrega o banco de questões para o teste adaptativo
        """
        try:
            self.question_bank = []
            
            for questao in questoes:
                questao_data = {
                    'id': questao.get('id'),
                    'enunciado': questao.get('enunciado', ''),
                    'opcoes': questao.get('opcoes', []),
                    'gabarito': questao.get('gabarito', ''),
                    'disciplina': questao.get('disciplina', ''),
                    'nivel_dificuldade': questao.get('nivel_dificuldade', 'medio'),
                    'peso': questao.get('peso', 1.0),
                    'tags': questao.get('tags', []),
                    'caracteristicas': self._extrair_caracteristicas_questao(questao)
                }
                self.question_bank.append(questao_data)
            
            logger.info(f"Banco de questões carregado: {len(self.question_bank)} questões")
            
        except Exception as e:
            logger.error(f"Erro ao carregar banco de questões: {e}")
    
    def _extrair_caracteristicas_questao(self, questao: Dict) -> List[float]:
        """
        Extrai características numéricas de uma questão para o modelo
        """
        try:
            caracteristicas = []
            
            # Características do enunciado
            enunciado = questao.get('enunciado', '')
            caracteristicas.extend([
                len(enunciado),  # Comprimento do enunciado
                enunciado.count('?'),  # Número de perguntas
                enunciado.count('.'),  # Número de pontos
                len(enunciado.split()),  # Número de palavras
            ])
            
            # Características das opções
            opcoes = questao.get('opcoes', [])
            caracteristicas.extend([
                len(opcoes),  # Número de opções
                sum(len(opcao) for opcao in opcoes) / len(opcoes) if opcoes else 0,  # Comprimento médio das opções
            ])
            
            # Características de dificuldade
            nivel = questao.get('nivel_dificuldade', 'medio')
            nivel_numerico = {'facil': 1, 'medio': 2, 'dificil': 3}.get(nivel, 2)
            caracteristicas.append(nivel_numerico)
            
            # Características de disciplina (one-hot encoding simplificado)
            disciplina = questao.get('disciplina', '').lower()
            disciplinas_principais = [
                'português', 'matemática', 'direito', 'administração', 
                'informática', 'história', 'geografia', 'atualidades'
            ]
            
            for disc in disciplinas_principais:
                caracteristicas.append(1 if disc in disciplina else 0)
            
            # Características de tags
            tags = questao.get('tags', [])
            caracteristicas.extend([
                len(tags),
                1 if 'conceitual' in tags else 0,
                1 if 'aplicação' in tags else 0,
                1 if 'análise' in tags else 0,
            ])
            
            return caracteristicas
            
        except Exception as e:
            logger.error(f"Erro ao extrair características da questão: {e}")
            return [0] * 15  # Retornar vetor de zeros com tamanho padrão
    
    def treinar_modelo(self, dados_historicos: List[Dict]):
        """
        Treina o modelo de predição de dificuldade baseado em dados históricos
        """
        try:
            if not dados_historicos:
                logger.warning("Nenhum dado histórico disponível para treinamento")
                return
            
            # Preparar dados para treinamento
            X = []  # Características das questões
            y = []  # Dificuldade real (baseada na taxa de acerto)
            
            for dado in dados_historicos:
                questao_id = dado.get('questao_id')
                taxa_acerto = dado.get('taxa_acerto', 0.5)
                
                # Encontrar questão no banco
                questao = next((q for q in self.question_bank if q['id'] == questao_id), None)
                if questao:
                    X.append(questao['caracteristicas'])
                    
                    # Converter taxa de acerto em nível de dificuldade
                    if taxa_acerto >= 0.7:
                        y.append(1)  # Fácil
                    elif taxa_acerto >= 0.4:
                        y.append(2)  # Médio
                    else:
                        y.append(3)  # Difícil
            
            if len(X) < 10:
                logger.warning("Dados insuficientes para treinamento")
                return
            
            # Treinar modelo
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            self.model.fit(X_train, y_train)
            
            # Avaliar modelo
            y_pred = self.model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            
            self.is_trained = True
            logger.info(f"Modelo treinado com precisão: {accuracy:.3f}")
            
        except Exception as e:
            logger.error(f"Erro ao treinar modelo: {e}")
    
    def selecionar_proxima_questao(self, respostas_usuario: List[Dict], 
                                 questoes_respondidas: List[int]) -> Optional[Dict]:
        """
        Seleciona a próxima questão baseada no algoritmo adaptativo
        """
        try:
            if not self.question_bank:
                logger.error("Banco de questões não carregado")
                return None
            
            # Calcular nível de proficiência atual
            proficiencia_atual = self._calcular_proficiencia_atual(respostas_usuario)
            
            # Calcular confiança na estimativa
            confianca = self._calcular_confianca(respostas_usuario)
            
            # Se confiança é alta e temos questões suficientes, finalizar teste
            if confianca >= self.confidence_threshold and len(respostas_usuario) >= self.min_questions:
                return None
            
            # Se atingiu limite máximo, finalizar teste
            if len(respostas_usuario) >= self.max_questions:
                return None
            
            # Selecionar questão baseada na proficiência atual
            questao_selecionada = self._selecionar_questao_otima(
                proficiencia_atual, confianca, questoes_respondidas
            )
            
            return questao_selecionada
            
        except Exception as e:
            logger.error(f"Erro ao selecionar próxima questão: {e}")
            return None
    
    def _calcular_proficiencia_atual(self, respostas_usuario: List[Dict]) -> float:
        """
        Calcula o nível de proficiência atual do usuário
        """
        try:
            if not respostas_usuario:
                return 0.5  # Nível médio inicial
            
            # Calcular proficiência usando modelo IRT simplificado
            proficiencia = 0.5  # Valor inicial
            
            for resposta in respostas_usuario:
                questao_id = resposta.get('questao_id')
                acertou = resposta.get('acertou', False)
                tempo_resposta = resposta.get('tempo_resposta', 30)
                
                # Encontrar questão
                questao = next((q for q in self.question_bank if q['id'] == questao_id), None)
                if not questao:
                    continue
                
                # Calcular dificuldade da questão
                dificuldade = self._calcular_dificuldade_questao(questao)
                
                # Atualizar proficiência usando algoritmo adaptativo
                if acertou:
                    proficiencia += 0.1 * (1 - proficiencia) * (1 - dificuldade)
                else:
                    proficiencia -= 0.1 * proficiencia * dificuldade
                
                # Ajustar baseado no tempo de resposta
                tempo_ideal = 60  # 1 minuto por questão
                if tempo_resposta < tempo_ideal * 0.5:
                    proficiencia += 0.05  # Respondeu muito rápido (pode ser fácil)
                elif tempo_resposta > tempo_ideal * 2:
                    proficiencia -= 0.05  # Respondeu muito lento
            
            # Manter proficiência entre 0 e 1
            return max(0, min(1, proficiencia))
            
        except Exception as e:
            logger.error(f"Erro ao calcular proficiência: {e}")
            return 0.5
    
    def _calcular_confianca(self, respostas_usuario: List[Dict]) -> float:
        """
        Calcula a confiança na estimativa de proficiência
        """
        try:
            if len(respostas_usuario) < 3:
                return 0.0
            
            # Calcular variância das respostas recentes
            respostas_recentes = respostas_usuario[-10:]  # Últimas 10 respostas
            acertos = [r.get('acertou', False) for r in respostas_recentes]
            
            taxa_acerto = sum(acertos) / len(acertos)
            variância = sum((acerto - taxa_acerto) ** 2 for acerto in acertos) / len(acertos)
            
            # Confiança baseada na consistência (baixa variância = alta confiança)
            confianca = max(0, 1 - variância * 2)
            
            # Ajustar baseado no número de respostas
            fator_amostra = min(1, len(respostas_usuario) / 20)
            confianca *= fator_amostra
            
            return confianca
            
        except Exception as e:
            logger.error(f"Erro ao calcular confiança: {e}")
            return 0.0
    
    def _calcular_dificuldade_questao(self, questao: Dict) -> float:
        """
        Calcula a dificuldade de uma questão
        """
        try:
            if self.is_trained:
                # Usar modelo treinado
                caracteristicas = questao.get('caracteristicas', [])
                if caracteristicas:
                    dificuldade_predita = self.model.predict([caracteristicas])[0]
                    return (dificuldade_predita - 1) / 2  # Normalizar para 0-1
            else:
                # Usar heurística baseada no nível
                nivel = questao.get('nivel_dificuldade', 'medio')
                return {'facil': 0.2, 'medio': 0.5, 'dificil': 0.8}.get(nivel, 0.5)
            
            return 0.5
            
        except Exception as e:
            logger.error(f"Erro ao calcular dificuldade da questão: {e}")
            return 0.5
    
    def _selecionar_questao_otima(self, proficiencia: float, confianca: float, 
                                questoes_respondidas: List[int]) -> Optional[Dict]:
        """
        Seleciona a questão ótima baseada na proficiência e confiança
        """
        try:
            # Filtrar questões não respondidas
            questoes_disponiveis = [
                q for q in self.question_bank 
                if q['id'] not in questoes_respondidas
            ]
            
            if not questoes_disponiveis:
                return None
            
            # Calcular score para cada questão
            scores = []
            for questao in questoes_disponiveis:
                score = self._calcular_score_questao(questao, proficiencia, confianca)
                scores.append((score, questao))
            
            # Ordenar por score e selecionar a melhor
            scores.sort(key=lambda x: x[0], reverse=True)
            
            return scores[0][1]
            
        except Exception as e:
            logger.error(f"Erro ao selecionar questão ótima: {e}")
            return None
    
    def _calcular_score_questao(self, questao: Dict, proficiencia: float, 
                              confianca: float) -> float:
        """
        Calcula o score de uma questão para seleção
        """
        try:
            dificuldade = self._calcular_dificuldade_questao(questao)
            
            # Score baseado na proximidade da dificuldade com a proficiência
            proximidade = 1 - abs(dificuldade - proficiencia)
            
            # Ajustar baseado na confiança
            # Se confiança é baixa, preferir questões de dificuldade média
            if confianca < 0.5:
                if 0.3 <= dificuldade <= 0.7:
                    proximidade += 0.2
            
            # Ajustar baseado na disciplina (preferir disciplinas mais testadas)
            disciplina = questao.get('disciplina', '')
            if disciplina in ['português', 'matemática']:
                proximidade += 0.1
            
            # Ajustar baseado no peso da questão
            peso = questao.get('peso', 1.0)
            proximidade *= peso
            
            return proximidade
            
        except Exception as e:
            logger.error(f"Erro ao calcular score da questão: {e}")
            return 0.0
    
    def gerar_relatorio_proficiencia(self, respostas_usuario: List[Dict]) -> Dict:
        """
        Gera relatório detalhado de proficiência
        """
        try:
            if not respostas_usuario:
                return {"erro": "Nenhuma resposta disponível"}
            
            # Calcular métricas gerais
            total_questoes = len(respostas_usuario)
            acertos = sum(1 for r in respostas_usuario if r.get('acertou', False))
            taxa_acerto = acertos / total_questoes
            
            # Calcular proficiência final
            proficiencia_final = self._calcular_proficiencia_atual(respostas_usuario)
            confianca_final = self._calcular_confianca(respostas_usuario)
            
            # Análise por disciplina
            disciplinas = {}
            for resposta in respostas_usuario:
                questao_id = resposta.get('questao_id')
                questao = next((q for q in self.question_bank if q['id'] == questao_id), None)
                
                if questao:
                    disciplina = questao.get('disciplina', 'Não identificada')
                    if disciplina not in disciplinas:
                        disciplinas[disciplina] = {'acertos': 0, 'total': 0}
                    
                    disciplinas[disciplina]['total'] += 1
                    if resposta.get('acertou', False):
                        disciplinas[disciplina]['acertos'] += 1
            
            # Calcular taxa de acerto por disciplina
            for disciplina in disciplinas:
                dados = disciplinas[disciplina]
                dados['taxa_acerto'] = dados['acertos'] / dados['total']
            
            # Análise por nível de dificuldade
            niveis = {}
            for resposta in respostas_usuario:
                questao_id = resposta.get('questao_id')
                questao = next((q for q in self.question_bank if q['id'] == questao_id), None)
                
                if questao:
                    nivel = questao.get('nivel_dificuldade', 'medio')
                    if nivel not in niveis:
                        niveis[nivel] = {'acertos': 0, 'total': 0}
                    
                    niveis[nivel]['total'] += 1
                    if resposta.get('acertou', False):
                        niveis[nivel]['acertos'] += 1
            
            # Calcular taxa de acerto por nível
            for nivel in niveis:
                dados = niveis[nivel]
                dados['taxa_acerto'] = dados['acertos'] / dados['total']
            
            # Tempo médio de resposta
            tempos = [r.get('tempo_resposta', 0) for r in respostas_usuario]
            tempo_medio = sum(tempos) / len(tempos) if tempos else 0
            
            # Gerar recomendações
            recomendacoes = self._gerar_recomendacoes(disciplinas, niveis, proficiencia_final)
            
            return {
                'metadados': {
                    'data_teste': datetime.now().isoformat(),
                    'total_questoes': total_questoes,
                    'tempo_total': sum(tempos),
                    'versao_algoritmo': '1.0'
                },
                'proficiencia': {
                    'nivel_geral': proficiencia_final,
                    'confianca': confianca_final,
                    'taxa_acerto_geral': taxa_acerto,
                    'classificacao': self._classificar_proficiencia(proficiencia_final)
                },
                'analise_disciplinas': disciplinas,
                'analise_niveis': niveis,
                'tempo_resposta': {
                    'medio': tempo_medio,
                    'minimo': min(tempos) if tempos else 0,
                    'maximo': max(tempos) if tempos else 0
                },
                'recomendacoes': recomendacoes
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar relatório de proficiência: {e}")
            return {"erro": str(e)}
    
    def _classificar_proficiencia(self, proficiencia: float) -> str:
        """
        Classifica o nível de proficiência
        """
        if proficiencia >= 0.8:
            return "Avançado"
        elif proficiencia >= 0.6:
            return "Intermediário"
        elif proficiencia >= 0.4:
            return "Básico"
        else:
            return "Iniciante"
    
    def _gerar_recomendacoes(self, disciplinas: Dict, niveis: Dict, 
                           proficiencia: float) -> List[str]:
        """
        Gera recomendações baseadas na análise
        """
        recomendacoes = []
        
        # Recomendações por disciplina
        for disciplina, dados in disciplinas.items():
            if dados['taxa_acerto'] < 0.5:
                recomendacoes.append(f"Foque em {disciplina} - taxa de acerto baixa ({dados['taxa_acerto']:.1%})")
        
        # Recomendações por nível
        if 'dificil' in niveis and niveis['dificil']['taxa_acerto'] < 0.3:
            recomendacoes.append("Questões difíceis precisam de mais atenção")
        
        # Recomendações gerais
        if proficiencia < 0.4:
            recomendacoes.append("Recomendamos revisar conceitos básicos")
        elif proficiencia > 0.8:
            recomendacoes.append("Excelente desempenho! Continue praticando questões avançadas")
        
        return recomendacoes

# Exemplo de uso
if __name__ == "__main__":
    engine = AdaptiveTestingEngine()
    
    # Exemplo de questões
    questoes_exemplo = [
        {
            'id': 1,
            'enunciado': 'Qual é a capital do Brasil?',
            'opcoes': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador'],
            'gabarito': 'C',
            'disciplina': 'geografia',
            'nivel_dificuldade': 'facil'
        },
        {
            'id': 2,
            'enunciado': 'Calcule a derivada de x²',
            'opcoes': ['x', '2x', 'x²', '2x²'],
            'gabarito': 'B',
            'disciplina': 'matemática',
            'nivel_dificuldade': 'medio'
        }
    ]
    
    engine.carregar_banco_questoes(questoes_exemplo)
    
    # Exemplo de respostas
    respostas = [
        {'questao_id': 1, 'acertou': True, 'tempo_resposta': 30},
        {'questao_id': 2, 'acertou': False, 'tempo_resposta': 120}
    ]
    
    # Selecionar próxima questão
    proxima = engine.selecionar_proxima_questao(respostas, [1, 2])
    print(f"Próxima questão: {proxima}")
    
    # Gerar relatório
    relatorio = engine.gerar_relatorio_proficiencia(respostas)
    print(f"Relatório: {relatorio}")
