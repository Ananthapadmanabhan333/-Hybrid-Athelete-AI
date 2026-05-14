from sqlalchemy.orm import Session
from .extension_models import MacroLoadAdjustment, UserDietaryProfile
from datetime import datetime

class MacroService:
    @staticmethod
    def calculate_targets(db: Session, user_id: int, intensity: str):
        # Base logic for macro calculation
        # Protein: 2g/kg, Fats: 0.8g/kg, Carbs fill the rest
        # Medium Intensity: +10% Calories
        # High Intensity: +20% Calories (mostly Carbs)
        
        # In a real app, query User and Profile for weight/height
        weight_kg = 80.0 # Placeholder
        
        protein = weight_kg * 2.2
        fats = weight_kg * 0.9
        base_cals = 2500
        
        if intensity == "medium":
            base_cals *= 1.1
        elif intensity == "high":
            base_cals *= 1.25
            
        remaining_cals = base_cals - (protein * 4) - (fats * 9)
        carbs = max(remaining_cals / 4, 50.0)
        
        adjustment = MacroLoadAdjustment(
            user_id=user_id,
            training_intensity=intensity,
            target_protein=round(protein, 1),
            target_carbs=round(carbs, 1),
            target_fats=round(fats, 1),
            target_calories=int(base_cals),
            micronutrient_targets={"magnesium": "400mg", "zinc": "15mg"}
        )
        db.add(adjustment)
        db.commit()
        db.refresh(adjustment)
        return adjustment

    @staticmethod
    def get_todays_targets(db: Session, user_id: int):
        return db.query(MacroLoadAdjustment).filter(
            MacroLoadAdjustment.user_id == user_id
        ).order_by(MacroLoadAdjustment.date.desc()).first()
