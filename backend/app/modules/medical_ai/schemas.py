
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

class LabReportBase(BaseModel):
    report_type: str
    analysis_summary: Optional[str] = None
    extracted_data: Optional[Dict[str, Any]] = None

class LabReportCreate(LabReportBase):
    pass

class LabReport(LabReportBase):
    id: int
    user_id: int
    date: datetime
    file_path: Optional[str] = None

    class Config:
        orm_mode = True

class SymptomLogBase(BaseModel):
    symptom_name: str
    severity: int
    notes: Optional[str] = None

class SymptomLogCreate(SymptomLogBase):
    pass

class SymptomLog(SymptomLogBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        orm_mode = True
