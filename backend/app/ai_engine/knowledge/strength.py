from typing import List, Dict, Any

class StrengthKnowledge:
    EXERCISE_DB = [
        # ===== CHEST EXERCISES =====
        {"name": "Barbell Bench Press", "type": "Compound", "muscle": "Chest", "secondary": ["Triceps", "Shoulders"], "cns": 8, "flags": ["shoulder", "wrist"], "subs": ["DB Bench", "Machine Press"]},
        {"name": "Incline Barbell Bench Press", "type": "Compound", "muscle": "Chest", "secondary": ["Shoulders", "Triceps"], "cns": 8, "flags": ["shoulder"], "subs": ["Incline DB Press"]},
        {"name": "Decline Bench Press", "type": "Compound", "muscle": "Chest", "secondary": ["Triceps"], "cns": 7, "flags": ["shoulder"], "subs": ["Decline DB Press"]},
        {"name": "Dumbbell Bench Press", "type": "Compound", "muscle": "Chest", "secondary": ["Triceps", "Shoulders"], "cns": 7, "flags": ["shoulder"], "subs": ["Barbell Bench"]},
        {"name": "Incline Dumbbell Press", "type": "Compound", "muscle": "Chest", "secondary": ["Shoulders"], "cns": 7, "flags": ["shoulder"], "subs": ["Incline Barbell"]},
        {"name": "Decline Dumbbell Press", "type": "Compound", "muscle": "Chest", "secondary": ["Triceps"], "cns": 7, "flags": ["shoulder"], "subs": ["Decline Barbell"]},
        {"name": "Chest Dips", "type": "Compound", "muscle": "Chest", "secondary": ["Triceps"], "cns": 7, "flags": ["shoulder"], "subs": ["Machine Chest Press"]},
        {"name": "Cable Flyes", "type": "Isolation", "muscle": "Chest", "secondary": [], "cns": 4, "flags": ["shoulder"], "subs": ["DB Flyes"]},
        {"name": "Dumbbell Flyes", "type": "Isolation", "muscle": "Chest", "secondary": [], "cns": 4, "flags": ["shoulder"], "subs": ["Cable Flyes"]},
        {"name": "Incline Cable Flyes", "type": "Isolation", "muscle": "Chest", "secondary": [], "cns": 4, "flags": ["shoulder"], "subs": ["Incline DB Flyes"]},
        {"name": "Incline Dumbbell Flyes", "type": "Isolation", "muscle": "Chest", "secondary": [], "cns": 4, "flags": ["shoulder"], "subs": ["Cable Flyes"]},
        {"name": "Pec Deck Machine", "type": "Isolation", "muscle": "Chest", "secondary": [], "cns": 3, "flags": ["shoulder"], "subs": ["Cable Flyes"]},
        {"name": "Machine Chest Press", "type": "Compound", "muscle": "Chest", "secondary": ["Triceps"], "cns": 5, "flags": ["shoulder"], "subs": ["DB Bench"]},
        {"name": "Pushups", "type": "Bodyweight", "muscle": "Chest", "secondary": ["Core"], "cns": 4, "flags": ["wrist"], "subs": ["Knee Pushups"]},
        {"name": "Weighted Pushups", "type": "Bodyweight", "muscle": "Chest", "secondary": ["Core"], "cns": 6, "flags": ["wrist"], "subs": ["Regular Pushups"]},
        {"name": "Diamond Pushups", "type": "Bodyweight", "muscle": "Triceps", "secondary": ["Chest"], "cns": 5, "flags": ["wrist", "elbow"], "subs": ["Regular Pushups"]},
        {"name": "Svend Press", "type": "Isolation", "muscle": "Chest", "secondary": [], "cns": 3, "flags": ["shoulder"], "subs": ["Cable Flyes"]},
        
        # ===== BACK EXERCISES =====
        {"name": "Deadlift", "type": "Compound", "muscle": "Posterior Chain", "secondary": ["Back", "Grip"], "cns": 10, "flags": ["lower_back", "hip"], "subs": ["Romanian Deadlift", "Trap Bar DL"]},
        {"name": "Sumo Deadlift", "type": "Compound", "muscle": "Posterior Chain", "secondary": ["Quads"], "cns": 9, "flags": ["lower_back", "hip"], "subs": ["Conventional Deadlift"]},
        {"name": "Trap Bar Deadlift", "type": "Compound", "muscle": "Posterior Chain", "secondary": ["Quads"], "cns": 8, "flags": ["lower_back"], "subs": ["Deadlift"]},
        {"name": "Barbell Row", "type": "Compound", "muscle": "Back", "secondary": ["Biceps"], "cns": 7, "flags": ["lower_back"], "subs": ["Chest Supported Row"]},
        {"name": "Pendlay Row", "type": "Compound", "muscle": "Back", "secondary": ["Biceps"], "cns": 8, "flags": ["lower_back"], "subs": ["Barbell Row"]},
        {"name": "Dumbbell Row", "type": "Unilateral", "muscle": "Back", "secondary": ["Biceps"], "cns": 6, "flags": [], "subs": ["Cable Row"]},
        {"name": "T-Bar Row", "type": "Compound", "muscle": "Back", "secondary": ["Biceps"], "cns": 7, "flags": ["lower_back"], "subs": ["DB Row"]},
        {"name": "Meadows Row", "type": "Unilateral", "muscle": "Back", "secondary": ["Biceps"], "cns": 6, "flags": [], "subs": ["DB Row"]},
        {"name": "Seal Row", "type": "Compound", "muscle": "Back", "secondary": ["Biceps"], "cns": 6, "flags": [], "subs": ["Chest Supported Row"]},
        {"name": "Pullups", "type": "Bodyweight", "muscle": "Lats", "secondary": ["Biceps"], "cns": 7, "flags": ["shoulder", "elbow"], "subs": ["Lat Pulldown"]},
        {"name": "Chinups", "type": "Bodyweight", "muscle": "Lats", "secondary": ["Biceps"], "cns": 7, "flags": ["shoulder", "elbow"], "subs": ["Underhand Lat Pulldown"]},
        {"name": "Weighted Pullups", "type": "Compound", "muscle": "Lats", "secondary": ["Biceps"], "cns": 8, "flags": ["shoulder"], "subs": ["Pullups"]},
        {"name": "Weighted Chinups", "type": "Compound", "muscle": "Lats", "secondary": ["Biceps"], "cns": 8, "flags": ["shoulder"], "subs": ["Chinups"]},
        {"name": "Lat Pulldown", "type": "Compound", "muscle": "Lats", "secondary": ["Biceps"], "cns": 5, "flags": ["shoulder"], "subs": ["Band Pulldown"]},
        {"name": "Wide Grip Lat Pulldown", "type": "Compound", "muscle": "Lats", "secondary": ["Biceps"], "cns": 5, "flags": ["shoulder"], "subs": ["Lat Pulldown"]},
        {"name": "Close Grip Lat Pulldown", "type": "Compound", "muscle": "Lats", "secondary": ["Biceps"], "cns": 5, "flags": ["shoulder"], "subs": ["Lat Pulldown"]},
        {"name": "Cable Row", "type": "Compound", "muscle": "Back", "secondary": ["Biceps"], "cns": 5, "flags": [], "subs": ["DB Row"]},
        {"name": "Seated Cable Row", "type": "Compound", "muscle": "Back", "secondary": ["Biceps"], "cns": 5, "flags": [], "subs": ["Cable Row"]},
        {"name": "Single Arm Cable Row", "type": "Unilateral", "muscle": "Back", "secondary": ["Biceps"], "cns": 5, "flags": [], "subs": ["DB Row"]},
        {"name": "Face Pulls", "type": "Isolation", "muscle": "Rear Delts", "secondary": ["Upper Back"], "cns": 3, "flags": [], "subs": ["Band Pull Apart"]},
        {"name": "Chest Supported Row", "type": "Compound", "muscle": "Back", "secondary": ["Biceps"], "cns": 6, "flags": [], "subs": ["DB Row"]},
        {"name": "Inverted Row", "type": "Bodyweight", "muscle": "Back", "secondary": ["Biceps"], "cns": 5, "flags": [], "subs": ["Cable Row"]},
        {"name": "Rack Pulls", "type": "Compound", "muscle": "Back", "secondary": ["Traps"], "cns": 8, "flags": ["lower_back"], "subs": ["Deadlift"]},
        {"name": "Shrugs", "type": "Isolation", "muscle": "Traps", "secondary": [], "cns": 4, "flags": [], "subs": ["Dumbbell Shrugs"]},
        {"name": "Dumbbell Shrugs", "type": "Isolation", "muscle": "Traps", "secondary": [], "cns": 4, "flags": [], "subs": ["Barbell Shrugs"]},
        
        # ===== SHOULDER EXERCISES =====
        {"name": "Overhead Press", "type": "Compound", "muscle": "Shoulders", "secondary": ["Triceps", "Core"], "cns": 8, "flags": ["shoulder", "lower_back"], "subs": ["DB Seated Press"]},
        {"name": "Push Press", "type": "Compound", "muscle": "Shoulders", "secondary": ["Triceps", "Legs"], "cns": 8, "flags": ["shoulder", "lower_back"], "subs": ["Overhead Press"]},
        {"name": "Seated Dumbbell Press", "type": "Compound", "muscle": "Shoulders", "secondary": ["Triceps"], "cns": 7, "flags": ["shoulder"], "subs": ["Machine Shoulder Press"]},
        {"name": "Standing Dumbbell Press", "type": "Compound", "muscle": "Shoulders", "secondary": ["Triceps", "Core"], "cns": 7, "flags": ["shoulder"], "subs": ["Seated DB Press"]},
        {"name": "Arnold Press", "type": "Compound", "muscle": "Shoulders", "secondary": ["Triceps"], "cns": 6, "flags": ["shoulder"], "subs": ["DB Press"]},
        {"name": "Machine Shoulder Press", "type": "Compound", "muscle": "Shoulders", "secondary": ["Triceps"], "cns": 5, "flags": ["shoulder"], "subs": ["DB Press"]},
        {"name": "Lateral Raises", "type": "Isolation", "muscle": "Shoulders", "secondary": [], "cns": 3, "flags": ["shoulder"], "subs": ["Cable Lateral Raise"]},
        {"name": "Cable Lateral Raises", "type": "Isolation", "muscle": "Shoulders", "secondary": [], "cns": 3, "flags": ["shoulder"], "subs": ["DB Lateral Raise"]},
        {"name": "Leaning Lateral Raises", "type": "Isolation", "muscle": "Shoulders", "secondary": [], "cns": 3, "flags": ["shoulder"], "subs": ["Lateral Raises"]},
        {"name": "Front Raises", "type": "Isolation", "muscle": "Shoulders", "secondary": [], "cns": 3, "flags": ["shoulder"], "subs": ["Plate Raise"]},
        {"name": "Plate Front Raises", "type": "Isolation", "muscle": "Shoulders", "secondary": [], "cns": 3, "flags": ["shoulder"], "subs": ["DB Front Raise"]},
        {"name": "Rear Delt Flyes", "type": "Isolation", "muscle": "Rear Delts", "secondary": [], "cns": 3, "flags": ["shoulder"], "subs": ["Face Pulls"]},
        {"name": "Reverse Pec Deck", "type": "Isolation", "muscle": "Rear Delts", "secondary": [], "cns": 3, "flags": ["shoulder"], "subs": ["Rear Delt Flyes"]},
        {"name": "Upright Row", "type": "Compound", "muscle": "Shoulders", "secondary": ["Traps"], "cns": 5, "flags": ["shoulder"], "subs": ["Cable Upright Row"]},
        {"name": "Landmine Press", "type": "Compound", "muscle": "Shoulders", "secondary": ["Core"], "cns": 6, "flags": [], "subs": ["DB Press"]},
        {"name": "Viking Press", "type": "Compound", "muscle": "Shoulders", "secondary": ["Triceps"], "cns": 7, "flags": ["shoulder"], "subs": ["Landmine Press"]},
        {"name": "Bradford Press", "type": "Compound", "muscle": "Shoulders", "secondary": ["Triceps"], "cns": 6, "flags": ["shoulder"], "subs": ["Overhead Press"]},
        
        # ===== ARM EXERCISES =====
        {"name": "Barbell Curl", "type": "Isolation", "muscle": "Biceps", "secondary": [], "cns": 4, "flags": ["elbow"], "subs": ["DB Curl"]},
        {"name": "EZ Bar Curl", "type": "Isolation", "muscle": "Biceps", "secondary": [], "cns": 4, "flags": ["elbow"], "subs": ["Barbell Curl"]},
        {"name": "Dumbbell Curl", "type": "Isolation", "muscle": "Biceps", "secondary": [], "cns": 4, "flags": ["elbow"], "subs": ["Cable Curl"]},
        {"name": "Alternating Dumbbell Curl", "type": "Isolation", "muscle": "Biceps", "secondary": [], "cns": 4, "flags": ["elbow"], "subs": ["DB Curl"]},
        {"name": "Hammer Curl", "type": "Isolation", "muscle": "Biceps", "secondary": ["Forearms"], "cns": 4, "flags": ["elbow"], "subs": ["DB Curl"]},
        {"name": "Cross Body Hammer Curl", "type": "Isolation", "muscle": "Biceps", "secondary": ["Forearms"], "cns": 4, "flags": ["elbow"], "subs": ["Hammer Curl"]},
        {"name": "Preacher Curl", "type": "Isolation", "muscle": "Biceps", "secondary": [], "cns": 4, "flags": ["elbow"], "subs": ["Cable Curl"]},
        {"name": "Cable Curl", "type": "Isolation", "muscle": "Biceps", "secondary": [], "cns": 3, "flags": ["elbow"], "subs": ["DB Curl"]},
        {"name": "Concentration Curl", "type": "Isolation", "muscle": "Biceps", "secondary": [], "cns": 3, "flags": ["elbow"], "subs": ["DB Curl"]},
        {"name": "Incline Dumbbell Curl", "type": "Isolation", "muscle": "Biceps", "secondary": [], "cns": 4, "flags": ["elbow"], "subs": ["DB Curl"]},
        {"name": "Spider Curl", "type": "Isolation", "muscle": "Biceps", "secondary": [], "cns": 4, "flags": ["elbow"], "subs": ["Preacher Curl"]},
        {"name": "Close Grip Bench Press", "type": "Compound", "muscle": "Triceps", "secondary": ["Chest"], "cns": 7, "flags": ["shoulder", "elbow"], "subs": ["Dips"]},
        {"name": "Tricep Dips", "type": "Compound", "muscle": "Triceps", "secondary": ["Chest"], "cns": 7, "flags": ["shoulder", "elbow"], "subs": ["Tricep Pushdown"]},
        {"name": "Weighted Tricep Dips", "type": "Compound", "muscle": "Triceps", "secondary": ["Chest"], "cns": 8, "flags": ["shoulder", "elbow"], "subs": ["Tricep Dips"]},
        {"name": "Tricep Pushdown", "type": "Isolation", "muscle": "Triceps", "secondary": [], "cns": 3, "flags": ["elbow"], "subs": ["Overhead Extension"]},
        {"name": "Rope Tricep Pushdown", "type": "Isolation", "muscle": "Triceps", "secondary": [], "cns": 3, "flags": ["elbow"], "subs": ["Tricep Pushdown"]},
        {"name": "Overhead Tricep Extension", "type": "Isolation", "muscle": "Triceps", "secondary": [], "cns": 4, "flags": ["elbow", "shoulder"], "subs": ["Tricep Pushdown"]},
        {"name": "Skull Crushers", "type": "Isolation", "muscle": "Triceps", "secondary": [], "cns": 5, "flags": ["elbow"], "subs": ["Tricep Pushdown"]},
        {"name": "Dumbbell Tricep Extension", "type": "Isolation", "muscle": "Triceps", "secondary": [], "cns": 4, "flags": ["elbow"], "subs": ["Overhead Extension"]},
        {"name": "Cable Overhead Extension", "type": "Isolation", "muscle": "Triceps", "secondary": [], "cns": 3, "flags": ["elbow"], "subs": ["Overhead Extension"]},
        {"name": "Tricep Kickback", "type": "Isolation", "muscle": "Triceps", "secondary": [], "cns": 3, "flags": ["elbow"], "subs": ["Tricep Pushdown"]},
        
        # ===== LEG EXERCISES =====
        {"name": "Back Squat", "type": "Compound", "muscle": "Quads", "secondary": ["Glutes", "Core"], "cns": 9, "flags": ["knee", "lower_back"], "subs": ["Goblet Squat", "Leg Press"]},
        {"name": "Front Squat", "type": "Compound", "muscle": "Quads", "secondary": ["Core"], "cns": 9, "flags": ["knee", "wrist"], "subs": ["Goblet Squat"]},
        {"name": "High Bar Squat", "type": "Compound", "muscle": "Quads", "secondary": ["Glutes"], "cns": 9, "flags": ["knee", "lower_back"], "subs": ["Back Squat"]},
        {"name": "Low Bar Squat", "type": "Compound", "muscle": "Posterior Chain", "secondary": ["Quads"], "cns": 9, "flags": ["knee", "lower_back"], "subs": ["Back Squat"]},
        {"name": "Pause Squat", "type": "Compound", "muscle": "Quads", "secondary": ["Glutes"], "cns": 9, "flags": ["knee", "lower_back"], "subs": ["Back Squat"]},
        {"name": "Box Squat", "type": "Compound", "muscle": "Quads", "secondary": ["Glutes"], "cns": 8, "flags": ["knee", "lower_back"], "subs": ["Back Squat"]},
        {"name": "Goblet Squat", "type": "Compound", "muscle": "Quads", "secondary": ["Glutes"], "cns": 6, "flags": ["knee"], "subs": ["Bodyweight Squat"]},
        {"name": "Zercher Squat", "type": "Compound", "muscle": "Quads", "secondary": ["Core"], "cns": 8, "flags": ["knee", "lower_back"], "subs": ["Front Squat"]},
        {"name": "Bulgarian Split Squat", "type": "Unilateral", "muscle": "Quads", "secondary": ["Glutes"], "cns": 7, "flags": ["knee", "ankle"], "subs": ["Lunges"]},
        {"name": "Walking Lunges", "type": "Unilateral", "muscle": "Glutes", "secondary": ["Quads"], "cns": 6, "flags": ["knee", "ankle"], "subs": ["Step Ups"]},
        {"name": "Reverse Lunges", "type": "Unilateral", "muscle": "Glutes", "secondary": ["Quads"], "cns": 6, "flags": ["knee"], "subs": ["Step Ups"]},
        {"name": "Forward Lunges", "type": "Unilateral", "muscle": "Quads", "secondary": ["Glutes"], "cns": 6, "flags": ["knee"], "subs": ["Reverse Lunges"]},
        {"name": "Dumbbell Lunges", "type": "Unilateral", "muscle": "Quads", "secondary": ["Glutes"], "cns": 6, "flags": ["knee"], "subs": ["Bodyweight Lunges"]},
        {"name": "Leg Press", "type": "Compound", "muscle": "Quads", "secondary": ["Glutes"], "cns": 6, "flags": ["knee"], "subs": ["Goblet Squat"]},
        {"name": "Hack Squat", "type": "Compound", "muscle": "Quads", "secondary": [], "cns": 7, "flags": ["knee"], "subs": ["Leg Press"]},
        {"name": "Smith Machine Squat", "type": "Compound", "muscle": "Quads", "secondary": ["Glutes"], "cns": 6, "flags": ["knee"], "subs": ["Back Squat"]},
        {"name": "Romanian Deadlift", "type": "Compound", "muscle": "Hamstrings", "secondary": ["Glutes"], "cns": 7, "flags": ["lower_back", "hamstring"], "subs": ["Leg Curl"]},
        {"name": "Stiff Leg Deadlift", "type": "Compound", "muscle": "Hamstrings", "secondary": ["Lower Back"], "cns": 7, "flags": ["lower_back", "hamstring"], "subs": ["RDL"]},
        {"name": "Single Leg RDL", "type": "Unilateral", "muscle": "Hamstrings", "secondary": ["Glutes"], "cns": 6, "flags": ["hamstring"], "subs": ["RDL"]},
        {"name": "Leg Curl", "type": "Isolation", "muscle": "Hamstrings", "secondary": [], "cns": 3, "flags": ["hamstring"], "subs": ["Nordic Curl"]},
        {"name": "Seated Leg Curl", "type": "Isolation", "muscle": "Hamstrings", "secondary": [], "cns": 3, "flags": ["hamstring"], "subs": ["Lying Leg Curl"]},
        {"name": "Lying Leg Curl", "type": "Isolation", "muscle": "Hamstrings", "secondary": [], "cns": 3, "flags": ["hamstring"], "subs": ["Seated Leg Curl"]},
        {"name": "Nordic Hamstring Curl", "type": "Bodyweight", "muscle": "Hamstrings", "secondary": [], "cns": 6, "flags": ["hamstring"], "subs": ["Leg Curl"]},
        {"name": "Good Morning", "type": "Compound", "muscle": "Hamstrings", "secondary": ["Lower Back"], "cns": 7, "flags": ["lower_back"], "subs": ["RDL"]},
        {"name": "Hip Thrust", "type": "Compound", "muscle": "Glutes", "secondary": ["Hamstrings"], "cns": 6, "flags": ["hip"], "subs": ["Glute Bridge"]},
        {"name": "Barbell Hip Thrust", "type": "Compound", "muscle": "Glutes", "secondary": ["Hamstrings"], "cns": 7, "flags": ["hip"], "subs": ["Hip Thrust"]},
        {"name": "Barbell Glute Bridge", "type": "Compound", "muscle": "Glutes", "secondary": ["Hamstrings"], "cns": 5, "flags": ["hip"], "subs": ["Bodyweight Bridge"]},
        {"name": "Single Leg Hip Thrust", "type": "Unilateral", "muscle": "Glutes", "secondary": ["Hamstrings"], "cns": 6, "flags": ["hip"], "subs": ["Hip Thrust"]},
        {"name": "Cable Pull Through", "type": "Compound", "muscle": "Glutes", "secondary": ["Hamstrings"], "cns": 5, "flags": ["hip"], "subs": ["Hip Thrust"]},
        {"name": "Leg Extension", "type": "Isolation", "muscle": "Quads", "secondary": [], "cns": 3, "flags": ["knee"], "subs": ["Goblet Squat"]},
        {"name": "Single Leg Extension", "type": "Isolation", "muscle": "Quads", "secondary": [], "cns": 3, "flags": ["knee"], "subs": ["Leg Extension"]},
        {"name": "Step Ups", "type": "Unilateral", "muscle": "Quads", "secondary": ["Glutes"], "cns": 5, "flags": ["knee"], "subs": ["Lunges"]},
        {"name": "Dumbbell Step Ups", "type": "Unilateral", "muscle": "Quads", "secondary": ["Glutes"], "cns": 6, "flags": ["knee"], "subs": ["Step Ups"]},
        {"name": "Calf Raises", "type": "Isolation", "muscle": "Calves", "secondary": [], "cns": 3, "flags": ["ankle"], "subs": ["Seated Calf Raise"]},
        {"name": "Standing Calf Raises", "type": "Isolation", "muscle": "Calves", "secondary": [], "cns": 3, "flags": ["ankle"], "subs": ["Seated Calf Raise"]},
        {"name": "Seated Calf Raises", "type": "Isolation", "muscle": "Calves", "secondary": [], "cns": 3, "flags": ["ankle"], "subs": ["Standing Calf Raise"]},
        
        # ===== CORE EXERCISES =====
        {"name": "Plank", "type": "Iso", "muscle": "Core", "secondary": [], "cns": 3, "flags": [], "subs": ["Deadbug"]},
        {"name": "Side Plank", "type": "Iso", "muscle": "Obliques", "secondary": [], "cns": 3, "flags": [], "subs": ["Russian Twist"]},
        {"name": "Weighted Plank", "type": "Iso", "muscle": "Core", "secondary": [], "cns": 4, "flags": [], "subs": ["Plank"]},
        {"name": "Hanging Leg Raise", "type": "Bodyweight", "muscle": "Abs", "secondary": ["Hip Flexors"], "cns": 5, "flags": ["shoulder"], "subs": ["Lying Leg Raise"]},
        {"name": "Hanging Knee Raise", "type": "Bodyweight", "muscle": "Abs", "secondary": ["Hip Flexors"], "cns": 4, "flags": ["shoulder"], "subs": ["Lying Leg Raise"]},
        {"name": "Lying Leg Raise", "type": "Bodyweight", "muscle": "Abs", "secondary": [], "cns": 3, "flags": [], "subs": ["Crunches"]},
        {"name": "Cable Crunch", "type": "Isolation", "muscle": "Abs", "secondary": [], "cns": 3, "flags": [], "subs": ["Crunch"]},
        {"name": "Crunches", "type": "Bodyweight", "muscle": "Abs", "secondary": [], "cns": 2, "flags": [], "subs": ["Plank"]},
        {"name": "Ab Wheel Rollout", "type": "Compound", "muscle": "Core", "secondary": ["Shoulders"], "cns": 6, "flags": ["lower_back"], "subs": ["Plank"]},
        {"name": "Russian Twist", "type": "Isolation", "muscle": "Obliques", "secondary": [], "cns": 3, "flags": [], "subs": ["Side Plank"]},
        {"name": "Weighted Russian Twist", "type": "Isolation", "muscle": "Obliques", "secondary": [], "cns": 4, "flags": [], "subs": ["Russian Twist"]},
        {"name": "Pallof Press", "type": "Iso", "muscle": "Core", "secondary": ["Obliques"], "cns": 4, "flags": [], "subs": ["Plank"]},
        {"name": "Deadbug", "type": "Bodyweight", "muscle": "Core", "secondary": [], "cns": 3, "flags": [], "subs": ["Plank"]},
        {"name": "Bird Dog", "type": "Bodyweight", "muscle": "Core", "secondary": ["Lower Back"], "cns": 3, "flags": [], "subs": ["Plank"]},
        {"name": "Mountain Climbers", "type": "Bodyweight", "muscle": "Core", "secondary": ["Cardio"], "cns": 4, "flags": [], "subs": ["Plank"]},
        {"name": "Bicycle Crunches", "type": "Bodyweight", "muscle": "Abs", "secondary": ["Obliques"], "cns": 3, "flags": [], "subs": ["Crunches"]},
        {"name": "Woodchoppers", "type": "Isolation", "muscle": "Obliques", "secondary": [], "cns": 3, "flags": [], "subs": ["Russian Twist"]},
        {"name": "Landmine Rotation", "type": "Compound", "muscle": "Obliques", "secondary": ["Core"], "cns": 5, "flags": [], "subs": ["Russian Twist"]},
        
        # ===== OLYMPIC & POWER =====
        {"name": "Power Clean", "type": "Olympic", "muscle": "Full Body", "secondary": ["Traps", "Shoulders"], "cns": 9, "flags": ["wrist", "shoulder"], "subs": ["Hang Clean"]},
        {"name": "Hang Clean", "type": "Olympic", "muscle": "Full Body", "secondary": ["Traps"], "cns": 8, "flags": ["wrist"], "subs": ["KB Swing"]},
        {"name": "Clean and Jerk", "type": "Olympic", "muscle": "Full Body", "secondary": ["Shoulders"], "cns": 10, "flags": ["wrist", "shoulder"], "subs": ["Power Clean"]},
        {"name": "Snatch", "type": "Olympic", "muscle": "Full Body", "secondary": ["Shoulders"], "cns": 10, "flags": ["wrist", "shoulder"], "subs": ["Power Clean"]},
        {"name": "Hang Snatch", "type": "Olympic", "muscle": "Full Body", "secondary": ["Shoulders"], "cns": 9, "flags": ["wrist", "shoulder"], "subs": ["Hang Clean"]},
        {"name": "Kettlebell Swing", "type": "Power", "muscle": "Posterior Chain", "secondary": ["Shoulders"], "cns": 6, "flags": ["lower_back"], "subs": ["RDL"]},
        {"name": "Kettlebell Snatch", "type": "Power", "muscle": "Full Body", "secondary": ["Shoulders"], "cns": 7, "flags": ["shoulder"], "subs": ["KB Swing"]},
        {"name": "Box Jump", "type": "Plyometric", "muscle": "Legs", "secondary": ["Glutes"], "cns": 6, "flags": ["knee", "ankle"], "subs": ["Jump Squat"]},
        {"name": "Depth Jump", "type": "Plyometric", "muscle": "Legs", "secondary": ["Glutes"], "cns": 7, "flags": ["knee", "ankle"], "subs": ["Box Jump"]},
        {"name": "Broad Jump", "type": "Plyometric", "muscle": "Legs", "secondary": ["Glutes"], "cns": 6, "flags": ["knee", "ankle"], "subs": ["Box Jump"]},
        {"name": "Medicine Ball Slam", "type": "Power", "muscle": "Full Body", "secondary": ["Core"], "cns": 5, "flags": [], "subs": ["KB Swing"]},
        {"name": "Battle Ropes", "type": "Power", "muscle": "Shoulders", "secondary": ["Core", "Cardio"], "cns": 5, "flags": ["shoulder"], "subs": ["KB Swing"]},
    ]


    def get_exercises(self, focus: str, equipment: List[str], blocked_flags: List[str]) -> List[Dict[str, Any]]:
        valid = []
        for ex in self.EXERCISE_DB:
            # 1. Check Injury Flags
            if any(flag in blocked_flags for flag in ex["flags"]):
                continue
            
            # 2. Check Equipment (Simple heuristic)
            if "Barbell" in ex["name"] and "barbell" not in equipment: continue
            if "DB" in ex["name"] or "Dumbbell" in ex["name"]:
                if "dumbbells" not in equipment: continue
            if "Cable" in ex["name"] and "cables" not in equipment: continue
            if "Machine" in ex["name"] and "machines" not in equipment: continue
            if "Kettlebell" in ex["name"] or "KB" in ex["name"]:
                if "kettlebells" not in equipment: continue
            
            # 3. Check Focus
            if focus == "Upper Body Strength":
                if ex["muscle"] in ["Chest", "Shoulders", "Back", "Lats", "Triceps", "Biceps", "Rear Delts"]: 
                    valid.append(ex)
            elif focus == "Lower Body Strength":
                if ex["muscle"] in ["Quads", "Hamstrings", "Glutes", "Calves", "Legs", "Posterior Chain"]: 
                    valid.append(ex)
            elif focus == "Push":
                if ex["muscle"] in ["Chest", "Shoulders", "Triceps"]:
                    valid.append(ex)
            elif focus == "Pull":
                if ex["muscle"] in ["Back", "Lats", "Biceps", "Rear Delts"]:
                    valid.append(ex)
            elif focus == "Legs":
                if ex["muscle"] in ["Quads", "Hamstrings", "Glutes", "Calves", "Legs"]:
                    valid.append(ex)
            elif focus == "Full Body":
                valid.append(ex)
            elif focus == "Core":
                if ex["muscle"] in ["Core", "Abs", "Obliques"]:
                    valid.append(ex)
                
        return valid

    def get_substitute(self, exercise_name: str) -> str:
        for ex in self.EXERCISE_DB:
            if ex["name"] == exercise_name:
                return ex["subs"][0] if ex["subs"] else "Rest"
        return "Rest"
