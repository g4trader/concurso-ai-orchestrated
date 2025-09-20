from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from typing import List, Optional, Dict, Any
from app.models import User, Question, Simulado, SimuladoQuestion, SimuladoResult
from app.schemas import UserCreate, QuestionCreate, SimuladoCreate, SimuladoResultCreate
from app.auth import get_password_hash
import random


# User CRUD
def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Create new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        name=user.name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


# Question CRUD
def get_questions(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    subject: Optional[str] = None,
    banca: Optional[str] = None,
    level: Optional[str] = None
) -> List[Question]:
    """Get questions with filters"""
    query = db.query(Question)
    
    if subject:
        query = query.filter(Question.subject == subject)
    if banca:
        query = query.filter(Question.banca == banca)
    if level:
        query = query.filter(Question.level == level)
    
    return query.offset(skip).limit(limit).all()


def get_question(db: Session, question_id: int) -> Optional[Question]:
    """Get question by ID"""
    return db.query(Question).filter(Question.id == question_id).first()


def create_question(db: Session, question: QuestionCreate) -> Question:
    """Create new question"""
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


def get_questions_for_simulado(
    db: Session,
    subjects: List[str],
    banca: str,
    level: str,
    num_questions: int
) -> List[Question]:
    """Get questions for simulado generation"""
    query = db.query(Question).filter(
        and_(
            Question.subject.in_(subjects),
            Question.banca == banca,
            Question.level == level
        )
    )
    
    all_questions = query.all()
    
    # If we don't have enough questions, get from all levels
    if len(all_questions) < num_questions:
        query = db.query(Question).filter(
            and_(
                Question.subject.in_(subjects),
                Question.banca == banca
            )
        )
        all_questions = query.all()
    
    # If still not enough, get any questions from the subjects
    if len(all_questions) < num_questions:
        query = db.query(Question).filter(Question.subject.in_(subjects))
        all_questions = query.all()
    
    # Randomly select questions
    if len(all_questions) >= num_questions:
        return random.sample(all_questions, num_questions)
    else:
        return all_questions


# Simulado CRUD
def create_simulado(db: Session, simulado: SimuladoCreate, user_id: int) -> Simulado:
    """Create new simulado"""
    db_simulado = Simulado(
        title=simulado.title,
        user_id=user_id,
        config=simulado.config.dict(),
        time_limit=simulado.time_limit,
        total_questions=simulado.total_questions
    )
    db.add(db_simulado)
    db.commit()
    db.refresh(db_simulado)
    return db_simulado


def get_simulado(db: Session, simulado_id: int, user_id: int) -> Optional[Simulado]:
    """Get simulado by ID for specific user"""
    return db.query(Simulado).filter(
        and_(Simulado.id == simulado_id, Simulado.user_id == user_id)
    ).first()


