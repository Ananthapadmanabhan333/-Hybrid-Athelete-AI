from sqlalchemy.orm import Session
from app.models.user import User
from .context_manager import ContextManager
from .llm_service import LLMService
from .finetuning_service import FineTuningService
import time

class CoachOrchestrator:
    """
    Coordinates the AI Coach interaction.
    1. Builds Context
    2. Constructs Prompt
    3. Routes to best available LLM (Mistral → Gemini → G4F → keyword)
    """
    
    def __init__(self):
        self.llm = LLMService()
        try:
            self.finetuning = FineTuningService()
        except Exception as e:
            print(f"Fine-tuning service not available: {e}")
            self.finetuning = None

    def process_message(self, user: User, message: str, db: Session) -> str:
        # 1. Gather Context
        context_str = ContextManager.build_context(user, db)
        
        # 2. Build structured context dict for Mistral adapter routing
        context_dict = self._build_context_dict(user, context_str)

        # 3. System Prompt (used by Gemini/G4F fallbacks)
        system_prompt = f"""
        You are 'Hybrid Coach', an elite AI performance coach for a hybrid athlete application.
        Your goal is to provide specific, actionable, and empathetic advice based on the user's data.
        
        CONTEXT DATA:
        {context_str}
        
        GUIDELINES:
        - Be concise but professional.
        - If fatigue is high (>80%), RECOMMEND REST or Active Recovery.
        - Support goals of Strength, Boxing, and Endurance.
        - Answer directly. Do not say "As an AI...".
        """
        
        # 4. Generate Response — Mistral adapter takes priority if loaded
        start_time = time.time()
        response = self.llm.generate_response(
            system_prompt=system_prompt,
            user_message=message,
            agent="coach",          # Routes to coach_adapter if Mistral is available
            context=context_dict,   # Structured athlete data for prompt injection
        )
        response_time_ms = (time.time() - start_time) * 1000
        
        # 5. Log conversation for fine-tuning (if available)
        if self.finetuning:
            try:
                self.finetuning.log_conversation(
                    db=db,
                    user_id=user.id,
                    user_message=message,
                    ai_response=response,
                    system_prompt=system_prompt,
                    user_context=context_dict,
                    response_time_ms=response_time_ms
                )
            except Exception as e:
                print(f"Failed to log conversation: {e}")
        
        return response

    @staticmethod
    def _build_context_dict(user: User, context_str: str) -> dict:
        """
        Build a lightweight structured dict for Mistral prompt injection.
        Falls back to minimal dict if user attributes are not populated.
        """
        ctx = {
            "athlete_name": getattr(user, "full_name", "athlete"),
            "weight_kg": getattr(user, "current_weight_kg", None),
            "activity_level": getattr(user, "activity_level", None),
            "fitness_goal": getattr(user, "fitness_goal", "hybrid_athlete"),
        }
        # Strip None values to keep prompt clean
        return {k: v for k, v in ctx.items() if v is not None}
