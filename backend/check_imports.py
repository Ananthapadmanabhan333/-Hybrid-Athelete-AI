
import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from app.db.session import engine
    print("Base Engine Import Success")
    from app.modules.performance_engine import models
    print("Performance Import Success")
except Exception as e:
    print(f"Error: {e}")
