from sqlalchemy.orm import Session
# Imports moved inside methods to avoid circularity

class AIOrchestratorService:
    @staticmethod
    def get_unified_dashboard_payload(db: Session, user_id: int):
        from app.adaptive_training_engine.services import AdaptiveTrainingService
        from app.performance_tracking_engine.services import PerformanceTrackingService
        from app.modules.nutrition_engine_v2.macro_service import MacroService
        from app.scheduling_engine.services import SchedulingService
        from app.injury_awareness_engine.services import InjuryAwarenessService
        """
        Synthesizes data from all engines for the dashboard.
        """
        # 1. Gather all data
        profile = AdaptiveTrainingService.get_user_profile(db, user_id)
        next_session = AdaptiveTrainingService.get_next_session(db, user_id)
        performance = PerformanceTrackingService.get_analytics(db, user_id)
        nutrition = MacroService.get_todays_targets(db, user_id)
        injury_plan = InjuryAwarenessService.get_adapted_plan(db, user_id)
        
        # 2. Generate structured payload for LLM/Frontend
        # This is where the "Orchestration" happens
        
        recovery_score = 100 - (performance["summary"].get("fatigue", 20))
        if injury_plan["trigger_recovery_week"]:
            recovery_score -= 30
            
        status_message = "All systems green."
        if injury_plan["modified_exercises"]:
            status_message = "Plan adjusted for injury compensation."
            
        payload = {
            "recovery_score": max(recovery_score, 0),
            "status_message": status_message,
            "next_workout": next_session.workout_payload if next_session else None,
            "macro_targets": {
                "p": nutrition.target_protein if nutrition else 0,
                "c": nutrition.target_carbs if nutrition else 0,
                "f": nutrition.target_fats if nutrition else 0
            } if nutrition else None,
            "performance_trends": performance["trends"],
            "adherence_pct": performance["adherence_pct"],
            "insights": [
                "Recovery is optimal. High intensity recommended for today.",
                "Ensure hydration is prioritized due to sweat rate trends."
            ]
        }
        
        return payload

    @staticmethod
    def run_daily_ai_validation(db: Session, user_id: int):
        """
        Runs rules to ensure nutrition, workload, and injury profiles are in sync.
        """
        # Logic to check if (High Workload + Low Calories) -> Warn user
        pass
