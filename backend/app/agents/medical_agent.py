from fastapi import APIRouter, Depends, HTTPException
from typing import Optional, List
from pydantic import BaseModel
from app.api import deps
from app.models.user import User

router = APIRouter()

class MedicalPayload(BaseModel):
    hba1c: Optional[float] = None
    fasting_glucose: Optional[float] = None
    cholesterol_ldl: Optional[float] = None
    cholesterol_hdl: Optional[float] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    symptoms: Optional[List[str]] = []

def analyze_lab_values(lab_data: dict) -> dict:
    if not any(v is not None for k, v in lab_data.items() if k != 'symptoms'):
        return {"status": "insufficient_data", "flags": [], "risk_level": "Unknown"}
        
    risk_flags = []
    risk_score = 0
    
    hba1c = lab_data.get("hba1c")
    if hba1c:
        if hba1c > 6.5:
            risk_flags.append("High diabetes risk (HbA1c > 6.5)")
            risk_score += 3
        elif hba1c >= 5.7:
            risk_flags.append("Pre-diabetes risk (HbA1c 5.7-6.4)")
            risk_score += 1
            
    sys_bp = lab_data.get("systolic_bp")
    dia_bp = lab_data.get("diastolic_bp")
    if sys_bp and dia_bp:
        if sys_bp > 140 or dia_bp > 90:
            risk_flags.append("High Blood Pressure detected (Stage 2)")
            risk_score += 2
        elif sys_bp > 130 or dia_bp > 80:
            risk_flags.append("Elevated Blood Pressure (Stage 1)")
            risk_score += 1

    ldl = lab_data.get("cholesterol_ldl")
    if ldl and ldl > 160:
        risk_flags.append("High LDL Cholesterol")
        risk_score += 2
            
    severity = "High" if risk_score >= 3 else "Moderate" if risk_score > 0 else "Low"
    return {"status": "success", "flags": risk_flags, "severity": severity, "score": risk_score}

def generate_medical_explanation(analysis: dict) -> dict:
    # Simulates LLM structured output
    flags = analysis.get("flags", [])
    if not flags:
        return {"message": "Lab values appear within normal ranges. Maintain healthy habits."}
        
    explanation = "Based on your provided metrics, there are flags requiring attention. "
    explanation += f"Specifically: {', '.join(flags)}. "
    
    if analysis.get("severity") == "High":
        explanation += "DISCLAIMER: This system cannot diagnose or prescribe medication. Given the high risk severity, please consult a physician immediately."
    else:
        explanation += "Consider reviewing these markers with your healthcare provider during your next routine checkup."
        
    return {"message": explanation, "disclaimer": True}

@router.post("/analyze")
async def analyze_medical_data(
    payload: MedicalPayload, 
    current_user: User = Depends(deps.get_current_user)
):
    analysis = analyze_lab_values(payload.dict())
    if analysis["status"] == "insufficient_data":
        return {"analysis": analysis, "insight": {"message": "Insufficient lab data provided.", "disclaimer": False}}
        
    insight = generate_medical_explanation(analysis)
    return {"analysis": analysis, "insight": insight}
