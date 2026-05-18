import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta, date
import random
import uuid

from app.db.session import SessionLocal
from app.models.user import User
from app.models.daily_log import DailyLog
from app.models.daily_task import DailyTask, TaskCategory, TaskPriority
from app.models.athlete_state import AthleteState, MesocyclePhase
from app.models.training import TrainingSession, TrainingType
from app.models.nutrition import NutritionLog, MealType, WaterLog
from app.models.injury import Injury, BodyPart, InjuryType, InjuryStatus
from app.models.chat_message import ChatMessage
from app.modules.body_progress_engine.models import BodyWeightLog

def seed_comprehensive_data():
    db = SessionLocal()
    user = db.query(User).first()
    
    if not user:
        print("No user found. Please register first.")
        db.close()
        return

    print(f"Starting comprehensive data seed for: {user.email}")
    
    # 0. Clean Existing Data to avoid duplication
    print("Cleaning old data...")
    db.query(DailyLog).filter(DailyLog.user_id == user.id).delete()
    db.query(DailyTask).filter(DailyTask.user_id == user.id).delete()
    db.query(TrainingSession).filter(TrainingSession.user_id == user.id).delete()
    db.query(NutritionLog).filter(NutritionLog.user_id == user.id).delete()
    db.query(WaterLog).filter(WaterLog.user_id == user.id).delete()
    db.query(Injury).filter(Injury.user_id == user.id).delete()
    db.query(ChatMessage).filter(ChatMessage.user_id == user.id).delete()
    db.query(BodyWeightLog).filter(BodyWeightLog.user_id == user.id).delete()
    db.commit()

    # 1. Athlete State
    print("Seeding Athlete State...")
    athlete_state = db.query(AthleteState).filter(AthleteState.user_id == user.id).first()
    if not athlete_state:
        athlete_state = AthleteState(
            user_id=user.id,
            cns_fatigue=55.0,
            muscular_fatigue_upper=75.0,
            muscular_fatigue_lower=40.0,
            cardio_fatigue=35.0,
            current_mesocycle_phase=MesocyclePhase.ACCUMULATION,
            week_in_phase=3,
            last_workout_date=datetime.utcnow() - timedelta(hours=14)
        )
        db.add(athlete_state)
    else:
        athlete_state.cns_fatigue = 55.0
        athlete_state.muscular_fatigue_upper = 75.0
        athlete_state.muscular_fatigue_lower = 40.0
        athlete_state.cardio_fatigue = 35.0
        athlete_state.week_in_phase = 3
    
    # 2. Daily Logs (last 30 days)
    print("Seeding 30 Days of Daily Logs...")
    logs = []
    for i in range(30):
        log_date = date.today() - timedelta(days=i)
        
        # Simulate an upward trend in recovery over the month
        base_recovery = 70 + (30 - i) * 0.5 
        recovery = min(100, int(base_recovery + random.uniform(-10, 10)))
        
        log = DailyLog(
            user_id=user.id,
            date=log_date,
            total_calories_in=random.randint(2300, 3100),
            total_training_minutes=random.choice([0, 45, 60, 60, 90, 120]),
            recovery_score=recovery,
            sleep_hours=round(random.uniform(6.0, 9.0), 1),
            mood=random.randint(6, 10),
            soreness_level=max(1, min(10, random.randint(2, 6) + (3 if i < 5 else 0))), # More sore recently
            notes="Felt good, pushed hard on the heavy bag." if i % 3 == 0 else ""
        )
        logs.append(log)
    db.add_all(logs)

    # 3. Body Progress (last 60 days)
    print("Seeding Body Progress Logs...")
    body_logs = []
    base_weight = 78.5
    base_bf = 19.5
    for i in range(60, -1, -1): # 60 days ago to today
        current_date = datetime.utcnow() - timedelta(days=i)
        # Simulate slight changes over time (trending down slightly, getting leaner)
        weight = base_weight - (60 - i) * 0.04 + random.uniform(-0.3, 0.3)
        bf = base_bf - (60 - i) * 0.05 + random.uniform(-0.1, 0.1)
        muscle = weight * (1 - (bf/100)) * 0.52 # Mock calculation
        
        log = BodyWeightLog(
            user_id=user.id,
            date=current_date,
            weight=round(weight, 1),
            body_fat_percentage=round(bf, 1),
            muscle_mass_estimate=round(muscle, 1)
        )
        body_logs.append(log)
    db.add_all(body_logs)

    # 4. Training Sessions (last 14 days)
    print("Seeding Training Sessions...")
    training = []
    for i in range(1, 15):
        if i % 3 == 0: continue # Rest days
        
        t_type = TrainingType.BOXING if i % 2 == 0 else TrainingType.STRENGTH
        started_at = datetime.utcnow() - timedelta(days=i, hours=random.randint(6, 16))
        durations = [45, 60, 90]
        
        training.append(TrainingSession(
            user_id=user.id,
            type=t_type,
            started_at=started_at,
            duration_minutes=random.choice(durations),
            rpe=random.randint(6, 9),
            notes=f"Great {t_type.value} session today. " + ("Worked on combinations." if t_type == TrainingType.BOXING else "Hit a PR on deadlifts.")
        ))
    db.add_all(training)

    # 5. Nutrition & Water Logs (Today & Yesterday)
    print("Seeding Nutrition & Water Logs...")
    meals = [
        {"name": "Protein Oatmeal with Berries", "cal": 450, "p": 35.0, "c": 55.0, "f": 10.0, "type": MealType.BREAKFAST, "offset_hrs": 6},
        {"name": "Chicken Breast, Sweet Potato, Broccoli", "cal": 650, "p": 55.0, "c": 70.0, "f": 15.0, "type": MealType.LUNCH, "offset_hrs": 3},
        {"name": "Greek Yogurt & Almonds", "cal": 280, "p": 20.0, "c": 15.0, "f": 16.0, "type": MealType.SNACK, "offset_hrs": 1},
    ]
    nutrition = []
    for m in meals:
        nutrition.append(NutritionLog(
            user_id=user.id, food_name=m["name"], calories=m["cal"],
            protein_g=m["p"], carbs_g=m["c"], fats_g=m["f"], meal_type=m["type"],
            timestamp=datetime.utcnow() - timedelta(hours=m["offset_hrs"])
        ))
        
        # Add identical meals for yesterday
        nutrition.append(NutritionLog(
            user_id=user.id, food_name=m["name"], calories=int(m["cal"]* 0.95),
            protein_g=m["p"], carbs_g=m["c"], fats_g=m["f"], meal_type=m["type"],
            timestamp=datetime.utcnow() - timedelta(days=1, hours=m["offset_hrs"])
        ))
    db.add_all(nutrition)
    
    water = [
        WaterLog(user_id=user.id, amount_ml=500, timestamp=datetime.utcnow() - timedelta(hours=i*2)) for i in range(1, 4)
    ]
    db.add_all(water)

    # 6. Injuries
    print("Seeding Injuries...")
    injuries = [
        Injury(user_id=user.id, body_part=BodyPart.SHOULDER.value, injury_type=InjuryType.STRAIN.value, severity="moderate", pain_level=6, status=InjuryStatus.ACTIVE.value, notes="Tweaked right shoulder during heavy bag work. Avoiding overhead presses.", created_at=datetime.utcnow() - timedelta(days=3)),
        Injury(user_id=user.id, body_part=BodyPart.KNEE.value, injury_type=InjuryType.SORENESS.value, severity="mild", pain_level=2, status=InjuryStatus.HEALED.value, notes="Patellar tendon felt tight, but recovered with foam rolling.", created_at=datetime.utcnow() - timedelta(days=20))
    ]
    db.add_all(injuries)

    # 7. AI Chat Messages
    print("Seeding Chat History...")
    session_str = str(uuid.uuid4())
    chats = [
        ChatMessage(user_id=user.id, user_message="Hey coach, my right shoulder is feeling a bit tight today after boxing yesterday.", ai_response="I hear you. Shoulder tightness is common after heavy bag work. Let's add a 'Moderate' Strain injury for your Right Shoulder to your log so the system adapts your upcoming workouts. For today, focus on posterior chain stretching (like doorway stretches and face pulls with light bands). Avoid heavy overhead pressing.", session_id=session_str, timestamp=datetime.utcnow() - timedelta(hours=48)),
        ChatMessage(user_id=user.id, user_message="What should I eat before my strength session today?", ai_response="Aim for easily digestible carbs and moderate protein about 1-2 hours before lifting. A great choice would be 1 cup of oatmeal with half a scoop of whey protein, or 2 rice cakes with a tablespoon of peanut butter and a banana. This will give you the glycogen you need without making you feel sluggish.", session_id=session_str, timestamp=datetime.utcnow() - timedelta(hours=5))
    ]
    db.add_all(chats)

    # 8. Daily Tasks (Today)
    print("Seeding Daily Tasks...")
    tasks = [
        DailyTask(user_id=user.id, title="Shoulder Mobility Routine", message="Do the 15-minute rotator cuff and lat mobility sequence to help heal your active shoulder strain.", category=TaskCategory.RECOVERY, priority=TaskPriority.HIGH, is_completed=False, due_date=datetime.utcnow()),
        DailyTask(user_id=user.id, title="Hit protein goal", message="You are currently at 110g of protein for the day. Consume another 60g across dinner to reach your 170g target.", category=TaskCategory.NUTRITION, priority=TaskPriority.HIGH, is_completed=False, due_date=datetime.utcnow()),
        DailyTask(user_id=user.id, title="Read: Boxing Footwork Fundamentals", message="Review the assigned article on maintaining dominant angles during combinations.", category=TaskCategory.MINDSET, priority=TaskPriority.LOW, is_completed=True, due_date=datetime.utcnow()),
        DailyTask(user_id=user.id, title="Evening Hydration", message="Drink 1L of water before bed to aid muscle protein synthesis during sleep.", category=TaskCategory.NUTRITION, priority=TaskPriority.MEDIUM, is_completed=False, due_date=datetime.utcnow()),
    ]
    db.add_all(tasks)

    db.commit()
    print("All Comprehensive Data Successfully Seeded!")
    db.close()

if __name__ == "__main__":
    seed_comprehensive_data()
