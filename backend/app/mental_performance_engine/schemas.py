from pydantic import BaseModel
from datetime import datetime

class MentalStatusOut(BaseModel):
    mood: int
    motivation: int
    burnout_risk: float
    recommendation: str

class MentalLogIn(BaseModel):
    mood: int
    motivation: int
    enjoyment: int
