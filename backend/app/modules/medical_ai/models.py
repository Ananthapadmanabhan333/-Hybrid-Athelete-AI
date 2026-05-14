
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from datetime import datetime
from app.db.base import Base

class LabReport(Base):
    __tablename__ = "lab_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime, default=datetime.utcnow)
    report_type = Column(String, index=True) # e.g., 'blood_panel', 'urine_analysis'
    file_path = Column(String, nullable=True) # Path to stored file
    extracted_data = Column(JSON) # JSON extracted by AI
    
    # Store AI analysis result
    analysis_summary = Column(String, nullable=True)

class SymptomLog(Base):
    __tablename__ = "symptom_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    symptom_name = Column(String, index=True)
    severity = Column(Integer) # scale 1-10
    notes = Column(String, nullable=True)
