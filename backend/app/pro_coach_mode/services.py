from sqlalchemy.orm import Session
from .models import TrainingBlockOverride, MonthlyReport
from datetime import datetime

class ProCoachService:
    @staticmethod
    def create_block_override(db: Session, user_id: int, block_name: str, constraints: dict):
        override = TrainingBlockOverride(
            user_id=user_id,
            block_name=block_name,
            constraints=constraints
        )
        db.add(override)
        db.commit()
        db.refresh(override)
        return override

    @staticmethod
    def generate_monthly_report(db: Session, user_id: int):
        # AI Summarization logic would go here
        summary = "Athlete showed 3% strength increase across main lifts. Recovery compliance is 88%."
        
        report = MonthlyReport(
            user_id=user_id,
            month_year=datetime.utcnow().strftime("%m-%Y"),
            summary_text=summary,
            data_payload={"strength_gain": 0.03, "recovery_compliance": 0.88}
        )
        db.add(report)
        db.commit()
        return report
