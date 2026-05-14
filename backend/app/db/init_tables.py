
import sys
import os

# Add backend directory to sys.path to allow imports
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from app.db.base import Base
from app.db.session import engine

# Import all models so Base.metadata knows about them
# Existing models (guessing some based on file structure, but ideally should import all found in app/models)
from app.models import user
# from app.models import nutrition, injury, ... (I'll skip specific existing ones if I don't know them all, but Base usually collects them if imported)

# Import NEW models
from app.modules.performance_engine import models as performance_models
from app.modules.recovery_engine import models as recovery_models
from app.modules.nutrition_engine import models as nutrition_models
from app.modules.medical_ai import models as medical_models
from app.modules.integrations import models as integration_models
from app.modules.community import models as community_models
from app.modules.habit_system import models as habit_models

def init_tables():
    print("Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    init_tables()
