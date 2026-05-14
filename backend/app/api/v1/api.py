from fastapi import APIRouter
from app.api.v1.endpoints import auth, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
from app.api.v1.endpoints import training
api_router.include_router(training.router, prefix="/training", tags=["training"])
from app.api.v1.endpoints import nutrition
api_router.include_router(nutrition.router, prefix="/nutrition", tags=["nutrition"])
from app.api.v1.endpoints import recovery
api_router.include_router(recovery.router, prefix="/recovery", tags=["recovery"])
from app.api.v1.endpoints import coach
api_router.include_router(coach.router, prefix="/coach", tags=["coach"])
from app.api.v1.endpoints import tasks
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
from app.api.v1.endpoints import ai_trainer
api_router.include_router(ai_trainer.router, prefix="/ai-trainer", tags=["ai-trainer"])
from app.api.v1.endpoints import finetuning
api_router.include_router(finetuning.router, prefix="/finetuning", tags=["finetuning"])
from app.api.v1.endpoints import daily_metrics
api_router.include_router(daily_metrics.router, prefix="/daily-metrics", tags=["daily-metrics"])

# New Modules
from app.modules.performance_engine.api import router as performance_router
api_router.include_router(performance_router, prefix="/performance", tags=["performance"])

from app.modules.recovery_engine.api import router as recovery_engine_router
api_router.include_router(recovery_engine_router, prefix="/recovery-engine", tags=["recovery-engine"])

from app.modules.nutrition_engine.api import router as nutrition_engine_router
api_router.include_router(nutrition_engine_router, prefix="/nutrition-engine", tags=["nutrition-engine"])

from app.modules.medical_ai.api import router as medical_ai_router
api_router.include_router(medical_ai_router, prefix="/medical-ai", tags=["medical-ai"])

from app.modules.integrations.api import router as integrations_router
api_router.include_router(integrations_router, prefix="/integrations", tags=["integrations"])

from app.modules.community.api import router as community_router
api_router.include_router(community_router, prefix="/community", tags=["community"])

from app.modules.habit_system.api import router as habits_router
api_router.include_router(habits_router, prefix="/habits", tags=["habits"])

# Senior Architect Upgrade Routers
from app.modules.athlete_level_engine.api import router as athlete_level_router
api_router.include_router(athlete_level_router, prefix="/athlete", tags=["athlete-level"])

from app.modules.performance_forecast.api import router as forecast_router
api_router.include_router(forecast_router, prefix="/performance", tags=["forecast"]) # Merges with performance prefix

from app.modules.dashboard_engine.api import router as dashboard_router
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])

# User Request: Recovery V3
from app.modules.recovery_engine_v3.api import router as recovery_v3_router
api_router.include_router(recovery_v3_router, prefix="/recovery/v3", tags=["recovery-v3"])

# User Request: Nutrition V2
from app.modules.nutrition_engine_v2.api import router as nutrition_v2_router
api_router.include_router(nutrition_v2_router, prefix="/nutrition/v2", tags=["nutrition-v2"])

# User Request: Body Progress
from app.modules.body_progress_engine.api import router as body_progress_router
api_router.include_router(body_progress_router, prefix="/body", tags=["body-progress"])

# --- AI Upgrade System (New Modules) ---
from app.adaptive_training_engine.api import router as adaptive_training_router
api_router.include_router(adaptive_training_router, prefix="/training/adaptive", tags=["adaptive-training"])

from app.scheduling_engine.api import router as scheduling_router
api_router.include_router(scheduling_router, prefix="/schedule", tags=["scheduling-engine"])

from app.exercise_library_v2.api import router as exercise_v2_router
api_router.include_router(exercise_v2_router, prefix="/exercises/v2", tags=["exercise-library-v2"])

from app.performance_tracking_engine.api import router as performance_tracker_router
api_router.include_router(performance_tracker_router, prefix="/performance/tracker", tags=["performance-tracking"])

from app.injury_awareness_engine.api import router as injury_awareness_router
api_router.include_router(injury_awareness_router, prefix="/injury", tags=["injury-awareness"])

from app.ai_orchestrator_v4.api import router as orchestrator_router
api_router.include_router(orchestrator_router, prefix="/ai-orchestrator", tags=["ai-orchestrator"])

# --- Phase 2: Performance Intelligence Upgrades ---
from app.metabolic_engine.api import router as metabolic_router
api_router.include_router(metabolic_router, prefix="/metabolic", tags=["metabolic-engine"])

from app.performance_prediction.api import router as prediction_router
api_router.include_router(prediction_router, prefix="/performance/predict", tags=["performance-prediction"])

from app.mental_performance_engine.api import router as mental_router
api_router.include_router(mental_router, prefix="/mental", tags=["mental-performance"])

from app.body_composition_engine.api import router as body_comp_router
api_router.include_router(body_comp_router, prefix="/body/composition", tags=["body-composition"])

from app.pro_coach_mode.api import router as pro_coach_router
api_router.include_router(pro_coach_router, prefix="/coach", tags=["pro-coach"])

from app.ai_orchestrator_v5.api import router as orchestrator_v5_router
api_router.include_router(orchestrator_v5_router, prefix="/ai-orchestrator/v5", tags=["ai-orchestrator-v5"])

from app.insight_engine.api import router as insight_router
api_router.include_router(insight_router, prefix="/insights", tags=["insight-engine"])

from app.modules.performance_core.api import router as performance_core_router
api_router.include_router(performance_core_router, prefix="/performance-core", tags=["performance-core"])

from app.agents.medical_agent import router as medical_agent_router
api_router.include_router(medical_agent_router, prefix="/agents/medical", tags=["agents-medical"])

from app.agents.nutrition_agent import router as nutrition_agent_router
api_router.include_router(nutrition_agent_router, prefix="/agents/nutrition", tags=["agents-nutrition"])

from app.agents.recovery_agent import router as recovery_agent_router
api_router.include_router(recovery_agent_router, prefix="/agents/recovery", tags=["agents-recovery"])

from app.agents.agent_orchestrator import router as agent_orchestrator_router
api_router.include_router(agent_orchestrator_router, prefix="/agents", tags=["agents"])

from app.recovery_engine_v4.routes import router as recovery_engine_router
api_router.include_router(recovery_engine_router, prefix="/recovery", tags=["recovery-engine"])
