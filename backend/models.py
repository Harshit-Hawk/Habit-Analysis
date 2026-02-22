from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
import enum
from datetime import datetime, timezone
from database import Base

class TargetFrequency(str, enum.Enum):
    daily = "daily"
    weekly = "weekly"

class Status(str, enum.Enum):
    success = "success"
    failure = "failure"

class Mood(str, enum.Enum):
    stressed = "stressed"
    tired = "tired"
    distracted = "distracted"
    neutral = "neutral"

class Context(str, enum.Enum):
    phone = "phone"
    work = "work"
    social = "social"
    other = "other"

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    target_frequency = Column(Enum(TargetFrequency), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    logs = relationship("HabitLog", back_populates="habit", cascade="all, delete-orphan")

class HabitLog(Base):
    __tablename__ = "habit_logs"

    id = Column(Integer, primary_key=True, index=True)
    habit_id = Column(Integer, ForeignKey("habits.id"), nullable=False)
    status = Column(Enum(Status), nullable=False)
    sleep_hours = Column(Float, nullable=True) # Optional in case they don't want to log sleep
    mood = Column(Enum(Mood), nullable=True)     # Optional
    context = Column(Enum(Context), nullable=True) # Optional
    logged_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    habit = relationship("Habit", back_populates="logs")
