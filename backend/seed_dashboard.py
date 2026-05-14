import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta, date
import random
from app.db.session import SessionLocal
from app.models.user import User
from app.models.daily_log import DailyLog
from app.models.daily_task import DailyTask, TaskCategory, TaskPriority
from app.models.athlete_state import AthleteState, MesocyclePhase
from app.models.training import TrainingSession, TrainingType
from app.models.nutrition import NutritionLog, MealType, WaterLog

def seed_dashboard():
    db = SessionLocal()
    user = db.query(User).first()
    
    if not user:
        print("No user found. Please register first.")
        db.close()
        return

    print(f"Populating full dashboard data for: {user.email}")
    
    # 1. Athlete State
    athlete_state = db.query(AthleteState).filter(AthleteState.user_id == user.id).first()
    if not athlete_state:
        athlete_state = AthleteState(
            user_id=user.id,
            cns_fatigue=45.0,
            muscular_fatigue_upper=60.0,
            muscular_fatigue_lower=30.0,
            cardio_fatigue=20.0,
            current_mesocycle_phase=MesocyclePhase.ACCUMULATION,
            week_in_phase=2,
            last_workout_date=datetime.utcnow() - timedelta(days=1)
        )
        db.add(athlete_state)
    else:
        athlete_state.cns_fatigue = 45.0
        athlete_state.muscular_fatigue_upper = 60.0
        athlete_state.muscular_fatigue_lower = 30.0
        athlete_state.cardio_fatigue = 20.0

    # 2. Daily Logs (last 14 days)
    db.query(DailyLog).filter(DailyLog.user_id == user.id).delete()
    logs = []
    
    for i in range(14):
        log_date = date.today() - timedelta(days=i)
        
        log = DailyLog(
            user_id=user.id,
            date=log_date,
            total_calories_in=random.randint(2200, 2800),
            total_training_minutes=random.choice([0, 45, 60, 90]),
            recovery_score=random.randint(60, 95),
            sleep_hours=random.uniform(6.5, 8.5),
            mood=random.randint(6, 10),
            soreness_level=random.randint(2, 7)
        )
        logs.append(log)
    
    db.add_all(logs)
    
    # 3. Daily Tasks (Today)
    db.query(DailyTask).filter(DailyTask.user_id == user.id).delete()
    
    tasks = [
        DailyTask(
            user_id=user.id,
            title="Heavy Bag Intervals",
            message="Focus on speed and combination flow today. 5 rounds of 3 minutes with 1 minute rest.",
            category=TaskCategory.TRAINING,
            priority=TaskPriority.HIGH,
            is_completed=False,
            due_date=datetime.utcnow()
        ),
        DailyTask(
            user_id=user.id,
            title="Post-Workout Protein",
            message="Get 40g of protein within 1 hour after boxing to aid muscular recovery.",
            category=TaskCategory.NUTRITION,
            priority=TaskPriority.HIGH,
            is_completed=False,
            due_date=datetime.utcnow()
        ),
        DailyTask(
            user_id=user.id,
            title="Foam Roll Upper Body",
            message="Your upper body fatigue is at 60%. Spend 10 mins on lats, traps, and chest.",
            category=TaskCategory.RECOVERY,
            priority=TaskPriority.MEDIUM,
            is_completed=True,
            due_date=datetime.utcnow()
        ),
        DailyTask(
            user_id=user.id,
            title="Hydration Check",
            message="Drink at least 3 liters of water today.",
            category=TaskCategory.NUTRITION,
            priority=TaskPriority.MEDIUM,
            is_completed=True,
            due_date=datetime.utcnow()
        )
    ]
    db.add_all(tasks)
    
    # 4. Dummy Training Session (for today)
    db.query(TrainingSession).filter(TrainingSession.user_id == user.id).delete()
    
    training = TrainingSession(
        user_id=user.id,
        type=TrainingType.BOXING,
        started_at=datetime.utcnow() - timedelta(hours=3),
        duration_minutes=60,
        rpe=8,
        notes="Felt explosive today, combinations flowing well."
    )
    db.add(training)
    
    # 5. Dummy Nutrition for today
    db.query(NutritionLog).filter(NutritionLog.user_id == user.id).delete()
    db.query(WaterLog).filter(WaterLog.user_id == user.id).delete()
    
    nutrition = [
        NutritionLog(
            user_id=user.id, food_name="Oatmeal with Protein Powder", calories=450, 
            protein_g=35.0, carbs_g=55.0, fats_g=10.0, meal_type=MealType.BREAKFAST,
            timestamp=datetime.utcnow() - timedelta(hours=6)
        ),
        NutritionLog(
            user_id=user.id, food_name="Chicken Rice and Broccoli", calories=650, 
            protein_g=50.0, carbs_g=70.0, fats_g=15.0, meal_type=MealType.LUNCH,
            timestamp=datetime.utcnow() - timedelta(hours=2)
        )
    ]
    water = WaterLog(user_id=user.id, amount_ml=1500, timestamp=datetime.utcnow() - timedelta(hours=4))
    
    db.add_all(nutrition)
    db.add(water)
    
    db.commit()
    print("Dashboard fully populated with realistic seed data!")
    db.close()

if __name__ == "__main__":
    seed_dashboard()
