from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class ChatMessage(Base):
    """Store AI Coach chat messages for history and fine-tuning"""
    __tablename__ = "chat_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Message content
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow)
    session_id = Column(String, nullable=True)  # Group related messages
    
    # Relationship
    user = relationship("User", backref="chat_history")
