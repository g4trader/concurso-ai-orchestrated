from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth
from app.models import User

router = APIRouter(prefix="/simulados", tags=["simulados"])


@router.post("/", response_model=schemas.Simulado)
def create_simulado(
    simulado: schemas.SimuladoCreate,
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new simulado"""
    # Generate questions for the simulado
    questions = crud.get_questions_for_simulado(
        db=db,
        subjects=simulado.config.subjects,
        banca=simulado.config.banca,
        level=simulado.config.level,
        num_questions=simulado.config.num_questions
    )
    
    if len(questions) < simulado.config.num_questions:
        raise HTTPException(
            status_code=400,
            detail=f"Not enough questions available. Found {len(questions)}, requested {simulado.config.num_questions}"
        )
    
    # Create simulado
    db_simulado = crud.create_simulado(db=db, simulado=simulado, user_id=current_user.id)
    
    # Add questions to simulado
    crud.add_questions_to_simulado(db=db, simulado_id=db_simulado.id, questions=questions)
    
    return db_simulado


@router.get("/", response_model=List[schemas.Simulado])
def get_simulados(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get user's simulados"""
    return crud.get_user_simulados(db=db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/{simulado_id}", response_model=schemas.SimuladoWithQuestions)
def get_simulado(
    simulado_id: int,
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get simulado with questions"""
    simulado = crud.get_simulado(db=db, simulado_id=simulado_id, user_id=current_user.id)
    if not simulado:
        raise HTTPException(status_code=404, detail="Simulado not found")
    
    # Get questions for this simulado
    simulado_questions = db.query(crud.SimuladoQuestion).filter(
        crud.SimuladoQuestion.simulado_id == simulado_id
    ).order_by(crud.SimuladoQuestion.order).all()
    
    questions = []
    for sq in simulado_questions:
        question = crud.get_question(db=db, question_id=sq.question_id)
        if question:
            questions.append(question)
    
    # Convert to response model
    simulado_dict = {
        "id": simulado.id,
        "title": simulado.title,
        "user_id": simulado.user_id,
        "config": simulado.config,
        "time_limit": simulado.time_limit,
        "total_questions": simulado.total_questions,
        "created_at": simulado.created_at,
        "started_at": simulado.started_at,
        "completed_at": simulado.completed_at,
        "questions": questions
    }
    
    return schemas.SimuladoWithQuestions(**simulado_dict)


@router.post("/{simulado_id}/start", response_model=schemas.Simulado)
def start_simulado(
    simulado_id: int,
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Start a simulado"""
    simulado = crud.start_simulado(db=db, simulado_id=simulado_id, user_id=current_user.id)
    if not simulado:
        raise HTTPException(status_code=404, detail="Simulado not found")
    
    return simulado


@router.post("/{simulado_id}/submit", response_model=schemas.SimuladoResult)
def submit_simulado(
    simulado_id: int,
    result: schemas.SimuladoResultCreate,
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Submit simulado answers and get results"""
    # Verify simulado belongs to user
    simulado = crud.get_simulado(db=db, simulado_id=simulado_id, user_id=current_user.id)
    if not simulado:
        raise HTTPException(status_code=404, detail="Simulado not found")
    
    # Check if already submitted
    existing_result = crud.get_simulado_result(db=db, simulado_id=simulado_id, user_id=current_user.id)
    if existing_result:
        raise HTTPException(status_code=400, detail="Simulado already submitted")
    
    # Create result
    return crud.create_simulado_result(db=db, result=result, user_id=current_user.id)


@router.get("/{simulado_id}/result", response_model=schemas.SimuladoResult)
def get_simulado_result(
    simulado_id: int,
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get simulado result"""
    result = crud.get_simulado_result(db=db, simulado_id=simulado_id, user_id=current_user.id)
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")
    
    return result
