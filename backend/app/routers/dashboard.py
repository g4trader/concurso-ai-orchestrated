from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas, auth
from app.models import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get dashboard statistics for current user"""
    return crud.get_dashboard_stats(db=db, user_id=current_user.id)


@router.get("/results", response_model=list[schemas.SimuladoResult])
def get_recent_results(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(auth.get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get recent simulado results"""
    return crud.get_user_results(db=db, user_id=current_user.id, skip=skip, limit=limit)
