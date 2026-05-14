from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Index, Text
from app.db.base import Base

class RecoveryLog(Base):
    __tablename__ = "recovery_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    
    sleep_hours = Column(Float, nullable=False)
    sleep_quality = Column(Integer, nullable=False) # 1-10
    hrv = Column(Float, nullable=False)
    resting_heart_rate = Column(Float, nullable=False)
    soreness = Column(Integer, nullable=False) # 1-10
    stress = Column(Integer, nullable=False) # 1-10
    hydration_liters = Column(Float, nullable=False)
    notes = Column(Text, nullable=True)

    __table_args__ = (Index('ix_rec_logs_user_date', 'user_id', 'date'), {'extend_existing': True})

class RecoveryScore(Base):
    __tablename__ = "recovery_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    date = Column(Date, nullable=False)
    
    recovery_score = Column(Float, nullable=False)
    fatigue_flag = Column(String, nullable=True)
    
    __table_args__ = (Index('ix_rec_scores_user_date', 'user_id', 'date'), {'extend_existing': True})
