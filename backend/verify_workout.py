
import requests
import json
import time

# Give uvicorn a moment
time.sleep(1)

BASE_URL = "http://127.0.0.1:8001/api/v1"

def test_workout_generation():
    # Use utf-8 encoding for Windows compatibility with emojis
    with open("verification_output.txt", "w", encoding="utf-8") as f:
        f.write("Testing Strength Workout Generation...\n")
        
        payload = {
            "time_available_minutes": 60,
            "equipment_available": ["barbell", "dumbbells", "bodyweight", "bench", "cables", "machines", "pull_up_bar", "box", "kettlebells"],
            "workout_type": "Strength",
            "difficulty": "Intermediate"
        }
        
        try:
            response = requests.post(f"{BASE_URL}/ai-trainer/generate", json=payload)
            
            if response.status_code == 200:
                workout = response.json()
                exercises = workout.get("exercises", [])
                f.write(f"✅ Generated {len(exercises)} exercises!\n")
                f.write(f"Workout Title: {workout.get('title')}\n")
                
                f.write("\nExercises:\n")
                for i, ex in enumerate(exercises, 1):
                    f.write(f"{i}. {ex['name']} ({ex['sets']} sets x {ex['reps']})\n")
                    
                if len(exercises) >= 10:
                    f.write("\n✅ SUCCESS: Workout contains significantly more exercises (Target >= 10)\n")
                else:
                    f.write("\n❌ FAILURE: Workout still has few exercises.\n")
            else:
                f.write(f"❌ Error: {response.status_code} - {response.text}\n")
                
        except Exception as e:
            f.write(f"❌ Exception: {e}\n")

if __name__ == "__main__":
    test_workout_generation()
