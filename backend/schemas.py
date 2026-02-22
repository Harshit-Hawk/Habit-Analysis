from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from models import TargetFrequency, Status, Mood, Context

# Habit Schemas
class HabitBase(BaseModel):
    name: str
    target_frequency: TargetFrequency

class HabitCreate(HabitBase):
    pass

class HabitResponse(HabitBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# HabitLog Schemas
class HabitLogBase(BaseModel):
    status: Status
    sleep_hours: Optional[float] = None
    mood: Optional[Mood] = None
    context: Optional[Context] = None
    
    # Allow logging for a past date if needed, otherwise defaults to now
    logged_at: Optional[datetime] = None

class HabitLogCreate(HabitLogBase):
    habit_id: int

class HabitLogResponse(HabitLogBase):
    id: int
    habit_id: int
    logged_at: datetime

    class Config:
        from_attributes = True

# Analytics Schemas
class FailurePredictionSummary(BaseModel):
    habit_id: int
    risk_level: str # 'Low', 'Medium', 'High'
    explanation: str

class CorrelationStat(BaseModel):
    factor: str
    failure_rate: float
    sample_size: int

class AnalyticsDashboardResponse(BaseModel):
    habit: HabitResponse
    total_logs: int
    success_rate: float
    predictions: FailurePredictionSummary
    correlations: dict[str, List[CorrelationStat]] # e.g., {'mood': [...], 'context': [...]}
