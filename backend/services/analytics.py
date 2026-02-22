from sqlalchemy.orm import Session
from sqlalchemy import func
import models
import schemas
from typing import List

# Helper function to compute correlations based on a specific attribute
def get_failure_correlations(logs: List[models.HabitLog], attribute: str) -> List[schemas.CorrelationStat]:
    counts = {}     # { "attr_value": total_logs }
    failures = {}   # { "attr_value": total_failures }

    for log in logs:
        # e.g. getting log.mood, log.context
        val = getattr(log, attribute)
        if val is None:
            continue
            
        val_str = str(val.value) if hasattr(val, 'value') else str(val)
        
        counts[val_str] = counts.get(val_str, 0) + 1
        if log.status == models.Status.failure:
            failures[val_str] = failures.get(val_str, 0) + 1
            
    stats = []
    for val_str, total in counts.items():
        if total >= 3: # Need minimal sample size to be considered a 'correlation'
            fail_count = failures.get(val_str, 0)
            stats.append(schemas.CorrelationStat(
                factor=val_str,
                failure_rate=fail_count / total,
                sample_size=total
            ))
            
    # Sort by highest failure rate
    stats.sort(key=lambda x: x.failure_rate, reverse=True)
    return stats

def get_sleep_correlation(logs: List[models.HabitLog]) -> List[schemas.CorrelationStat]:
    # Group sleep into brackets: < 6, 6-8, > 8
    counts = {"< 6 hours": 0, "6-8 hours": 0, "> 8 hours": 0}
    failures = {"< 6 hours": 0, "6-8 hours": 0, "> 8 hours": 0}

    for log in logs:
        if log.sleep_hours is None:
            continue
            
        if log.sleep_hours < 6:
            bracket = "< 6 hours"
        elif log.sleep_hours <= 8:
            bracket = "6-8 hours"
        else:
            bracket = "> 8 hours"
            
        counts[bracket] += 1
        if log.status == models.Status.failure:
            failures[bracket] += 1
            
    stats = []
    for bracket, total in counts.items():
        if total >= 3:
            fail_count = failures.get(bracket, 0)
            stats.append(schemas.CorrelationStat(
                factor=bracket,
                failure_rate=fail_count / total,
                sample_size=total
            ))
            
    stats.sort(key=lambda x: x.failure_rate, reverse=True)
    return stats

def generate_dashboard_data(habit_id: int, db: Session) -> schemas.AnalyticsDashboardResponse | None:
    habit = db.query(models.Habit).filter(models.Habit.id == habit_id).first()
    if not habit:
        return None
        
    logs = db.query(models.HabitLog).filter(models.HabitLog.habit_id == habit_id).all()
    total_logs = len(logs)
    
    if total_logs == 0:
        return schemas.AnalyticsDashboardResponse(
            habit=schemas.HabitResponse.model_validate(habit),
            total_logs=0,
            success_rate=0.0,
            predictions=schemas.FailurePredictionSummary(
                habit_id=habit_id,
                risk_level="Low",
                explanation="Not enough data to predict failure risk."
            ),
            correlations={"mood": [], "context": [], "sleep": []}
        )
        
    successes = sum(1 for log in logs if log.status == models.Status.success)
    success_rate = successes / total_logs
    overall_failure_rate = 1.0 - success_rate
    
    mood_stats = get_failure_correlations(logs, 'mood')
    context_stats = get_failure_correlations(logs, 'context')
    sleep_stats = get_sleep_correlation(logs)
    
    # Simple Heuristic for Risk Prediction
    # High risk if overall failure > 60% OR there's a specific factor causing > 80% failure
    # Medium risk if overall failure > 30% OR there's a specific factor causing > 50% failure
    
    max_specific_failure_rate = 0.0
    top_risk_factor = None
    
    all_stats = mood_stats + context_stats + sleep_stats
    for stat in all_stats:
        if stat.failure_rate > max_specific_failure_rate:
            max_specific_failure_rate = stat.failure_rate
            top_risk_factor = stat.factor
            
    if overall_failure_rate > 0.6 or max_specific_failure_rate > 0.8:
        risk_level = "High"
    elif overall_failure_rate > 0.3 or max_specific_failure_rate > 0.5:
        risk_level = "Medium"
    else:
        risk_level = "Low"
        
    # Generate Explanation
    explanation = "Based on statistical analysis, "
    
    if top_risk_factor and max_specific_failure_rate > 0.5:
        rate_pct = int(max_specific_failure_rate * 100)
        explanation += f"the risk is primarily driven by the factor '{top_risk_factor}', which has a {rate_pct}% failure rate."
    else:
        fail_pct = int(overall_failure_rate * 100)
        if risk_level == "Low":
            explanation += f"you are maintaining a good success rate with only a {fail_pct}% overall failure rate."
        else:
            explanation += f"the overall failure rate is {fail_pct}%, though no single dominant external factor was identified. Consider reviewing the habit target frequency."

    return schemas.AnalyticsDashboardResponse(
        habit=schemas.HabitResponse.model_validate(habit),
        total_logs=total_logs,
        success_rate=success_rate,
        predictions=schemas.FailurePredictionSummary(
            habit_id=habit_id,
            risk_level=risk_level,
            explanation=explanation
        ),
        correlations={
            "mood": mood_stats,
            "context": context_stats,
            "sleep": sleep_stats
        }
    )
