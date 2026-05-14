from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta
from typing import List
from app.models.user import User
from app.models.daily_task import DailyTask, TaskCategory, TaskPriority
from app.models.athlete_state import AthleteState
from app.models.daily_log import DailyLog
# from app.ai_engine.workout_generator import WorkoutGenerator # Circular dependency risk if not careful

class NotificationAgent:
    """
    Intelligent Agent that generates and manages daily tasks.
    Acts as the 'Executive Function' for the athlete.
    """
    
    def get_or_create_daily_tasks(self, user: User, db: Session) -> List[DailyTask]:
        """
        Fetches today's tasks. If none exist, generates them based on current state.
        """
        today = date.today()
        # Query tasks for today
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        tasks = db.query(DailyTask).filter(
            DailyTask.user_id == user.id, 
            DailyTask.due_date >= start_of_day,
            DailyTask.due_date <= end_of_day
        ).all()
        
        if not tasks:
            tasks = self._generate_daily_plan(user, db)
        
        return tasks

    def _generate_daily_plan(self, user: User, db: Session) -> List[DailyTask]:
        """
        The Brain: Decides what the user needs to do today.
        """
        new_tasks = []
        state = db.query(AthleteState).filter(AthleteState.user_id == user.id).first()
        
        # 1. Training Task
        # Check fatigue to determine tone
        fatigue_high = False
        if state and (state.cns_fatigue > 8.0 or state.muscular_fatigue_lower > 8.0): # Assuming 0-10 or 0-100 scale? previous code used 0-100% logic in UI but 0-10 in rules. Let's assume 0-10 for consistency with RPE or handle scaling. 
            # If rules.py uses 0-10 for fatigue, we assume state stores analogous value. 
            # Let looks at AthleteState Definition: cns_fatigue is Float.
            pass

        # For MVP, let's create a generic Training Task that links to the Workout Generator
        new_task_training = DailyTask(
            user_id=user.id,
            title="Daily Training Session",
            message="Your adaptive plan is ready. Tap to view.",
            category="training", # Using string for simplicity to avoid Enum issues with SQLite sometimes
            priority="high",
            due_date=datetime.now(),
            is_completed=False
        )
        new_tasks.append(new_task_training)
        
        # 2. Nutrition Task
        new_tasks.append(DailyTask(
             user_id=user.id,
             title="Log Nutrition",
             message="Track your meals to stay on target.",
             category="nutrition",
             priority="medium",
             due_date=datetime.now(),
             is_completed=False
        ))

        # 3. Mindset/Recovery Check-in
        new_tasks.append(DailyTask(
             user_id=user.id,
             title="Recovery Check",
             message="How are you feeling? Log your metrics.",
             category="recovery",
             priority="low",
             due_date=datetime.now(),
             is_completed=False
        ))

        # Save to DB
        try:
            for t in new_tasks:
                db.add(t)
            db.commit()
            # Refresh to get IDs
            for t in new_tasks:
                db.refresh(t)
        except Exception as e:
            db.rollback()
            print(f"Error creating tasks: {e}")
            return []
        
        return new_tasks

    def complete_task(self, task_id: int, db: Session) -> bool:
        task = db.query(DailyTask).filter(DailyTask.id == task_id).first()
        if task:
            task.is_completed = True
            db.commit()
            return True
        return False
