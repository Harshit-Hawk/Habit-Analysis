from database import SessionLocal
import models
from datetime import datetime, timedelta, timezone

def seed_data():
    db = SessionLocal()
    
    # Check if habit already exists
    habit = db.query(models.Habit).filter(models.Habit.name == "Morning Workout").first()
    if not habit:
        habit = models.Habit(name="Morning Workout", target_frequency=models.TargetFrequency.daily)
        db.add(habit)
        db.commit()
        db.refresh(habit)
        
    print(f"Created/Found habit: {habit.id}")
    
    # Add some mock logs where failing is correlated with low sleep and stressed mood
    logs_to_add = [
        # Failures (low sleep, stressed)
        models.HabitLog(habit_id=habit.id, status=models.Status.failure, sleep_hours=5.0, mood=models.Mood.stressed, context=models.Context.other, logged_at=datetime.now(timezone.utc) - timedelta(days=5)),
        models.HabitLog(habit_id=habit.id, status=models.Status.failure, sleep_hours=4.5, mood=models.Mood.stressed, context=models.Context.other, logged_at=datetime.now(timezone.utc) - timedelta(days=4)),
        models.HabitLog(habit_id=habit.id, status=models.Status.failure, sleep_hours=5.5, mood=models.Mood.tired, context=models.Context.other, logged_at=datetime.now(timezone.utc) - timedelta(days=3)),
        
        # Successes (good sleep, varied moods)
        models.HabitLog(habit_id=habit.id, status=models.Status.success, sleep_hours=8.0, mood=models.Mood.neutral, context=models.Context.other, logged_at=datetime.now(timezone.utc) - timedelta(days=2)),
        models.HabitLog(habit_id=habit.id, status=models.Status.success, sleep_hours=7.5, mood=models.Mood.neutral, context=models.Context.other, logged_at=datetime.now(timezone.utc) - timedelta(days=1)),
        models.HabitLog(habit_id=habit.id, status=models.Status.success, sleep_hours=9.0, mood=models.Mood.neutral, context=models.Context.other, logged_at=datetime.now(timezone.utc)),
    ]
    
    # To trigger the ">= 3" threshold for a bracket in analytics
    for _ in range(3):
        db.add(models.HabitLog(habit_id=habit.id, status=models.Status.failure, sleep_hours=5.0, mood=models.Mood.stressed, context=models.Context.work, logged_at=datetime.now(timezone.utc)))
    
    for log in logs_to_add:
        db.add(log)
        
    db.commit()
    print("Test data seeded!")
    db.close()

if __name__ == "__main__":
    seed_data()
