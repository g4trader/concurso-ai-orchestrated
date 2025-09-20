from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    simulados = relationship("Simulado", back_populates="user")
    results = relationship("SimuladoResult", back_populates="user")


class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # List of options
    correct_answer = Column(Integer, nullable=False)  # Index of correct option
    explanation = Column(Text)
    subject = Column(String, nullable=False)
    banca = Column(String, nullable=False)
    level = Column(String, nullable=False)  # basic, intermediate, advanced
    year = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    simulado_questions = relationship("SimuladoQuestion", back_populates="question")


class Simulado(Base):
    __tablename__ = "simulados"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    config = Column(JSON, nullable=False)  # Configuration used to generate
    time_limit = Column(Integer, nullable=False)  # in minutes
    total_questions = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    user = relationship("User", back_populates="simulados")
    questions = relationship("SimuladoQuestion", back_populates="simulado")
    result = relationship("SimuladoResult", back_populates="simulado", uselist=False)


class SimuladoQuestion(Base):
    __tablename__ = "simulado_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    simulado_id = Column(Integer, ForeignKey("simulados.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    order = Column(Integer, nullable=False)  # Order in the simulado
    
    # Relationships
    simulado = relationship("Simulado", back_populates="questions")
    question = relationship("Question", back_populates="simulado_questions")


class SimuladoResult(Base):
    __tablename__ = "simulado_results"
    
    id = Column(Integer, primary_key=True, index=True)
    simulado_id = Column(Integer, ForeignKey("simulados.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    answers = Column(JSON, nullable=False)  # User's answers
    score = Column(Integer, nullable=False)  # Percentage
    correct_answers = Column(Integer, nullable=False)
    time_spent = Column(Integer, nullable=False)  # in seconds
    subject_scores = Column(JSON, nullable=False)  # Scores by subject
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    simulado = relationship("Simulado", back_populates="result")
    user = relationship("User", back_populates="results")
