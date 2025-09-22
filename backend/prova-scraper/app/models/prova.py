from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, Dict, Any

Base = declarative_base()

class Banca(Base):
    __tablename__ = "bancas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    sigla = Column(String(10), nullable=False, unique=True)
    url_base = Column(Text)
    ativa = Column(Boolean, default=True)
    configuracao_scraping = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    provas = relationship("Prova", back_populates="banca")

class Prova(Base):
    __tablename__ = "provas"
    
    id = Column(Integer, primary_key=True, index=True)
    banca_id = Column(Integer, ForeignKey("bancas.id"), nullable=False)
    concurso_id = Column(Integer, ForeignKey("concursos.id"), nullable=True)
    titulo = Column(String(500), nullable=False)
    ano = Column(Integer)
    cargo = Column(String(255))
    nivel = Column(String(50))  # fundamental, medio, superior
    url_original = Column(Text, nullable=False)
    arquivo_url = Column(Text)
    arquivo_local = Column(String(500))
    status_processamento = Column(String(50), default="pendente")  # pendente, processando, processado, erro
    hash_conteudo = Column(String(64))
    metadados = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    banca = relationship("Banca", back_populates="provas")
    questoes = relationship("Questao", back_populates="prova")

class Questao(Base):
    __tablename__ = "questoes"
    
    id = Column(Integer, primary_key=True, index=True)
    prova_id = Column(Integer, ForeignKey("provas.id"), nullable=False)
    numero = Column(Integer, nullable=False)
    enunciado = Column(Text, nullable=False)
    opcoes = Column(JSON)  # Lista de opções A, B, C, D, E
    gabarito = Column(String(1))  # A, B, C, D, E
    disciplina = Column(String(100))
    subdisciplina = Column(String(100))
    nivel_dificuldade = Column(String(20))  # facil, medio, dificil
    peso = Column(Float, default=1.0)
    explicacao = Column(Text)
    fonte = Column(String(255))
    ano_original = Column(Integer)
    banca_original = Column(String(100))
    tags = Column(JSON)  # Tags para categorização
    metadados = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    prova = relationship("Prova", back_populates="questoes")

class Disciplina(Base):
    __tablename__ = "disciplinas"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False, unique=True)
    descricao = Column(Text)
    categoria = Column(String(50))  # exatas, humanas, biologicas
    ativa = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    subdisciplinas = relationship("Subdisciplina", back_populates="disciplina")

class Subdisciplina(Base):
    __tablename__ = "subdisciplinas"
    
    id = Column(Integer, primary_key=True, index=True)
    disciplina_id = Column(Integer, ForeignKey("disciplinas.id"), nullable=False)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text)
    ativa = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    disciplina = relationship("Disciplina", back_populates="subdisciplinas")

class Gabarito(Base):
    __tablename__ = "gabaritos"
    
    id = Column(Integer, primary_key=True, index=True)
    prova_id = Column(Integer, ForeignKey("provas.id"), nullable=False)
    versao = Column(String(10), default="1.0")
    gabarito_oficial = Column(JSON)  # {1: "A", 2: "B", ...}
    gabarito_alternativo = Column(JSON)  # Para casos de anulação
    status = Column(String(20), default="oficial")  # oficial, alternativo, anulado
    fonte = Column(String(255))
    data_publicacao = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    prova = relationship("Prova")

class ProcessamentoProva(Base):
    __tablename__ = "processamento_provas"
    
    id = Column(Integer, primary_key=True, index=True)
    prova_id = Column(Integer, ForeignKey("provas.id"), nullable=False)
    status = Column(String(50), nullable=False)  # iniciado, processando, concluido, erro
    progresso = Column(Integer, default=0)  # 0-100
    questoes_processadas = Column(Integer, default=0)
    questoes_total = Column(Integer, default=0)
    erros = Column(JSON)
    tempo_processamento = Column(Integer)  # em segundos
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    prova = relationship("Prova")

class QualidadeQuestao(Base):
    __tablename__ = "qualidade_questoes"
    
    id = Column(Integer, primary_key=True, index=True)
    questao_id = Column(Integer, ForeignKey("questoes.id"), nullable=False)
    score_qualidade = Column(Float)  # 0-1
    criterios_avaliacao = Column(JSON)  # {clareza: 0.8, relevancia: 0.9, ...}
    problemas_identificados = Column(JSON)  # Lista de problemas
    sugestoes_melhoria = Column(JSON)  # Lista de sugestões
    aprovada = Column(Boolean, default=False)
    revisada_por = Column(String(100))  # Sistema ou usuário
    data_avaliacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    questao = relationship("Questao")

class EstatisticaProva(Base):
    __tablename__ = "estatisticas_provas"
    
    id = Column(Integer, primary_key=True, index=True)
    prova_id = Column(Integer, ForeignKey("provas.id"), nullable=False)
    total_questoes = Column(Integer)
    questoes_por_disciplina = Column(JSON)
    nivel_dificuldade_medio = Column(Float)
    tempo_medio_resolucao = Column(Integer)  # em minutos
    taxa_acerto_historica = Column(Float)  # 0-1
    questoes_mais_dificeis = Column(JSON)  # IDs das questões mais difíceis
    questoes_mais_faceis = Column(JSON)  # IDs das questões mais fáceis
    analise_tendencias = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    prova = relationship("Prova")

class ScrapingProvaLog(Base):
    __tablename__ = "scraping_prova_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    banca = Column(String(100), nullable=False)
    url = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)  # sucesso, erro, timeout
    provas_encontradas = Column(Integer, default=0)
    questoes_extraidas = Column(Integer, default=0)
    erro_detalhes = Column(Text)
    tempo_execucao = Column(Integer)  # em segundos
    metadados = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
