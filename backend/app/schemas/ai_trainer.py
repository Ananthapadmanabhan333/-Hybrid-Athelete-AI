from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime

class WorkoutGenerationRequest(BaseModel):
    time_available_minutes: int = 60
    equipment_available: Optional[List[str]] = None
    workout_type: str = "General"  # Boxing, Strength, Cardio, Athletics
    difficulty: str = "Intermediate" # Beginner, Intermediate, Advanced

class ExerciseSchema(BaseModel):
    name: str
    sets: int
    reps: str
    rest: str = "60s"
    note: Optional[str] = None # Technique cues or explanations

class WorkoutResponse(BaseModel):
    title: str
    focus: str
    duration: int
    intensity: str
    reasoning: str
    exercises: List[ExerciseSchema]
    
class FeedbackCreate(BaseModel):
    training_session_id: int
    rpe: int
    enjoyment: int
    soreness_map: Dict[str, int]
