from sqlalchemy.orm import Session
from .models import PerformanceMetric, WearableData
from .schemas import WearableDataIn
from datetime import datetime, timedelta

class PerformanceTrackingService:
    @staticmethod
    def log_metric(db: Session, user_id: int, metric_type: str, key: str, value: float, unit: str = None):
        metric = PerformanceMetric(
            user_id=user_id,
            metric_type=metric_type,
            metric_key=key,
            value=value,
            unit=unit
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric

    @staticmethod
    def log_wearable(db: Session, user_id: int, data: WearableDataIn):
        db_data = WearableData(
            user_id=user_id,
            source=data.source,
            data_type=data.data_type,
            value=data.value,
            metadata_json=data.metadata_json
        )
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
        return db_data

    @staticmethod
    def get_analytics(db: Session, user_id: int):
        # Basic aggregation for analytics
        # Mocking trends and summaries
        metrics = db.query(PerformanceMetric).filter(PerformanceMetric.user_id == user_id).all()
        
        summary = {
            "total_volume_lifted": 12500.0,
            "avg_steps": 8500.0,
            "curr_strength_level": 7.5
        }
        
        trends = [
            {"date": (datetime.utcnow() - timedelta(days=i)).isoformat(), "value": 100 + i*5}
            for i in range(7)
        ]
        
        return {
            "summary": summary,
            "trends": trends,
            "adherence_pct": 92.5
        }
