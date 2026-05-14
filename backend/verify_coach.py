import sys
import os
import traceback

# Add current directory to path so 'app' module can be found
sys.path.append(os.getcwd())

from app.api.deps import get_mock_user
from app.ai_engine.coach_orchestrator import CoachOrchestrator
from app.db.session import SessionLocal

# Import models to ensure registry is populated
from app.models.user import User
from app.models.chat_message import ChatMessage
from app.models.daily_log import DailyLog
from app.models.training import TrainingSession
from app.models.athlete_state import AthleteState


print("Starting verification...")

try:
    # 1. Setup Mock User
    print("Setting up user...")
    db = SessionLocal()
    user = get_mock_user(db)
    print(f"User: {user.full_name}, ID: {user.id}")
    
    # 2. Initialize Orchestrator
    print("Initializing orchestrator...")
    orch = CoachOrchestrator()
    print("Orchestrator initialized.")
    
    # 3. Process Message
    print("Processing message...")
    response = orch.process_message(user, "Hello coach", db)
    print(f"Response: {response}")
    print("SUCCESS")
    
except Exception as e:
    print("\nCRASH DETECTED:")
    traceback.print_exc()

finally:
    if 'db' in locals():
        db.close()
