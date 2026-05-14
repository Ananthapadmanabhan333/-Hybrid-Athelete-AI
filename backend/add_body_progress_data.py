import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
import random
from app.db.session import SessionLocal
from app.models.user import User
from app.modules.body_progress_engine.models import BodyWeightLog

def add_data():
    db = SessionLocal()
    # Get the test user or first user
    user = db.query(User).first()
    if not user:
        print("No user found. Please register a user first.")
        db.close()
        return

    print(f"Adding body progress data for user: {user.email}")
    
    # Clear existing logs for this user to avoid duplication during testing
    db.query(BodyWeightLog).filter(BodyWeightLog.user_id == user.id).delete()
    
    # Generate last 30 days of data
    start_date = datetime.utcnow() - timedelta(days=30)
    
    base_weight = 75.0
    base_bf = 18.0
    
    logs = []
    for i in range(30):
        current_date = start_date + timedelta(days=i)
        
        # Simulate slight changes over time (trending down slightly)
        weight = base_weight - (i * 0.05) + random.uniform(-0.5, 0.5)
        bf = base_bf - (i * 0.05) + random.uniform(-0.2, 0.2)
        muscle = weight * (1 - (bf/100)) * 0.51 # Mock calculation
        
        log = BodyWeightLog(
            user_id=user.id,
            date=current_date,
            weight=round(weight, 1),
            body_fat_percentage=round(bf, 1),
            muscle_mass_estimate=round(muscle, 1)
        )
        logs.append(log)
    
    db.add_all(logs)
    db.commit()
    print(f"Successfully added {len(logs)} body weight logs!")
    db.close()

if __name__ == "__main__":
    add_data()