def get_user_simulados(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[Simulado]:
    """Get user's simulados"""
    return db.query(Simulado).filter(Simulado.user_id == user_id).offset(skip).limit(limit).all()


def add_questions_to_simulado(db: Session, simulado_id: int, questions: List[Question]):
    """Add questions to simulado"""
    for i, question in enumerate(questions):
        simulado_question = SimuladoQuestion(
            simulado_id=simulado_id,
            question_id=question.id,
            order=i + 1
        )
        db.add(simulado_question)
    db.commit()


def start_simulado(db: Session, simulado_id: int, user_id: int) -> Optional[Simulado]:
    """Mark simulado as started"""
    simulado = get_simulado(db, simulado_id, user_id)
    if simulado:
        simulado.started_at = func.now()
        db.commit()
        db.refresh(simulado)
    return simulado


def complete_simulado(db: Session, simulado_id: int, user_id: int) -> Optional[Simulado]:
    """Mark simulado as completed"""
    simulado = get_simulado(db, simulado_id, user_id)
    if simulado:
        simulado.completed_at = func.now()
        db.commit()
        db.refresh(simulado)
    return simulado


# Simulado Result CRUD
def create_simulado_result(db: Session, result: SimuladoResultCreate, user_id: int) -> SimuladoResult:
    """Create simulado result"""
    # Calculate score
    simulado = get_simulado(db, result.simulado_id, user_id)
    if not simulado:
        raise ValueError("Simulado not found")
    
    # Get questions for this simulado
    simulado_questions = db.query(SimuladoQuestion).filter(
        SimuladoQuestion.simulado_id == result.simulado_id
    ).order_by(SimuladoQuestion.order).all()
    
    correct_answers = 0
    subject_scores = {}
    
    for sq in simulado_questions:
        question = get_question(db, sq.question_id)
        if not question:
            continue
            
        user_answer = result.answers.get(str(question.id))
        if user_answer == question.correct_answer:
            correct_answers += 1
        
        # Track subject scores
        if question.subject not in subject_scores:
            subject_scores[question.subject] = {"correct": 0, "total": 0}
        
        subject_scores[question.subject]["total"] += 1
        if user_answer == question.correct_answer:
            subject_scores[question.subject]["correct"] += 1
    
    score = int((correct_answers / len(simulado_questions)) * 100) if simulado_questions else 0
    
    db_result = SimuladoResult(
        simulado_id=result.simulado_id,
        user_id=user_id,
        answers=result.answers,
        score=score,
        correct_answers=correct_answers,
        time_spent=result.time_spent,
        subject_scores=subject_scores
    )
    
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    
    # Mark simulado as completed
    complete_simulado(db, result.simulado_id, user_id)
    
    return db_result


def get_simulado_result(db: Session, simulado_id: int, user_id: int) -> Optional[SimuladoResult]:
    """Get simulado result"""
    return db.query(SimuladoResult).filter(
        and_(
            SimuladoResult.simulado_id == simulado_id,
            SimuladoResult.user_id == user_id
        )
    ).first()


def get_user_results(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[SimuladoResult]:
    """Get user's results"""
    return db.query(SimuladoResult).filter(
        SimuladoResult.user_id == user_id
    ).offset(skip).limit(limit).all()


# Dashboard stats
def get_dashboard_stats(db: Session, user_id: int) -> Dict[str, Any]:
    """Get dashboard statistics for user"""
    # Total simulados
    total_simulados = db.query(Simulado).filter(Simulado.user_id == user_id).count()
    
    # Total questions answered
    total_questions = db.query(func.sum(SimuladoResult.correct_answers)).filter(
        SimuladoResult.user_id == user_id
    ).scalar() or 0
    
    # Average score
    avg_score = db.query(func.avg(SimuladoResult.score)).filter(
        SimuladoResult.user_id == user_id
    ).scalar() or 0
    
    # Best score
    best_score = db.query(func.max(SimuladoResult.score)).filter(
        SimuladoResult.user_id == user_id
    ).scalar() or 0
    
    # Total time spent
    total_time = db.query(func.sum(SimuladoResult.time_spent)).filter(
        SimuladoResult.user_id == user_id
    ).scalar() or 0
    
    # Subject performance
    results = db.query(SimuladoResult).filter(SimuladoResult.user_id == user_id).all()
    subject_performance = {}
    
    for result in results:
        for subject, scores in result.subject_scores.items():
            if subject not in subject_performance:
                subject_performance[subject] = {"correct": 0, "total": 0}
            subject_performance[subject]["correct"] += scores["correct"]
            subject_performance[subject]["total"] += scores["total"]
    
    # Calculate percentages
    for subject in subject_performance:
        total = subject_performance[subject]["total"]
        if total > 0:
            subject_performance[subject] = (subject_performance[subject]["correct"] / total) * 100
        else:
            subject_performance[subject] = 0
    
    return {
        "total_simulados": total_simulados,
        "total_questions_answered": total_questions,
        "average_score": round(avg_score, 2),
        "best_score": best_score,
        "time_spent_total": total_time,
        "subjects_performance": subject_performance
    }
