from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/logs",
    tags=["logs"]
)

@router.post("/", response_model=schemas.HabitLogResponse)
def create_habit_log(log: schemas.HabitLogCreate, db: Session = Depends(get_db)):
    # Verify habit exists
    habit = db.query(models.Habit).filter(models.Habit.id == log.habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    db_log = models.HabitLog(**log.model_dump(exclude_unset=True))
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/habit/{habit_id}", response_model=list[schemas.HabitLogResponse])
def read_habit_logs(habit_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    logs = db.query(models.HabitLog).filter(models.HabitLog.habit_id == habit_id).order_by(models.HabitLog.logged_at.desc()).offset(skip).limit(limit).all()
    return logs
