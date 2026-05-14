from pydantic import BaseModel
from typing import List, Dict, Optional

class ExerciseV2Base(BaseModel):
    name: str
    video_url: Optional[str] = None
    instructions: List[str] = []
    muscle_groups: List[str]
    equipment_needed: List[str]
    progression_id: Optional[int] = None
    regression_id: Optional[int] = None

class ExerciseV2Create(ExerciseV2Base):
    pass

class ExerciseV2Out(ExerciseV2Base):
    id: int
    
    class Config:
        from_attributes = True

class ExerciseFilter(BaseModel):
    muscle_group: Optional[str] = None
    equipment: Optional[List[str]] = None
    search: Optional[str] = None
