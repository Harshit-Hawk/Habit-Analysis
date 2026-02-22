from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
from services.analytics import generate_dashboard_data

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)

@router.get("/{habit_id}", response_model=schemas.AnalyticsDashboardResponse)
def get_habit_analytics(habit_id: int, db: Session = Depends(get_db)):
    dashboard_data = generate_dashboard_data(habit_id, db)
    if not dashboard_data:
        raise HTTPException(status_code=404, detail="Habit not found or insufficient data")
    return dashboard_data
