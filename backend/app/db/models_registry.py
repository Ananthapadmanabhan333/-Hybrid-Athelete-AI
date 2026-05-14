# Models registry for late discovery to avoid circular imports during startup
from app.models.user import User
from app.models.athlete_state import AthleteState
from app.models.injury import Injury
from app.models.training import TrainingSession
from app.models.feedback import WorkoutFeedback
from app.models.progress import ProgressHistory
from app.models.daily_log import DailyLog
from app.models.nutrition import NutritionLog, WaterLog
from app.models.chat_message import ChatMessage
from app.models.training_conversation import TrainingConversation
from app.models.daily_task import DailyTask
from app.adaptive_training_engine.models import UserWorkoutProfile, AdaptiveWorkoutSession
from app.scheduling_engine.models import UserAvailability, ScheduledActivity
from app.exercise_library_v2.models import ExerciseV2
from app.performance_tracking_engine.models import PerformanceMetric as PerformanceMetricV2, WearableData
from app.injury_awareness_engine.models import InjuryReport as InjuryReportV2, MobilityConstraint
from app.modules.nutrition_engine_v2.extension_models import MacroLoadAdjustment, NutritionCoachMessage, UserDietaryProfile

# Phase 2
from app.metabolic_engine.models import MetabolicStatus, MetabolicLog
from app.performance_prediction.models import PerformanceProjection, PlateauAlert
from app.mental_performance_engine.models import MentalState, MentalHistory
from app.body_composition_engine.models import BodyComposition
from app.pro_coach_mode.models import TrainingBlockOverride, MonthlyReport
from app.modules.performance_core.models import PerformanceSummary

from app.recovery_engine_v4.models import RecoveryLog, RecoveryScore

