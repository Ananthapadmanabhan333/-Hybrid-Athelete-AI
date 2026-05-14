from sqlalchemy.orm import Session

class AIOrchestratorV5:
    @staticmethod
    async def get_orchestrated_summary(db: Session, user_id: int):
        from app.metabolic_engine.services import MetabolicService
        from app.performance_prediction.services import PredictionService
        from app.mental_performance_engine.services import MentalService
        from app.body_composition_engine.services import BodyCompService
        from app.modules.recovery_engine_v3.services import RecoveryServiceV3
        # 1. Fetch data from all sub-engines
        metabolic = MetabolicService.get_status(db, user_id)
        prediction = PredictionService.get_projections(db, user_id)
        mental = MentalService.get_status(db, user_id)
        body = BodyCompService.get_summary(db, user_id)
        recovery_summary = RecoveryServiceV3.get_weekly_summary(db, user_id)
        
        # 2. Synthesis Logic (Rule-based for safety)
        priority_action = "Maintain current training intensity."
        if mental and mental.get("burnout_risk", 0) > 7.5:
            priority_action = "CRITICAL: Immediate deload recommended due to burnout risk."
        elif metric_stalled := PredictionService.check_plateaus(db, user_id)["stalled_metrics"]:
            priority_action = f"Plateau detected in {metric_stalled[0]}. Adjusting volume."

        # 3. Context Compression for LLM
        compressed_context = {
            "tdee": metabolic[0].current_tdee if metabolic else 2500,
            "burnout_risk": mental["burnout_risk"] if mental else 0.0,
            "projections": prediction,
            "body_quality": body["bulk_quality"] if body else 0.0,
            "recovery_score": recovery_summary.get("total_score", 0)
        }
        
        return {
            "priority_action": priority_action,
            "summary": compressed_context,
            "health_alerts": ["Metabolic adaptation detected"] if metabolic and metabolic[0].adaptation_index < 0.8 else []
        }
