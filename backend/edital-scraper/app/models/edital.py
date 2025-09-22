from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Optional, Dict, Any

Base = declarative_base()

class Concurso(Base):
    __tablename__ = "concursos"
    
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    orgao = Column(String(255), nullable=False)
    banca_organizadora = Column(String(100), nullable=False)
    data_publicacao = Column(DateTime)
    data_inscricao_inicio = Column(DateTime)
    data_inscricao_fim = Column(DateTime)
    data_prova = Column(DateTime)
    vagas = Column(Integer)
    salario_base = Column(String(100))
    nivel_escolaridade = Column(String(100))
    status = Column(String(50), default="ativo")  # ativo, encerrado, suspenso
    url_edital = Column(Text)
    url_inscricao = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    editais = relationship("Edital", back_populates="concurso")
    cargos = relationship("Cargo", back_populates="concurso")

class Edital(Base):
    __tablename__ = "editais"
    
    id = Column(Integer, primary_key=True, index=True)
    concurso_id = Column(Integer, ForeignKey("concursos.id"), nullable=False)
    numero = Column(String(50), nullable=False)
    titulo = Column(String(500), nullable=False)
    conteudo_completo = Column(Text)
    conteudo_extraido = Column(JSON)  # Estrutura extraída com IA
    data_publicacao = Column(DateTime)
    data_retificacao = Column(DateTime)
    url_original = Column(Text, nullable=False)
    arquivo_pdf_url = Column(Text)
    arquivo_pdf_local = Column(String(500))
    status_processamento = Column(String(50), default="pendente")  # pendente, processando, processado, erro
    hash_conteudo = Column(String(64))  # Para detectar mudanças
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    concurso = relationship("Concurso", back_populates="editais")
    requisitos = relationship("Requisito", back_populates="edital")
    disciplinas = relationship("DisciplinaEdital", back_populates="edital")

class Cargo(Base):
    __tablename__ = "cargos"
    
    id = Column(Integer, primary_key=True, index=True)
    concurso_id = Column(Integer, ForeignKey("concursos.id"), nullable=False)
    codigo = Column(String(20))
    nome = Column(String(255), nullable=False)
    descricao = Column(Text)
    vagas = Column(Integer)
    salario = Column(String(100))
    carga_horaria = Column(String(50))
    requisitos_especificos = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    concurso = relationship("Concurso", back_populates="cargos")

class Requisito(Base):
    __tablename__ = "requisitos"
    
    id = Column(Integer, primary_key=True, index=True)
    edital_id = Column(Integer, ForeignKey("editais.id"), nullable=False)
    tipo = Column(String(50), nullable=False)  # idade, escolaridade, experiencia, etc.
    descricao = Column(Text, nullable=False)
    obrigatorio = Column(Boolean, default=True)
    detalhes = Column(JSON)  # Informações estruturadas
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    edital = relationship("Edital", back_populates="requisitos")

class DisciplinaEdital(Base):
    __tablename__ = "disciplinas_edital"
    
    id = Column(Integer, primary_key=True, index=True)
    edital_id = Column(Integer, ForeignKey("editais.id"), nullable=False)
    nome = Column(String(255), nullable=False)
    peso = Column(Integer)  # Peso da disciplina na prova
    numero_questoes = Column(Integer)
    tempo_prova = Column(Integer)  # em minutos
    conteudo_programatico = Column(Text)
    bibliografia = Column(Text)
    observacoes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    edital = relationship("Edital", back_populates="disciplinas")

class ScrapingLog(Base):
    __tablename__ = "scraping_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    fonte = Column(String(100), nullable=False)  # CESPE, FGV, etc.
    url = Column(Text, nullable=False)
    status = Column(String(50), nullable=False)  # sucesso, erro, timeout
    conteudo_encontrado = Column(JSON)
    erro_detalhes = Column(Text)
    tempo_execucao = Column(Integer)  # em segundos
    created_at = Column(DateTime, default=datetime.utcnow)

class ConfiguracaoScraping(Base):
    __tablename__ = "configuracoes_scraping"
    
    id = Column(Integer, primary_key=True, index=True)
    fonte = Column(String(100), nullable=False, unique=True)
    url_base = Column(Text, nullable=False)
    seletores = Column(JSON)  # Seletores CSS/XPath
    intervalo_busca = Column(Integer, default=3600)  # em segundos
    ativo = Column(Boolean, default=True)
    ultima_busca = Column(DateTime)
    proxima_busca = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
