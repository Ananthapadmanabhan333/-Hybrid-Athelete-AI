from sqlalchemy.orm import Session
from .models import BodyComposition
from datetime import datetime, timedelta

class BodyCompService:
    @staticmethod
    def calculate_metrics(db: Session, user_id: int, weight: float, bf_pct: float, waist: float):
        lean_mass = weight * (1 - bf_pct / 100)
        fat_mass = weight - lean_mass
        waist_ratio = waist / weight
        
        # Quality Logic
        # Fetch previous record to compare
        prev = db.query(BodyComposition).filter(
            BodyComposition.user_id == user_id
        ).order_by(BodyComposition.timestamp.desc()).first()
        
        bulk_q = 0.0
        cut_q = 0.0
        
        if prev:
            weight_diff = weight - (prev.lean_mass + prev.fat_mass)
            lean_diff = lean_mass - prev.lean_mass
            fat_diff = fat_mass - prev.fat_mass
            
            if weight_diff > 0: # Bulking
                bulk_q = lean_diff / weight_diff if weight_diff != 0 else 0
            elif weight_diff < 0: # Cutting
                cut_q = abs(fat_diff / weight_diff) if weight_diff != 0 else 0
        
        comp = BodyComposition(
            user_id=user_id,
            lean_mass=lean_mass,
            fat_mass=fat_mass,
            body_fat_pct=bf_pct,
            waist_circumference=waist,
            waist_to_weight_ratio=waist_ratio,
            bulk_quality_score=bulk_q,
            cut_quality_score=cut_q
        )
        db.add(comp)
        db.commit()
        db.refresh(comp)
        return comp

    @staticmethod
    def get_summary(db: Session, user_id: int):
        latest = db.query(BodyComposition).filter(
            BodyComposition.user_id == user_id
        ).order_by(BodyComposition.timestamp.desc()).first()
        
        if not latest: return None
        
        return {
            "lean_mass": latest.lean_mass,
            "fat_mass": latest.fat_mass,
            "body_fat_pct": latest.body_fat_pct,
            "bulk_quality": latest.bulk_quality_score,
            "cut_quality": latest.cut_quality_score,
            "waist_ratio": latest.waist_to_weight_ratio,
            "timestamp": latest.timestamp
        }
