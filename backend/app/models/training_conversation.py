from sqlalchemy import Column, Integer, String, Text, DateTime, Float, JSON, Boolean
from sqlalchemy.sql import func
from app.db.base import Base

class TrainingConversation(Base):
    """
    Stores AI Coach conversations for fine-tuning data collection.
    Each conversation can be rated and used for model improvement.
    """
    __tablename__ = "training_conversation"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    
    # Conversation data
    user_message = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=False)
    system_prompt = Column(Text, nullable=True)
    
    # Context at time of conversation
    user_context = Column(JSON, nullable=True)  # Fatigue, sleep, mood, etc.
    
    # Quality metrics
    user_rating = Column(Integer, nullable=True)  # 1-5 stars
    was_helpful = Column(Boolean, default=None, nullable=True)
    feedback_text = Column(Text, nullable=True)
    
    # Model info
    model_version = Column(String, default="gemini-pro")
    response_time_ms = Column(Float, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    rated_at = Column(DateTime(timezone=True), nullable=True)
    
    # Fine-tuning flags
    included_in_training = Column(Boolean, default=False)
    training_dataset_version = Column(String, nullable=True)
