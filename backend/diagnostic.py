import traceback
import sys
import os

# Add the current directory to sys.path to mimic uvicorn's behavior
sys.path.append(os.getcwd())

try:
    import app.main
    print("Backend imported successfully!")
except Exception:
    traceback.print_exc()
