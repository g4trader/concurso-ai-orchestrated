#!/usr/bin/env python3
"""
Script para inicializar o banco de dados com dados reais
"""

from sqlalchemy.orm import Session
from app.database import engine, SessionLocal
from app.models import Base, Question
from app.crud import create_question
from app.schemas import QuestionCreate
import random

# Create all tables
Base.metadata.create_all(bind=engine)

# Sample questions data
SAMPLE_QUESTIONS = [
    {
        "text": "A respeito dos direitos fundamentais, assinale a opção correta.",
        "options": [
            "Os direitos fundamentais são absolutos e não admitem restrições.",
            "Os direitos fundamentais podem ser restringidos por lei, desde que respeitados os princípios da proporcionalidade e razoabilidade.",
            "Os direitos fundamentais só podem ser restringidos em caso de estado de sítio.",
            "Os direitos fundamentais não se aplicam às relações privadas."
        ],
        "correct_answer": 1,
        "explanation": "Os direitos fundamentais podem ser restringidos por lei, desde que respeitados os princípios da proporcionalidade e razoabilidade.",
        "subject": "Direito Constitucional",
        "banca": "CESPE",
        "level": "intermediario",
        "year": 2023
    },
    {
        "text": "Sobre o controle de constitucionalidade no Brasil, é correto afirmar:",
        "options": [
            "O controle de constitucionalidade é exercido apenas pelo Supremo Tribunal Federal.",
            "O controle de constitucionalidade pode ser exercido por qualquer juiz ou tribunal.",
            "O controle de constitucionalidade é exercido apenas pelo Poder Legislativo.",
            "O controle de constitucionalidade não existe no ordenamento jurídico brasileiro."
        ],
        "correct_answer": 1,
        "explanation": "O controle de constitucionalidade pode ser exercido por qualquer juiz ou tribunal, sendo o STF o guardião da Constituição.",
        "subject": "Direito Constitucional",
        "banca": "CESPE",
        "level": "intermediario",
        "year": 2023
    },
    {
        "text": "A respeito do Poder Judiciário, assinale a opção correta.",
        "options": [
            "O Poder Judiciário é composto apenas pelo Supremo Tribunal Federal.",
            "O Poder Judiciário é composto por tribunais e juízes, sendo o STF o órgão de cúpula.",
            "O Poder Judiciário não tem autonomia administrativa.",
            "O Poder Judiciário é subordinado ao Poder Executivo."
        ],
        "correct_answer": 1,
        "explanation": "O Poder Judiciário é composto por tribunais e juízes, sendo o STF o órgão de cúpula do sistema judiciário.",
        "subject": "Direito Constitucional",
        "banca": "CESPE",
        "level": "intermediario",
        "year": 2023
    },
    {
        "text": "Sobre os princípios fundamentais da República Federativa do Brasil, é correto afirmar:",
        "options": [
            "A República Federativa do Brasil é formada pela união indissolúvel dos Estados e Municípios.",
            "A República Federativa do Brasil é formada pela união indissolúvel dos Estados, Municípios e Distrito Federal.",
            "A República Federativa do Brasil é formada pela união dos Estados, que podem se separar.",
            "A República Federativa do Brasil não é uma federação."
        ],
        "correct_answer": 1,
        "explanation": "A República Federativa do Brasil é formada pela união indissolúvel dos Estados, Municípios e Distrito Federal.",
        "subject": "Direito Constitucional",
        "banca": "CESPE",
        "level": "intermediario",
        "year": 2023
    },
    {
        "text": "A respeito da organização do Estado, assinale a opção correta.",
        "options": [
            "O Brasil é um Estado unitário.",
            "O Brasil é uma federação com autonomia dos entes federativos.",
            "O Brasil é uma confederação.",
            "O Brasil não tem forma de Estado definida."
        ],
        "correct_answer": 1,
        "explanation": "O Brasil é uma federação com autonomia dos entes federativos (União, Estados, Municípios e Distrito Federal).",
        "subject": "Direito Constitucional",
        "banca": "CESPE",
        "level": "intermediario",
        "year": 2023
    },
    # Direito Administrativo
    {
        "text": "Sobre os princípios da Administração Pública, é correto afirmar:",
        "options": [
            "A legalidade é o princípio que exige que a administração atue conforme a lei.",
            "A legalidade permite que a administração atue livremente, sem limitações legais.",
            "A legalidade se aplica apenas aos atos administrativos discricionários.",
            "A legalidade não se aplica aos atos administrativos."
        ],
        "correct_answer": 0,
        "explanation": "A legalidade é o princípio fundamental que exige que a administração atue conforme a lei.",
        "subject": "Direito Administrativo",
        "banca": "CESPE",
        "level": "intermediario",
        "year": 2023
    },
    {
        "text": "Sobre o processo administrativo, assinale a opção correta:",
        "options": [
            "O processo administrativo não precisa seguir princípios constitucionais.",
            "O processo administrativo deve observar os princípios da legalidade, finalidade, motivação, razoabilidade e proporcionalidade.",
            "O processo administrativo é dispensável em todos os casos.",
            "O processo administrativo não admite recursos."
        ],
        "correct_answer": 1,
        "explanation": "O processo administrativo deve observar os princípios constitucionais, especialmente os da legalidade, finalidade, motivação, razoabilidade e proporcionalidade.",
        "subject": "Direito Administrativo",
        "banca": "CESPE",
        "level": "intermediario",
        "year": 2023
    },
    # Português
    {
        "text": "Assinale a alternativa em que a concordância verbal está correta:",
        "options": [
            "Haviam muitos problemas na empresa.",
            "Havia muitos problemas na empresa.",
            "Haviam muitos problema na empresa.",
            "Havia muitos problema na empresa."
        ],
        "correct_answer": 1,
        "explanation": "O verbo 'haver' no sentido de 'existir' é impessoal, devendo ser usado sempre na 3ª pessoa do singular.",
        "subject": "Português",
        "banca": "CESPE",
        "level": "basico",
        "year": 2023
    },
    {
        "text": "Assinale a alternativa em que o uso da crase está correto:",
        "options": [
            "Vou à escola todos os dias.",
            "Vou a escola todos os dias.",
            "Vou à escola todos os dias.",
            "Vou a escola todos os dias."
        ],
        "correct_answer": 0,
        "explanation": "A crase é obrigatória quando há a preposição 'a' + artigo 'a' (à escola).",
        "subject": "Português",
        "banca": "CESPE",
        "level": "basico",
        "year": 2023
    },
    # Raciocínio Lógico
    {
        "text": "Se todos os gatos são mamíferos e todos os mamíferos são vertebrados, então:",
        "options": [
            "Todos os gatos são vertebrados.",
            "Alguns gatos são vertebrados.",
            "Nenhum gato é vertebrado.",
            "Não é possível concluir."
        ],
        "correct_answer": 0,
        "explanation": "Se todos os gatos são mamíferos e todos os mamíferos são vertebrados, então todos os gatos são vertebrados (silogismo válido).",
        "subject": "Raciocínio Lógico",
        "banca": "CESPE",
        "level": "intermediario",
        "year": 2023
    }
]

def init_database():
    """Initialize database with sample data"""
    db = SessionLocal()
    
    try:
        # Check if questions already exist
        existing_questions = db.query(Question).count()
        if existing_questions > 0:
            print(f"Database already has {existing_questions} questions. Skipping initialization.")
            return
        
        print("Initializing database with sample questions...")
        
        # Add sample questions
        for question_data in SAMPLE_QUESTIONS:
            question = QuestionCreate(**question_data)
            create_question(db=db, question=question)
        
        db.commit()
        print(f"Successfully added {len(SAMPLE_QUESTIONS)} questions to the database.")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
