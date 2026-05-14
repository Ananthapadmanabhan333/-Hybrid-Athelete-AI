
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from datetime import datetime
from app.db.base import Base

class WearableSyncStatus(Base):
    __tablename__ = "wearable_sync_status"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    provider = Column(String, index=True) # e.g., 'apple', 'garmin', 'whoop'
    last_sync = Column(DateTime)
    status = Column(String) # 'success', 'failed', 'pending'
    access_token = Column(String, nullable=True) # encrypted in real app, simplified for now
    refresh_token = Column(String, nullable=True)
    expires_in = Column(Integer, nullable=True)
