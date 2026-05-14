from sqlalchemy.orm import Session
from .models import InjuryReport, MobilityConstraint
from .schemas import InjuryReportIn
from datetime import datetime

class InjuryAwarenessService:
    @staticmethod
    def report_injury(db: Session, user_id: int, report_in: InjuryReportIn):
        report = InjuryReport(
            user_id=user_id,
            affected_area=report_in.affected_area,
            pain_level=report_in.pain_level,
            notes=report_in.notes
        )
        db.add(report)
        db.commit()
        db.refresh(report)
        return report

    @staticmethod
    def get_adapted_plan(db: Session, user_id: int):
        # 1. Fetch active injuries
        active_injuries = db.query(InjuryReport).filter(
            InjuryReport.user_id == user_id,
            InjuryReport.is_active == True
        ).all()
        
        # 2. Logic to determine adaptations
        modified_exercises = []
        recommendation = "Stay active but avoid heavy loading on joints."
        trigger_recovery = False
        
        if any(i.pain_level >= 7 for i in active_injuries):
            recommendation = "Severe pain detected. Recommending a mobility-only week."
            trigger_recovery = True
            
        # Mock substitution logic
        for injury in active_injuries:
            if "shoulder" in injury.affected_area:
                modified_exercises.append({
                    "original": "Overhead Press",
                    "substituted": "Lateral Raises (Low weight)",
                    "reason": "Reduce vertical loading on shoulder joint"
                })
        
        return {
            "modified_exercises": modified_exercises,
            "recommendation": recommendation,
            "trigger_recovery_week": trigger_recovery
        }

    @staticmethod
    def check_recovery_trigger(stress_score: float, hrv: float, soreness: int):
        # Stress (0-100), HRV (ms), Soreness (1-10)
        if stress_score > 80 and hrv < 40 and soreness > 7:
            return True
        return False
