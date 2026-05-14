from sqlalchemy.orm import Session
from .extension_models import NutritionCoachMessage
from .macro_service import MacroService

class NutritionCoachService:
    @staticmethod
    def chat(db: Session, user_id: int, message: str):
        # 1. Save user message
        user_msg = NutritionCoachMessage(user_id=user_id, role="user", content=message)
        db.add(user_msg)
        
        # 2. Logic to generate reply (would call OpenAI/Anthropic/Gemini in production)
        # Mocking reply for now
        reply_content = "Based on your high-intensity training today, I've increased your carbohydrate target by 50g to support glycogen replenishment. Make sure to prioritize magnesium-rich foods like spinach or almonds this evening."
        
        # 3. Save assistant reply
        assistant_msg = NutritionCoachMessage(user_id=user_id, role="assistant", content=reply_content)
        db.add(assistant_msg)
        
        db.commit()
        
        # Also potentially trigger a macro recalculation
        todays_macros = MacroService.get_todays_targets(db, user_id)
        
        return {
            "reply": reply_content,
            "suggested_macros": todays_macros
        }

    @staticmethod
    def get_recommendations(db: Session, user_id: int):
        # Placeholder for meal recommendations logic
        return [
            {"meal": "Post-Workout Bowl", "description": "Chicken, Quinoa, Sweet Potato, Spinach"},
            {"meal": "Recovery Shake", "description": "Whey Isolate, Banana, Almond Butter"}
        ]
