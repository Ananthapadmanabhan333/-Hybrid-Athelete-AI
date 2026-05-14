"""
Database migration script to add TrainingConversation table.
Run this to enable fine-tuning data collection.
"""
from sqlalchemy import create_engine, MetaData
from app.core.config import settings
from app.db.base import Base
from app.models.user import User
from app.models.athlete_state import AthleteState
from app.models.training_conversation import TrainingConversation
# Import all other models
from app.models.daily_log import DailyLog
from app.models.feedback import WorkoutFeedback
from app.models.injury import Injury

def create_tables():
    """Create all tables in the database."""
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")
    print("\nNew tables added:")
    print("  - training_conversation (for fine-tuning data collection)")

if __name__ == "__main__":
    create_tables()
