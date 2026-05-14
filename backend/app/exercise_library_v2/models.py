from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class ExerciseV2(Base):
    __tablename__ = "exercises_v2"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    video_url = Column(String, nullable=True)
    
    # Store steps as list of strings: ["Step 1", "Step 2", ...]
    instructions = Column(JSON, nullable=True)
    
    # Metadata for filtering and AI logic
    muscle_groups = Column(JSON, nullable=False) # e.g., ["chest", "triceps"]
    equipment_needed = Column(JSON, nullable=False) # e.g., ["dumbbells", "bench"]
    
    # Scaling logic
    # progression_id: easier -> harder
    # regression_id: harder -> easier
    progression_id = Column(Integer, ForeignKey("exercises_v2.id"), nullable=True)
    regression_id = Column(Integer, ForeignKey("exercises_v2.id"), nullable=True)
    
    # Self-referential relationships for progression/regression
    progression = relationship("ExerciseV2", remote_side=[id], foreign_keys=[progression_id], post_update=True)
    regression = relationship("ExerciseV2", remote_side=[id], foreign_keys=[regression_id], post_update=True)
