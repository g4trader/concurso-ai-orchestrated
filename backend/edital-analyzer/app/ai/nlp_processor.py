import openai
import spacy
from transformers import pipeline
import re
from typing import Dict, List, Optional, Any
import logging
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class NLPProcessor:
    """
    Processador de linguagem natural para análise de editais
    """
    
    def __init__(self):
        # Configurar OpenAI
        openai.api_key = "sua-chave-openai-aqui"  # TODO: Mover para variável de ambiente
        
        # Carregar modelo spaCy para português
        try:
            self.nlp = spacy.load("pt_core_news_sm")
        except OSError:
            logger.warning("Modelo spaCy não encontrado. Instalando...")
            # Em produção, instalar com: python -m spacy download pt_core_news_sm
            self.nlp = None
        
        # Pipeline de análise de sentimento
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
            return_all_scores=True
        )
        
        # Padrões regex para extração de informações
        self.patterns = {
            'data': [
                r'(\d{1,2})/(\d{1,2})/(\d{4})',
                r'(\d{1,2}) de (\w+) de (\d{4})',
                r'(\d{4})-(\d{1,2})-(\d{1,2})'
            ],
            'valor': [
                r'R\$\s*([\d.,]+)',
                r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',
                r'valor.*?(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)'
            ],
            'vagas': [
                r'(\d+)\s*vagas?',
                r'(\d+)\s*cargos?',
                r'(\d+)\s*oportunidades?'
            ],
            'escolaridade': [
                r'(ensino médio|superior|pós-graduação|mestrado|doutorado)',
                r'(fundamental|médio|superior)',
                r'(graduação|especialização|mestrado|doutorado)'
            ]
        }
    
    def analisar_edital_completo(self, conteudo: str, url: str = None) -> Dict[str, Any]:
        """
        Analisa um edital completo e extrai informações estruturadas
        """
        try:
            logger.info("Iniciando análise completa do edital")
            
            # Limpar e preparar conteúdo
            conteudo_limpo = self._limpar_conteudo(conteudo)
            
            # Análise com IA
            analise_ia = self._analisar_com_ia(conteudo_limpo)
            
            # Análise com NLP
            analise_nlp = self._analisar_com_nlp(conteudo_limpo)
            
            # Extração de padrões
            padroes_extraidos = self._extrair_padroes(conteudo_limpo)
            
            # Análise de requisitos
            requisitos = self._extrair_requisitos(conteudo_limpo)
            
            # Análise de disciplinas
            disciplinas = self._extrair_disciplinas(conteudo_limpo)
            
            # Análise de cronograma
            cronograma = self._extrair_cronograma(conteudo_limpo)
            
            # Compilar resultado final
            resultado = {
                'metadados': {
                    'url': url,
                    'data_analise': datetime.now().isoformat(),
                    'tamanho_conteudo': len(conteudo),
                    'versao_analise': '1.0'
                },
                'analise_ia': analise_ia,
                'analise_nlp': analise_nlp,
                'padroes_extraidos': padroes_extraidos,
                'requisitos': requisitos,
                'disciplinas': disciplinas,
                'cronograma': cronograma,
                'resumo_executivo': self._gerar_resumo_executivo(
                    analise_ia, analise_nlp, padroes_extraidos
                )
            }
            
            logger.info("Análise completa finalizada")
            return resultado
            
        except Exception as e:
            logger.error(f"Erro na análise do edital: {e}")
            return {'erro': str(e)}
    
    def _limpar_conteudo(self, conteudo: str) -> str:
        """
        Limpa e normaliza o conteúdo do edital
        """
        # Remover caracteres especiais e normalizar espaços
        conteudo = re.sub(r'\s+', ' ', conteudo)
        conteudo = re.sub(r'[^\w\s.,;:!?()\-/]', '', conteudo)
        
        # Remover quebras de linha excessivas
        conteudo = re.sub(r'\n+', '\n', conteudo)
        
        return conteudo.strip()
    
    def _analisar_com_ia(self, conteudo: str) -> Dict[str, Any]:
        """
        Analisa o conteúdo usando IA (OpenAI GPT)
        """
        try:
            prompt = f"""
            Analise o seguinte edital de concurso público e extraia as informações mais importantes:
            
            {conteudo[:4000]}  # Limitar tamanho para evitar token limit
            
            Por favor, extraia e organize as seguintes informações:
            1. Título do concurso
            2. Órgão responsável
            3. Banca organizadora
            4. Número de vagas
            5. Requisitos básicos
            6. Disciplinas da prova
            7. Cronograma principal
            8. Valor da remuneração
            9. Nível de escolaridade exigido
            10. Observações importantes
            
            Responda em formato JSON estruturado.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é um especialista em análise de editais de concursos públicos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1500,
                temperature=0.3
            )
            
            resultado = response.choices[0].message.content
            
            # Tentar parsear JSON
            try:
                return json.loads(resultado)
            except json.JSONDecodeError:
                return {'texto_bruto': resultado}
                
        except Exception as e:
            logger.error(f"Erro na análise com IA: {e}")
            return {'erro': str(e)}
    
    def _analisar_com_nlp(self, conteudo: str) -> Dict[str, Any]:
        """
        Analisa o conteúdo usando NLP (spaCy)
        """
        try:
            if not self.nlp:
                return {'erro': 'Modelo spaCy não disponível'}
            
            doc = self.nlp(conteudo)
            
            # Extrair entidades nomeadas
            entidades = []
            for ent in doc.ents:
                entidades.append({
                    'texto': ent.text,
                    'label': ent.label_,
                    'inicio': ent.start_char,
                    'fim': ent.end_char
                })
            
            # Extrair substantivos importantes
            substantivos = [token.lemma_ for token in doc 
                          if token.pos_ == 'NOUN' and len(token.text) > 3]
            
            # Análise de sentimento
            sentimentos = self.sentiment_analyzer(conteudo[:512])  # Limitar tamanho
            
            # Extrair frases importantes
            frases_importantes = []
            for sent in doc.sents:
                if len(sent.text) > 20 and any(
                    palavra in sent.text.lower() 
                    for palavra in ['concurso', 'vaga', 'prova', 'edital', 'inscrição']
                ):
                    frases_importantes.append(sent.text.strip())
            
            return {
                'entidades': entidades,
                'substantivos_importantes': list(set(substantivos))[:20],
                'sentimentos': sentimentos,
                'frases_importantes': frases_importantes[:10],
                'estatisticas': {
                    'total_palavras': len(doc),
                    'total_sentencas': len(list(doc.sents)),
                    'total_entidades': len(entidades)
                }
            }
            
        except Exception as e:
            logger.error(f"Erro na análise NLP: {e}")
            return {'erro': str(e)}
    
    def _extrair_padroes(self, conteudo: str) -> Dict[str, List[str]]:
        """
        Extrai padrões específicos do conteúdo
        """
        padroes_encontrados = {}
        
        for tipo, padroes in self.patterns.items():
            padroes_encontrados[tipo] = []
            
            for padrao in padroes:
                matches = re.findall(padrao, conteudo, re.IGNORECASE)
                padroes_encontrados[tipo].extend(matches)
        
        # Remover duplicatas
        for tipo in padroes_encontrados:
            padroes_encontrados[tipo] = list(set(padroes_encontrados[tipo]))
        
        return padroes_encontrados
    
    def _extrair_requisitos(self, conteudo: str) -> List[Dict[str, Any]]:
        """
        Extrai requisitos do edital
        """
        requisitos = []
        
        # Padrões para requisitos
        padroes_requisitos = [
            r'(idade.*?(\d+).*?anos)',
            r'(escolaridade.*?(ensino médio|superior|pós-graduação))',
            r'(experiência.*?(\d+).*?anos)',
            r'(curso.*?(técnico|superior|pós-graduação))',
            r'(certificação.*?(\w+))',
            r'(habilitação.*?(\w+))'
        ]
        
        for padrao in padroes_requisitos:
            matches = re.finditer(padrao, conteudo, re.IGNORECASE)
            for match in matches:
                requisitos.append({
                    'texto_completo': match.group(0),
                    'tipo': self._classificar_requisito(match.group(0)),
                    'valor': match.group(1) if len(match.groups()) > 1 else None,
                    'posicao': match.start()
                })
        
        return requisitos
    
    def _extrair_disciplinas(self, conteudo: str) -> List[Dict[str, Any]]:
        """
        Extrai disciplinas da prova
        """
        disciplinas = []
        
        # Lista de disciplinas comuns
        disciplinas_comuns = [
            'português', 'matemática', 'raciocínio lógico', 'informática',
            'direito constitucional', 'direito administrativo', 'direito penal',
            'direito civil', 'direito processual', 'administração pública',
            'contabilidade', 'economia', 'história', 'geografia', 'atualidades'
        ]
        
        for disciplina in disciplinas_comuns:
            padrao = rf'({disciplina}.*?(?:\d+.*?questões?|\d+.*?pontos?|\d+.*?peso))'
            matches = re.finditer(padrao, conteudo, re.IGNORECASE)
            
            for match in matches:
                disciplinas.append({
                    'nome': disciplina.title(),
                    'texto_completo': match.group(0),
                    'posicao': match.start()
                })
        
        return disciplinas
    
    def _extrair_cronograma(self, conteudo: str) -> List[Dict[str, Any]]:
        """
        Extrai cronograma do edital
        """
        cronograma = []
        
        # Padrões para datas importantes
        padroes_cronograma = [
            r'(inscrições?.*?(\d{1,2}/\d{1,2}/\d{4}))',
            r'(prova.*?(\d{1,2}/\d{1,2}/\d{4}))',
            r'(resultado.*?(\d{1,2}/\d{1,2}/\d{4}))',
            r'(homologação.*?(\d{1,2}/\d{1,2}/\d{4}))',
            r'(posse.*?(\d{1,2}/\d{1,2}/\d{4}))'
        ]
        
        for padrao in padroes_cronograma:
            matches = re.finditer(padrao, conteudo, re.IGNORECASE)
            for match in matches:
                cronograma.append({
                    'evento': match.group(1).split()[0].title(),
                    'data': match.group(2),
                    'texto_completo': match.group(0),
                    'posicao': match.start()
                })
        
        return cronograma
    
    def _classificar_requisito(self, texto: str) -> str:
        """
        Classifica o tipo de requisito
        """
        texto_lower = texto.lower()
        
        if 'idade' in texto_lower:
            return 'idade'
        elif 'escolaridade' in texto_lower or 'ensino' in texto_lower:
            return 'escolaridade'
        elif 'experiência' in texto_lower or 'anos' in texto_lower:
            return 'experiencia'
        elif 'curso' in texto_lower:
            return 'curso'
        elif 'certificação' in texto_lower:
            return 'certificacao'
        else:
            return 'outro'
    
    def _gerar_resumo_executivo(self, analise_ia: Dict, analise_nlp: Dict, 
                               padroes: Dict) -> Dict[str, Any]:
        """
        Gera um resumo executivo da análise
        """
        resumo = {
            'pontos_chave': [],
            'alertas': [],
            'recomendacoes': []
        }
        
        # Extrair pontos chave da análise de IA
        if 'texto_bruto' in analise_ia:
            resumo['pontos_chave'].append("Análise de IA disponível")
        
        # Verificar se há datas importantes
        if padroes.get('data'):
            resumo['pontos_chave'].append(f"Encontradas {len(padroes['data'])} datas importantes")
        
        # Verificar se há informações sobre vagas
        if padroes.get('vagas'):
            resumo['pontos_chave'].append(f"Vagas identificadas: {padroes['vagas']}")
        
        # Verificar se há informações sobre remuneração
        if padroes.get('valor'):
            resumo['pontos_chave'].append(f"Valores identificados: {padroes['valor']}")
        
        # Gerar alertas
        if not padroes.get('data'):
            resumo['alertas'].append("Nenhuma data importante identificada")
        
        if not padroes.get('vagas'):
            resumo['alertas'].append("Número de vagas não identificado")
        
        # Gerar recomendações
        resumo['recomendacoes'].append("Revisar manualmente as informações extraídas")
        resumo['recomendacoes'].append("Verificar cronograma completo no edital original")
        
        return resumo

# Exemplo de uso
if __name__ == "__main__":
    processor = NLPProcessor()
    
    # Exemplo de análise
    conteudo_exemplo = """
    EDITAL DE CONCURSO PÚBLICO Nº 001/2024
    
    A FUNDAÇÃO CESPE/CEBRASPE torna público que realizará concurso público para provimento de vagas no cargo de Analista Judiciário.
    
    VAGAS: 50 vagas
    REMUNERAÇÃO: R$ 8.000,00
    ESCOLARIDADE: Ensino Superior
    
    CRONOGRAMA:
    - Inscrições: 01/02/2024 a 15/02/2024
    - Prova: 15/03/2024
    - Resultado: 30/03/2024
    
    DISCIPLINAS:
    - Português: 20 questões
    - Direito Constitucional: 15 questões
    - Direito Administrativo: 15 questões
    """
    
    resultado = processor.analisar_edital_completo(conteudo_exemplo)
    print(json.dumps(resultado, indent=2, ensure_ascii=False))
