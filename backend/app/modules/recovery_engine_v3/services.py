
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Tuple
import numpy as np
from . import models, schemas

class RecoveryServiceV3:
    
    @staticmethod
    def calculate_score(log: schemas.RecoveryLogV3Create) -> dict:
        """
        Implements the Senior Architect's formula:
        RecoveryScore =
        (SleepQuality * 0.25) +
        (NormalizedHRV * 0.2) +
        (RHRStability * 0.15) +
        (InverseSoreness * 0.15) +
        (InverseStress * 0.15) +
        (HydrationScore * 0.1)
        """
        
        # 1. Normalize Inputs
        
        # Sleep Quality (1-10) -> 0-100
        sleep_score = (log.sleep_quality / 10.0) * 100
        
        # HRV Normalization (Mock Base: 50ms)
        # In prod, fetch 7-day baseline. For now, assume 50 is avg.
        # If HRV > 50, score > 50. Cap at 100.
        hrv_baseline = 50 
        hrv_normalized = min((log.hrv / hrv_baseline) * 50, 100) 
        
        # RHR Stability (Lower is better)
        # Mock Base: 60bpm.
        rhr_baseline = 60
        rhr_diff = abs(log.resting_heart_rate - rhr_baseline)
        # Score drops as diff increases. 0 diff = 100 score. 20 diff = 0 score.
        rhr_stability_score = max(100 - (rhr_diff * 5), 0)
        
        # Inverse Soreness (1-10, 10 is bad)
        # 1 sore = 100 score. 10 sore = 0 score.
        inv_soreness_score = (10 - log.muscle_soreness) * (100 / 9) 
        
        # Inverse Stress (1-10, 10 is bad)
        inv_stress_score = (10 - log.stress_level) * (100 / 9)
        
        # Hydration (Target ~3L)
        # 3L = 100 score. 
        hydration_score = min((log.hydration_liters / 3.0) * 100, 100)
        
        # 2. Apply Weights
        w_sleep = sleep_score * 0.25
        w_hrv = hrv_normalized * 0.20
        w_rhr = rhr_stability_score * 0.15
        w_soreness = inv_soreness_score * 0.15
        w_stress = inv_stress_score * 0.15
        w_hydration = hydration_score * 0.10
        
        total_score = w_sleep + w_hrv + w_rhr + w_soreness + w_stress + w_hydration
        
        # 3. Categorize
        if total_score >= 85:
            category = "Elite Recovery"
        elif total_score >= 70:
            category = "Ready to Train Hard"
        elif total_score >= 50:
            category = "Moderate Load"
        else:
            category = "Reduce Intensity"
            
        return {
            "total_score": round(total_score, 1),
            "category": category,
            "components": {
                "sleep": round(w_sleep, 1),
                "hrv": round(w_hrv, 1),
                "rhr": round(w_rhr, 1),
                "soreness": round(w_soreness, 1),
                "stress": round(w_stress, 1),
                "hydration": round(w_hydration, 1)
            }
        }

    @staticmethod
    def generate_recommendations(log: schemas.RecoveryLogV3Create, score: float) -> List[dict]:
        recs = []
        
        # Hydration
        if log.hydration_liters < 2.0:
            recs.append({
                "text": "Hydration is low. Aim for at least 3L today to boost recovery.",
                "type": "hydration",
                "priority": 1
            })
            
        # Mobility
        if log.muscle_soreness > 5:
            recs.append({
                "text": "High soreness detected. Perform 15 min of active mobility/stretching.",
                "type": "mobility",
                "priority": 1
            })
            
        # Stress
        if log.stress_level > 7:
             recs.append({
                "text": "High stress levels. Consider a 10 min breathwork session or meditation.",
                "type": "rest",
                "priority": 2
            })
            
        # Overall Score
        if score < 50:
             recs.append({
                "text": "Recovery is critical. Take a complete rest day or very light active recovery.",
                "type": "intensity",
                "priority": 1
            })
            
        return recs

    @staticmethod
    def get_weekly_summary(db: Session, user_id: int) -> dict:
        today = datetime.utcnow()
        week_ago = today - timedelta(days=7)
        
        logs = db.query(models.RecoveryLogV3).filter(
            models.RecoveryLogV3.user_id == user_id,
            models.RecoveryLogV3.date >= week_ago
        ).all()
        
        if not logs:
            return {"status": "No data"}
            
        avg_sleep = sum(l.sleep_duration for l in logs) / len(logs)
        avg_hrv = sum(l.hrv for l in logs) / len(logs)
        
        return {
            "avg_sleep_hours": round(avg_sleep, 1),
            "avg_hrv": round(avg_hrv, 1),
            "log_count": len(logs),
            "trend": "Stable" # Placeholder for regression logic
        }
    @staticmethod
    def get_method_impact(db: Session, user_id: int):
        logs = db.query(models.RecoveryLogV3).filter(
            models.RecoveryLogV3.user_id == user_id,
            models.RecoveryLogV3.method_used != None
        ).all()
        
        impacts = {}
        for log in logs:
            if log.method_used not in impacts:
                impacts[log.method_used] = []
            impacts[log.method_used].append(log.performance_next_day)
            
        summary = []
        for method, scores in impacts.items():
            avg_score = sum(scores) / len(scores)
            summary.append({
                "method": method,
                "avg_impact_pct": round(avg_score * 100, 1),
                "insight": f"{method} improves next-day performance by {round(avg_score * 100, 1)}%."
            })
        return summary

    @staticmethod
    def get_sleep_correlation(db: Session, user_id: int):
        # Correlate sleep hours with performance
        logs = db.query(models.RecoveryLogV3).filter(
            models.RecoveryLogV3.user_id == user_id
        ).limit(30).all()
        
        if len(logs) < 5: return "Insufficient data"
        
        sleep = [l.sleep_duration for l in logs]
        perf = [l.performance_next_day for l in logs if l.performance_next_day is not None]
        
        if len(perf) < 5: return "Insufficient data"
        
        correlation = np.corrcoef(sleep[:len(perf)], perf)[0, 1]
        
        return {
            "correlation_coefficient": round(correlation, 2),
            "insight": f"Sleep-to-strength correlation: {round(correlation * 100)}%"
        }
