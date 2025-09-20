from pydantic import BaseModel, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime


# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# Question schemas
class QuestionBase(BaseModel):
    text: str
    options: List[str]
    correct_answer: int
    explanation: Optional[str] = None
    subject: str
    banca: str
    level: str
    year: Optional[int] = None


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Simulado schemas
class SimuladoConfig(BaseModel):
    banca: str
    subjects: List[str]
    num_questions: int
    time_limit: int
    level: str


class SimuladoBase(BaseModel):
    title: str
    config: SimuladoConfig
    time_limit: int
    total_questions: int


class SimuladoCreate(SimuladoBase):
    pass


class Simulado(SimuladoBase):
    id: int
    user_id: int
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SimuladoWithQuestions(Simulado):
    questions: List[Question]


# Simulado Result schemas
class SimuladoResultBase(BaseModel):
    answers: Dict[str, int]  # question_id -> answer_index
    time_spent: int
    subject_scores: Dict[str, Dict[str, int]]  # subject -> {correct, total}


class SimuladoResultCreate(SimuladoResultBase):
    simulado_id: int


class SimuladoResult(SimuladoResultBase):
    id: int
    simulado_id: int
    user_id: int
    score: int
    correct_answers: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Dashboard schemas
class DashboardStats(BaseModel):
    total_simulados: int
    total_questions_answered: int
    average_score: float
    best_score: int
    time_spent_total: int
    subjects_performance: Dict[str, float]


# API Response schemas
class MessageResponse(BaseModel):
    message: str


class ErrorResponse(BaseModel):
    detail: str
