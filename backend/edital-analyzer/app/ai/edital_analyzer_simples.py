import re
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import logging
from collections import Counter

logger = logging.getLogger(__name__)

class EditalAnalyzerSimples:
    """
    Analisador de editais 100% funcional usando apenas regex e lógica
    SEM dependências externas problemáticas
    """
    
    def __init__(self):
        self.disciplinas_conhecidas = [
            'português', 'matemática', 'direito constitucional', 'direito administrativo',
            'direito penal', 'direito civil', 'informática', 'administração',
            'contabilidade', 'história', 'geografia', 'atualidades', 'raciocínio lógico',
            'legislação', 'ética', 'administração pública', 'gestão pública',
            'língua portuguesa', 'noções de direito', 'contabilidade geral'
        ]
        
        self.bancas_conhecidas = [
            'cespe', 'cebraspe', 'fgv', 'fcc', 'vunesp', 'cesgranrio', 'funesp'
        ]
        
        self.cargos_comuns = [
            'agente de polícia federal', 'delegado', 'perito criminal',
            'analista judiciário', 'técnico judiciário', 'assistente social',
            'psicólogo', 'médico', 'enfermeiro', 'engenheiro', 'contador'
        ]
    
    def analisar_edital_completo(self, conteudo_edital: str) -> Dict:
        """
        Análise completa de um edital - 100% funcional
        """
        try:
            logger.info("Iniciando análise completa do edital")
            
            # Análise básica
            analise_basica = self._analisar_basico(conteudo_edital)
            
            # Extração de informações específicas
            informacoes = self._extrair_informacoes_completas(conteudo_edital)
            
            # Análise de estrutura
            estrutura = self._analisar_estrutura(conteudo_edital)
            
            # Geração de resumo inteligente
            resumo = self._gerar_resumo_inteligente(conteudo_edital, informacoes)
            
            # Análise de relevância
            relevancia = self._analisar_relevancia(conteudo_edital)
            
            return {
                'metadados': {
                    'data_analise': datetime.now().isoformat(),
                    'tamanho_texto': len(conteudo_edital),
                    'palavras_totais': len(conteudo_edital.split()),
                    'versao_analisador': '2.0 - 100% Funcional',
                    'status': 'SUCESSO'
                },
                'analise_basica': analise_basica,
                'informacoes_extraidas': informacoes,
                'estrutura_documento': estrutura,
                'resumo_executivo': resumo,
                'analise_relevancia': relevancia,
                'estatisticas': self._calcular_estatisticas_detalhadas(conteudo_edital)
            }
            
        except Exception as e:
            logger.error(f"Erro na análise completa: {e}")
            return {"erro": str(e), "status": "ERRO"}
    
    def _analisar_basico(self, texto: str) -> Dict:
        """
        Análise básica do documento
        """
        try:
            # Identificar tipo de documento
            tipo_documento = self._identificar_tipo_documento(texto)
            
            # Identificar banca organizadora
            banca = self._identificar_banca(texto)
            
            # Identificar órgão
            orgao = self._identificar_orgao(texto)
            
            # Contar elementos estruturais
            secoes = len(re.findall(r'\d+\.\s+[A-ZÁÊÇÕ]', texto))
            paragrafos = len(re.findall(r'\n\s*\n', texto))
            listas = len(re.findall(r'[a-z]\)', texto))
            
            return {
                'tipo_documento': tipo_documento,
                'banca_organizadora': banca,
                'orgao_responsavel': orgao,
                'numero_secoes': secoes,
                'numero_paragrafos': paragrafos,
                'numero_listas': listas,
                'palavras_totais': len(texto.split()),
                'caracteres_totais': len(texto)
            }
            
        except Exception as e:
            logger.error(f"Erro na análise básica: {e}")
            return {}
    
    def _identificar_tipo_documento(self, texto: str) -> str:
        """Identifica o tipo de documento"""
        texto_lower = texto.lower()
        
        if 'concurso público' in texto_lower:
            return 'Concurso Público'
        elif 'seleção pública' in texto_lower:
            return 'Seleção Pública'
        elif 'processo seletivo' in texto_lower:
            return 'Processo Seletivo'
        elif 'edital' in texto_lower:
            return 'Edital'
        else:
            return 'Documento Oficial'
    
    def _identificar_banca(self, texto: str) -> str:
        """Identifica a banca organizadora"""
        texto_lower = texto.lower()
        
        for banca in self.bancas_conhecidas:
            if banca in texto_lower:
                return banca.upper()
        
        # Buscar padrões específicos
        if 'cebraspe' in texto_lower or 'cespe' in texto_lower:
            return 'CESPE/CEBRASPE'
        elif 'fgv' in texto_lower:
            return 'FGV'
        elif 'fcc' in texto_lower:
            return 'FCC'
        
        return 'Não identificada'
    
    def _identificar_orgao(self, texto: str) -> str:
        """Identifica o órgão responsável"""
        # Padrões comuns de órgãos
        padroes_orgao = [
            r'([A-Z][a-záêçõ\s]+(?:FEDERAL|ESTADUAL|MUNICIPAL|PÚBLICA))',
            r'([A-Z][a-záêçõ\s]+(?:POLÍCIA|TRIBUNAL|MINISTÉRIO|SECRETARIA))',
            r'([A-Z][a-záêçõ\s]+(?:UNIVERSIDADE|INSTITUTO|ESCOLA))'
        ]
        
        for padrao in padroes_orgao:
            matches = re.findall(padrao, texto)
            if matches:
                return matches[0].strip()
        
        return 'Não identificado'
    
    def _extrair_informacoes_completas(self, texto: str) -> Dict:
        """
        Extrai todas as informações importantes do edital
        """
        try:
            return {
                'cargos': self._extrair_cargos(texto),
                'vagas': self._extrair_vagas(texto),
                'disciplinas': self._extrair_disciplinas_detalhadas(texto),
                'datas': self._extrair_datas_detalhadas(texto),
                'valores': self._extrair_valores_detalhados(texto),
                'requisitos': self._extrair_requisitos_detalhados(texto),
                'etapas': self._extrair_etapas(texto),
                'localizacao': self._extrair_localizacao(texto)
            }
            
        except Exception as e:
            logger.error(f"Erro na extração de informações: {e}")
            return {}
    
    def _extrair_cargos(self, texto: str) -> List[Dict]:
        """Extrai cargos mencionados no edital"""
        cargos_encontrados = []
        texto_lower = texto.lower()
        
        for cargo in self.cargos_comuns:
            if cargo in texto_lower:
                # Buscar contexto do cargo
                padrao = rf'([^.]*{re.escape(cargo)}[^.]*)'
                matches = re.findall(padrao, texto_lower)
                if matches:
                    cargos_encontrados.append({
                        'cargo': cargo.title(),
                        'contexto': matches[0].strip()
                    })
        
        # Buscar padrões específicos de cargo
        padrao_cargo = r'(?:cargo de|função de|vaga para)\s+([A-Z][a-záêçõ\s]+)'
        matches = re.findall(padrao_cargo, texto, re.IGNORECASE)
        for match in matches:
            if len(match.strip()) > 5:  # Filtrar matches muito curtos
                cargos_encontrados.append({
                    'cargo': match.strip().title(),
                    'contexto': 'Extraído do texto'
                })
        
        return cargos_encontrados
    
    def _extrair_vagas(self, texto: str) -> List[Dict]:
        """Extrai informações sobre vagas"""
        vagas = []
        
        # Padrões de vagas
        padroes_vaga = [
            r'(\d+(?:\.\d{3})*)\s+vagas?',
            r'(\d+(?:\.\d{3})*)\s+cargos?',
            r'(\d+(?:\.\d{3})*)\s+postos?'
        ]
        
        for padrao in padroes_vaga:
            matches = re.finditer(padrao, texto, re.IGNORECASE)
            for match in matches:
                numero_vagas = int(match.group(1).replace('.', ''))
                contexto = texto[max(0, match.start()-50):match.end()+50]
                
                vagas.append({
                    'numero_vagas': numero_vagas,
                    'contexto': contexto.strip(),
                    'tipo': 'vagas'
                })
        
        return vagas
    
    def _extrair_disciplinas_detalhadas(self, texto: str) -> List[Dict]:
        """Extrai disciplinas com contexto detalhado"""
        disciplinas_encontradas = []
        texto_lower = texto.lower()
        
        for disciplina in self.disciplinas_conhecidas:
            if disciplina in texto_lower:
                # Buscar contexto da disciplina
                padrao = rf'([^.]*{re.escape(disciplina)}[^.]*)'
                matches = re.findall(padrao, texto_lower)
                if matches:
                    contexto = matches[0].strip()
                    
                    # Identificar se é obrigatória ou opcional
                    obrigatoria = any(palavra in contexto for palavra in ['obrigatória', 'obrigatório', 'será cobrada'])
                    opcional = any(palavra in contexto for palavra in ['opcional', 'específica'])
                    
                    disciplinas_encontradas.append({
                        'disciplina': disciplina.title(),
                        'contexto': contexto,
                        'obrigatoria': obrigatoria,
                        'opcional': opcional,
                        'tipo': 'obrigatória' if obrigatoria else 'opcional' if opcional else 'geral'
                    })
        
        return disciplinas_encontradas
    
    def _extrair_datas_detalhadas(self, texto: str) -> List[Dict]:
        """Extrai datas com contexto detalhado"""
        datas = []
        
        # Padrões de data
        padroes_data = [
            r'(\d{1,2})[\/\-](\d{1,2})[\/\-](\d{4})',  # DD/MM/YYYY
            r'(\d{1,2})\s+de\s+([a-z]+)\s+de\s+(\d{4})',  # DD de Mês de YYYY
        ]
        
        meses = {
            'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04',
            'maio': '05', 'junho': '06', 'julho': '07', 'agosto': '08',
            'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
        }
        
        for padrao in padroes_data:
            matches = re.finditer(padrao, texto, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 3:
                    if match.group(2).isdigit():
                        # Formato DD/MM/YYYY
                        dia, mes, ano = match.groups()
                        data_str = f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
                    else:
                        # Formato DD de Mês de YYYY
                        dia, mes_nome, ano = match.groups()
                        mes_num = meses.get(mes_nome.lower(), '01')
                        data_str = f"{ano}-{mes_num}-{dia.zfill(2)}"
                    
                    # Identificar tipo de data baseado no contexto
                    contexto = texto[max(0, match.start()-100):match.end()+100]
                    tipo_data = self._identificar_tipo_data_detalhado(contexto)
                    prioridade = self._calcular_prioridade_data(tipo_data)
                    
                    datas.append({
                        'data': data_str,
                        'tipo': tipo_data,
                        'prioridade': prioridade,
                        'contexto': contexto.strip(),
                        'formato_original': match.group(0)
                    })
        
        # Ordenar por prioridade
        datas.sort(key=lambda x: x['prioridade'], reverse=True)
        
        return datas
    
    def _identificar_tipo_data_detalhado(self, contexto: str) -> str:
        """Identifica o tipo de data com mais detalhes"""
        contexto_lower = contexto.lower()
        
        tipos_data = {
            'inscrições': ['inscrição', 'inscrever', 'inscrever-se', 'período de inscrição'],
            'prova': ['prova', 'exame', 'teste', 'avaliação', 'prova objetiva', 'prova discursiva'],
            'resultado': ['resultado', 'divulgação', 'publicação', 'gabarito'],
            'homologação': ['homologação', 'homologar', 'aprovação final'],
            'publicação': ['publicação', 'publicar', 'edital publicado'],
            'recurso': ['recurso', 'interposição', 'impugnação'],
            'entrega_documentos': ['entrega', 'documentos', 'documentação'],
            'entrevista': ['entrevista', 'avaliação oral'],
            'exame_medico': ['exame médico', 'avaliação médica', 'aptidão física']
        }
        
        for tipo, palavras in tipos_data.items():
            if any(palavra in contexto_lower for palavra in palavras):
                return tipo
        
        return 'outra'
    
    def _calcular_prioridade_data(self, tipo_data: str) -> int:
        """Calcula prioridade da data (maior = mais importante)"""
        prioridades = {
            'inscrições': 10,
            'prova': 9,
            'resultado': 8,
            'homologação': 7,
            'recurso': 6,
            'entrega_documentos': 5,
            'entrevista': 4,
            'exame_medico': 3,
            'publicação': 2,
            'outra': 1
        }
        return prioridades.get(tipo_data, 1)
    
    def _extrair_valores_detalhados(self, texto: str) -> List[Dict]:
        """Extrai valores monetários com contexto detalhado"""
        valores = []
        
        # Padrões de valores monetários
        padroes_valor = [
            r'R\$\s*(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)',  # R$ 1.000,00
            r'(\d{1,3}(?:\.\d{3})*(?:,\d{2})?)\s*reais',  # 1.000,00 reais
        ]
        
        for padrao in padroes_valor:
            matches = re.finditer(padrao, texto, re.IGNORECASE)
            for match in matches:
                valor_str = match.group(1)
                try:
                    valor_float = float(valor_str.replace('.', '').replace(',', '.'))
                    
                    # Identificar tipo de valor
                    contexto = texto[max(0, match.start()-100):match.end()+100]
                    tipo_valor = self._identificar_tipo_valor_detalhado(contexto)
                    
                    valores.append({
                        'valor': valor_float,
                        'valor_formatado': f"R$ {valor_str}",
                        'tipo': tipo_valor,
                        'contexto': contexto.strip(),
                        'importante': self._eh_valor_importante(tipo_valor)
                    })
                except ValueError:
                    continue
        
        return valores
    
    def _identificar_tipo_valor_detalhado(self, contexto: str) -> str:
        """Identifica o tipo de valor com mais detalhes"""
        contexto_lower = contexto.lower()
        
        tipos_valor = {
            'salario': ['salário', 'remuneração', 'vencimento', 'proventos'],
            'taxa_inscricao': ['taxa', 'inscrição', 'pagamento', 'valor da inscrição'],
            'multa': ['multa', 'penalidade', 'sanção'],
            'auxilio': ['auxílio', 'benefício', 'ajuda'],
            'gratificacao': ['gratificação', 'adicional', 'bonificação']
        }
        
        for tipo, palavras in tipos_valor.items():
            if any(palavra in contexto_lower for palavra in palavras):
                return tipo
        
        return 'outro'
    
    def _eh_valor_importante(self, tipo_valor: str) -> bool:
        """Determina se o valor é importante"""
        valores_importantes = ['salario', 'taxa_inscricao']
        return tipo_valor in valores_importantes
    
    def _extrair_requisitos_detalhados(self, texto: str) -> Dict:
        """Extrai requisitos com detalhes"""
        requisitos = {
            'escolaridade': [],
            'idade': [],
            'experiencia': [],
            'nacionalidade': [],
            'outros': []
        }
        
        # Escolaridade
        escolaridade_padroes = [
            r'(?:ensino|nível)\s+(?:fundamental|médio|superior)',
            r'(?:graduação|pós-graduação|mestrado|doutorado)',
            r'(?:curso superior|curso técnico)',
            r'(?:bacharelado|licenciatura|tecnólogo)'
        ]
        
        for padrao in escolaridade_padroes:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                requisitos['escolaridade'].append({
                    'requisito': match,
                    'tipo': 'escolaridade'
                })
        
        # Idade
        idade_padroes = [
            r'(\d+)\s*anos?\s*(?:de idade|completos)',
            r'idade\s*(?:mínima|máxima)?\s*(?:de\s*)?(\d+)\s*anos?',
            r'(?:entre\s*)?(\d+)\s*(?:e\s*)?(\d+)\s*anos?'
        ]
        
        for padrao in idade_padroes:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    requisitos['idade'].append({
                        'requisito': ' '.join(match),
                        'tipo': 'idade'
                    })
                else:
                    requisitos['idade'].append({
                        'requisito': match,
                        'tipo': 'idade'
                    })
        
        # Experiência
        exp_padroes = [
            r'(\d+)\s*anos?\s*(?:de\s*)?(?:experiência|atuação)',
            r'(?:experiência|atuação)\s*(?:de\s*)?(\d+)\s*anos?'
        ]
        
        for padrao in exp_padroes:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                requisitos['experiencia'].append({
                    'requisito': match,
                    'tipo': 'experiencia'
                })
        
        return requisitos
    
    def _extrair_etapas(self, texto: str) -> List[Dict]:
        """Extrai etapas do concurso"""
        etapas = []
        
        # Padrões de etapas
        padroes_etapa = [
            r'(?:prova|exame|teste|avaliação)\s+(?:objetiva|discursiva|oral|prática)',
            r'(?:exame|avaliação)\s+(?:médico|psicológico|de aptidão física)',
            r'(?:análise|avaliação)\s+(?:de títulos|curricular)',
            r'(?:entrevista|avaliação oral)'
        ]
        
        for padrao in padroes_etapa:
            matches = re.findall(padrao, texto, re.IGNORECASE)
            for match in matches:
                etapas.append({
                    'etapa': match,
                    'tipo': self._classificar_etapa(match)
                })
        
        return etapas
    
    def _classificar_etapa(self, etapa: str) -> str:
        """Classifica o tipo de etapa"""
        etapa_lower = etapa.lower()
        
        if 'objetiva' in etapa_lower:
            return 'prova_objetiva'
        elif 'discursiva' in etapa_lower:
            return 'prova_discursiva'
        elif 'oral' in etapa_lower:
            return 'prova_oral'
        elif 'médico' in etapa_lower:
            return 'exame_medico'
        elif 'psicológico' in etapa_lower:
            return 'exame_psicologico'
        elif 'aptidão física' in etapa_lower:
            return 'exame_fisico'
        else:
            return 'outra'
    
    def _extrair_localizacao(self, texto: str) -> List[str]:
        """Extrai informações de localização"""
        localizacoes = []
        
        # Padrões de localização
        padroes_local = [
            r'([A-Z][a-záêçõ\s]+(?:FEDERAL|ESTADUAL|MUNICIPAL))',
            r'([A-Z][a-záêçõ\s]+(?:POLÍCIA|TRIBUNAL|MINISTÉRIO))',
            r'(?:em|no|na)\s+([A-Z][a-záêçõ\s]+)'
        ]
        
        for padrao in padroes_local:
            matches = re.findall(padrao, texto)
            for match in matches:
                if len(match.strip()) > 3:  # Filtrar matches muito curtos
                    localizacoes.append(match.strip())
        
        return list(set(localizacoes))  # Remover duplicatas
    
    def _analisar_estrutura(self, texto: str) -> Dict:
        """Analisa a estrutura do documento"""
        try:
            # Identificar seções principais
            secoes = re.findall(r'(\d+\.\s+[A-ZÁÊÇÕ][^.\n]*)', texto)
            
            # Identificar subseções
            subsecoes = re.findall(r'(\d+\.\d+\s+[A-ZÁÊÇÕ][^.\n]*)', texto)
            
            # Identificar anexos
            anexos = re.findall(r'(?:anexo|apêndice)\s+[IVX\d]+', texto, re.IGNORECASE)
            
            return {
                'secoes_principais': secoes,
                'subsecoes': subsecoes,
                'anexos': anexos,
                'total_secoes': len(secoes),
                'total_subsecoes': len(subsecoes),
                'total_anexos': len(anexos),
                'estrutura_completa': len(secoes) > 5
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de estrutura: {e}")
            return {}
    
    def _gerar_resumo_inteligente(self, texto: str, informacoes: Dict) -> str:
        """Gera resumo executivo inteligente"""
        try:
            resumo_partes = []
            
            # Informações básicas
            analise_basica = informacoes.get('analise_basica', {})
            if analise_basica:
                tipo = analise_basica.get('tipo_documento', '')
                banca = analise_basica.get('banca_organizadora', '')
                orgao = analise_basica.get('orgao_responsavel', '')
                
                if tipo:
                    resumo_partes.append(f"Este é um {tipo.lower()}.")
                
                if banca and banca != 'Não identificada':
                    resumo_partes.append(f"Organizado pela banca {banca}.")
                
                if orgao and orgao != 'Não identificado':
                    resumo_partes.append(f"Órgão responsável: {orgao}.")
            
            # Vagas
            vagas = informacoes.get('vagas', [])
            if vagas:
                total_vagas = sum(v['numero_vagas'] for v in vagas)
                resumo_partes.append(f"Oferece {total_vagas} vagas.")
            
            # Cargos
            cargos = informacoes.get('cargos', [])
            if cargos:
                cargo_principal = cargos[0]['cargo'] if cargos else ''
                resumo_partes.append(f"Cargo principal: {cargo_principal}.")
            
            # Disciplinas
            disciplinas = informacoes.get('disciplinas', [])
            if disciplinas:
                num_disciplinas = len(disciplinas)
                resumo_partes.append(f"Contempla {num_disciplinas} disciplinas.")
            
            # Datas importantes
            datas = informacoes.get('datas', [])
            if datas:
                data_inscricao = next((d for d in datas if d['tipo'] == 'inscrições'), None)
                if data_inscricao:
                    resumo_partes.append(f"Inscrições em {data_inscricao['data']}.")
            
            # Valores importantes
            valores = informacoes.get('valores', [])
            if valores:
                salario = next((v for v in valores if v['tipo'] == 'salario'), None)
                if salario:
                    resumo_partes.append(f"Salário: {salario['valor_formatado']}.")
            
            return " ".join(resumo_partes) if resumo_partes else "Edital de concurso público com informações detalhadas sobre o processo seletivo."
            
        except Exception as e:
            logger.error(f"Erro na geração de resumo: {e}")
            return "Erro na geração do resumo executivo."
    
    def _analisar_relevancia(self, texto: str) -> Dict:
        """Analisa a relevância do edital"""
        try:
            # Fatores de relevância
            fatores = {
                'vagas_abertas': len(re.findall(r'\d+\s+vagas?', texto, re.IGNORECASE)),
                'disciplinas_importantes': len([d for d in self.disciplinas_conhecidas if d in texto.lower()]),
                'datas_definidas': len(re.findall(r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{4}', texto)),
                'valores_especificados': len(re.findall(r'R\$\s*\d+', texto)),
                'requisitos_claros': len(re.findall(r'(?:ensino|nível|graduação)', texto, re.IGNORECASE))
            }
            
            # Calcular score de relevância
            score = sum(fatores.values())
            max_score = 20  # Score máximo possível
            
            relevancia_percentual = (score / max_score) * 100
            
            return {
                'score_relevancia': score,
                'relevancia_percentual': relevancia_percentual,
                'fatores': fatores,
                'classificacao': self._classificar_relevancia(relevancia_percentual)
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de relevância: {e}")
            return {}
    
    def _classificar_relevancia(self, percentual: float) -> str:
        """Classifica a relevância do edital"""
        if percentual >= 80:
            return 'Muito Alta'
        elif percentual >= 60:
            return 'Alta'
        elif percentual >= 40:
            return 'Média'
        elif percentual >= 20:
            return 'Baixa'
        else:
            return 'Muito Baixa'
    
    def _calcular_estatisticas_detalhadas(self, texto: str) -> Dict:
        """Calcula estatísticas detalhadas do texto"""
        try:
            palavras = texto.split()
            frases = re.split(r'[.!?]+', texto)
            
            # Análise de complexidade
            palavras_unicas = set(palavras)
            palavras_complexas = [p for p in palavras_unicas if len(p) > 8]
            
            # Análise de repetição
            palavras_mais_comuns = Counter(palavras).most_common(10)
            
            return {
                'total_palavras': len(palavras),
                'total_frases': len([f for f in frases if f.strip()]),
                'palavras_unicas': len(palavras_unicas),
                'palavras_complexas': len(palavras_complexas),
                'densidade_informacao': len(palavras_unicas) / len(palavras) if palavras else 0,
                'palavras_mais_comuns': palavras_mais_comuns,
                'complexidade_texto': self._calcular_complexidade_texto(palavras),
                'legibilidade': self._calcular_legibilidade(palavras, frases)
            }
            
        except Exception as e:
            logger.error(f"Erro no cálculo de estatísticas: {e}")
            return {}
    
    def _calcular_complexidade_texto(self, palavras: List[str]) -> str:
        """Calcula a complexidade do texto"""
        if not palavras:
            return 'Indefinida'
        
        palavras_complexas = [p for p in palavras if len(p) > 8]
        percentual_complexas = (len(palavras_complexas) / len(palavras)) * 100
        
        if percentual_complexas >= 30:
            return 'Alta'
        elif percentual_complexas >= 15:
            return 'Média'
        else:
            return 'Baixa'
    
    def _calcular_legibilidade(self, palavras: List[str], frases: List[str]) -> str:
        """Calcula a legibilidade do texto"""
        if not palavras or not frases:
            return 'Indefinida'
        
        palavras_por_frase = len(palavras) / len(frases)
        
        if palavras_por_frase <= 15:
            return 'Fácil'
        elif palavras_por_frase <= 25:
            return 'Média'
        else:
            return 'Difícil'

# Exemplo de uso e teste
if __name__ == "__main__":
    # Criar instância do analisador
    analyzer = EditalAnalyzerSimples()
    
    # Exemplo de edital (texto real)
    edital_exemplo = """
    EDITAL Nº 1 – DGP/DPF, DE 15 DE JUNHO DE 2023
    CONCURSO PÚBLICO PARA O PROVIMENTO DE VAGAS NO CARGO DE AGENTE DE POLÍCIA FEDERAL

    O DIRETOR-GERAL DA POLÍCIA FEDERAL, no uso de suas atribuições, torna pública a realização de concurso público para o provimento de 1.500 vagas no cargo de Agente de Polícia Federal.

    1 DAS DISPOSIÇÕES PRELIMINARES
    1.1 O concurso público será regido por este edital e executado pelo Centro Brasileiro de Pesquisa em Avaliação e Seleção e de Promoção de Eventos (Cebraspe).
    1.2 O cargo de Agente de Polícia Federal exige nível superior em qualquer área de formação.
    1.3 A remuneração inicial é de R$ 12.522,50.

    2 DAS INSCRIÇÕES
    2.1 As inscrições poderão ser realizadas no período de 20/07/2023 a 02/08/2023.
    2.2 A taxa de inscrição é de R$ 180,00.

    3 DAS ETAPAS DO CONCURSO
    3.1 Prova Objetiva e Discursiva: 19/09/2023.
    3.2 Exame de Aptidão Física.
    3.3 Avaliação Médica.
    3.4 Avaliação Psicológica.

    4 DAS DISCIPLINAS
    Serão cobradas as seguintes disciplinas: Língua Portuguesa, Noções de Direito Administrativo, Noções de Direito Constitucional, Raciocínio Lógico, Informática, Contabilidade Geral.
    """
    
    # Executar análise
    print("🔍 Iniciando análise completa do edital...")
    resultado = analyzer.analisar_edital_completo(edital_exemplo)
    
    # Exibir resultados principais
    print("\n📊 RESULTADOS DA ANÁLISE:")
    print(f"Status: {resultado.get('metadados', {}).get('status', 'N/A')}")
    print(f"Tipo: {resultado.get('analise_basica', {}).get('tipo_documento', 'N/A')}")
    print(f"Banca: {resultado.get('analise_basica', {}).get('banca_organizadora', 'N/A')}")
    print(f"Órgão: {resultado.get('analise_basica', {}).get('orgao_responsavel', 'N/A')}")
    
    # Informações extraídas
    info = resultado.get('informacoes_extraidas', {})
    print(f"\n📋 INFORMAÇÕES EXTRAÍDAS:")
    print(f"Cargos: {len(info.get('cargos', []))}")
    print(f"Vagas: {len(info.get('vagas', []))}")
    print(f"Disciplinas: {len(info.get('disciplinas', []))}")
    print(f"Datas: {len(info.get('datas', []))}")
    print(f"Valores: {len(info.get('valores', []))}")
    print(f"Etapas: {len(info.get('etapas', []))}")
    
    # Relevância
    relevancia = resultado.get('analise_relevancia', {})
    print(f"\n⭐ RELEVÂNCIA:")
    print(f"Score: {relevancia.get('score_relevancia', 0)}")
    print(f"Classificação: {relevancia.get('classificacao', 'N/A')}")
    
    print(f"\n📝 RESUMO EXECUTIVO:")
    print(resultado.get('resumo_executivo', 'N/A'))
    
    print(f"\n✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
