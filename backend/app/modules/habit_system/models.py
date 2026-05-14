
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from app.db.base import Base

class HabitStreak(Base):
    __tablename__ = "habit_streaks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    habit_type = Column(String, index=True) # 'water', 'sleep', 'workout'
    current_streak = Column(Integer, default=0)
    max_streak = Column(Integer, default=0)
    last_completed_date = Column(DateTime, nullable=True)

class DailyHabitLog(Base):
    __tablename__ = "daily_habit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    habit_type = Column(String, index=True)
    status = Column(Boolean, default=False)
    value = Column(String, nullable=True) # e.g. "2000ml" for water
