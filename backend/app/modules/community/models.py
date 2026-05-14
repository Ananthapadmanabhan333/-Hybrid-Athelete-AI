
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class CommunityPost(Base):
    __tablename__ = "community_posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    content = Column(Text, nullable=False)
    post_type = Column(String, default="text") # 'text', 'workout_share', 'image'
    image_url = Column(String, nullable=True)
    likes_count = Column(Integer, default=0)
    
    # Simple JSON list for comments for MVP, or separate table
    # Sticking to separate table if complex, but MVP maybe JSON
    # Let's do a Comment table for better structure
    
class Comment(Base):
    __tablename__ = "community_comments"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer, ForeignKey("community_posts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    content = Column(String)
