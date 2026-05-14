from sqlalchemy.orm import Session
from .models import PerformanceProjection, PlateauAlert
from app.performance_tracking_engine.models import PerformanceMetric
from datetime import datetime, timedelta
import numpy as np

class PredictionService:
    @staticmethod
    def get_projections(db: Session, user_id: int):
        # Fetch last 30 days of performance data
        metrics = db.query(PerformanceMetric).filter(
            PerformanceMetric.user_id == user_id,
            PerformanceMetric.timestamp >= datetime.utcnow() - timedelta(days=30)
        ).all()
        
        if not metrics:
            return []
            
        projections = []
        # Group by metric and calculate trend
        unique_types = set(m.metric_name for m in metrics)
        
        for m_type in unique_types:
            values = [m.value for m in metrics if m.metric_name == m_type]
            if len(values) < 3: continue
            
            # Simple linear regression for projection
            x = np.arange(len(values))
            slope, intercept = np.polyfit(x, values, 1)
            
            current = values[-1]
            proj_4w = current + (slope * 4) # Assuming weekly entries
            proj_8w = current + (slope * 8)
            
            projections.append({
                "metric": m_type,
                "current": round(current, 1),
                "projection_4w": round(proj_4w, 1),
                "projection_8w": round(proj_8w, 1),
                "trend": "Increasing" if slope > 0.05 else ("Decreasing" if slope < -0.05 else "Stagnant")
            })
            
        return projections

    @staticmethod
    def check_plateaus(db: Session, user_id: int):
        # Logic to check if any metric hasn't increased in 3 weeks
        projections = PredictionService.get_projections(db, user_id)
        stalled = [p["metric"] for p in projections if p["trend"] == "Stagnant"]
        
        return {
            "stalled_metrics": stalled,
            "alert_triggered": len(stalled) > 0,
            "recommendation": "Consider a deload or changing stimulation pattern if plateau persists." if stalled else None
        }
