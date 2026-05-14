from typing import List, Dict, Any
from .knowledge import KnowledgeBase
import random

class WorkoutGenerator:
    """
    Generates adaptive daily workouts based on Athlete State using the Expert Knowledge Base.
    """
    
    kb = KnowledgeBase()

    @staticmethod
    def generate_session(
        state: Dict[str, float], 
        equipment: List[str], 
        time_available: int,
        blocked_movements: List[str] = [],
        workout_type: str = "General",
        difficulty: str = "Intermediate"
    ) -> Dict[str, Any]:
        
        cns = state.get("cns_fatigue", 0)
        
        # 1. Safety Check: If CNS is critically high, force Active Recovery
        if cns > 80:
            return WorkoutGenerator._build_recovery_session(time_available)

        # 2. Route to Domain-Specific Generator
        if workout_type == "Boxing":
            return WorkoutGenerator._build_boxing_session(difficulty, time_available, cns)
        elif workout_type == "Strength":
            # Auto-determine split based on fatigue if not specified
            focus = "Full Body"
            upper = state.get("muscular_upper_fatigue", 0)
            lower = state.get("muscular_lower_fatigue", 0)
            if lower < 40 and upper > 40: focus = "Lower Body Strength"
            elif upper < 40 and lower > 40: focus = "Upper Body Strength"
            
            return WorkoutGenerator._build_strength_session(focus, equipment, time_available, blocked_movements, difficulty)
        elif workout_type == "Athletics":
            return WorkoutGenerator._build_athletic_session(difficulty, time_available, cns, blocked_movements)
        elif workout_type == "Cardio":
            return WorkoutGenerator._build_cardio_session(difficulty, time_available, cns)
        
        # Default / Fallback
        return WorkoutGenerator._build_strength_session("Full Body", equipment, time_available, blocked_movements, difficulty)

    @staticmethod
    def _build_boxing_session(difficulty: str, duration: int, cns: float) -> Dict[str, Any]:
        exercises = []
        
        # Difficulty-specific parameters
        if difficulty == "Beginner":
            rounds = 3
            round_duration = "2 min"
            rest_between = "1 min"
            num_combos = 3
            intensity = "Moderate"
        elif difficulty == "Advanced":
            rounds = 6
            round_duration = "3 min"
            rest_between = "45s"
            num_combos = 5
            intensity = "Very High"
        else:  # Intermediate
            rounds = 5
            round_duration = "3 min"
            rest_between = "1 min"
            num_combos = 4
            intensity = "High"
        
        # Warmup - More comprehensive
        exercises.append({"name": "Jump Rope", "sets": 2 if difficulty == "Beginner" else 3, "reps": round_duration, "rest": "1 min", "note": "Rhythm & Cardio"})
        exercises.append({"name": "Shadowboxing (Loose)", "sets": 1, "reps": "3 min", "rest": "1 min", "note": "Flow, no power"})
        exercises.append({"name": "Dynamic Stretches", "sets": 1, "reps": "5 min", "rest": "0s", "note": "Arm circles, leg swings, torso twists"})
        
        # Skill Block (Combos) - More combinations
        combos = WorkoutGenerator.kb.boxing.get_combos(difficulty)
        for c in combos[:num_combos]: 
            exercises.append({
                "name": f"Combo: {'-'.join(c['seq'])}", 
                "sets": rounds, 
                "reps": round_duration, 
                "rest": rest_between,
                "note": f"{c['type']} - {c['cost']} Cost"
            })
            
        # Defense / Tactical
        if difficulty != "Beginner":
            drills = WorkoutGenerator.kb.boxing.get_tactical_drills("Defense")
            exercises.extend([{"name": d["name"], "sets": 3, "reps": d["duration"], "rest": "1 min", "note": d["desc"]} for d in drills[:2]])
        
        # Heavy Bag Work
        exercises.append({"name": "Heavy Bag Power Rounds", "sets": 3, "reps": "2 min", "rest": "1 min", "note": "Focus on power and technique"})
        
        # Speed Work
        exercises.append({"name": "Speed Bag", "sets": 3, "reps": "1 min", "rest": "30s", "note": "Hand-eye coordination"})
        
        # Conditioning finisher
        if difficulty == "Advanced":
            exercises.append({"name": "Burpees", "sets": 3, "reps": "15", "rest": "45s", "note": "Explosive conditioning"})
            exercises.append({"name": "Mountain Climbers", "sets": 3, "reps": "30s", "rest": "30s", "note": "Core & cardio"})
        else:
            exercises.append({"name": "Burpees", "sets": 2, "reps": "10", "rest": "1 min", "note": "Conditioning"})
        
        # Cool down
        exercises.append({"name": "Light Shadowboxing", "sets": 1, "reps": "2 min", "rest": "0s", "note": "Cool down, technique focus"})
        
        return {
            "title": f"{difficulty} Boxing Session",
            "focus": "Skill & Conditioning",
            "duration": duration,
            "exercises": exercises,
            "intensity": intensity,
            "reasoning": f"{difficulty} boxing program with {num_combos} combinations, {rounds} rounds per drill, and comprehensive conditioning. Total exercises: {len(exercises)}"
        }

        
    @staticmethod
    def _build_strength_session(focus: str, equipment: List[str], duration: int, blocked: List[str], difficulty: str) -> Dict[str, Any]:
        """
        Builds a professional-grade strength session with proper periodization.
        Structure: Warmup -> Primary Compound (Strength) -> Secondary (Hypertrophy) -> Accessories -> Core
        """
        exercises = []
        
        # 1. Professional Volume Parameters
        if difficulty == "Beginner":
            vol = {"main_sets": 3, "main_reps": "5-8", "sec_sets": 3, "sec_reps": "8-10", "acc_sets": 2, "acc_reps": "12-15"}
            intensity = "Moderate"
            rest = {"compound": "2-3 min", "accessory": "60-90s"}
        elif difficulty == "Advanced":
            vol = {"main_sets": 5, "main_reps": "3-5", "sec_sets": 4, "sec_reps": "6-8", "acc_sets": 3, "acc_reps": "10-12"}
            intensity = "High (RPE 8-9)"
            rest = {"compound": "3-5 min", "accessory": "90s"}
        else:  # Intermediate
            vol = {"main_sets": 4, "main_reps": "5-6", "sec_sets": 3, "sec_reps": "8-12", "acc_sets": 3, "acc_reps": "10-15"}
            intensity = "Moderate-High (RPE 7-8)"
            rest = {"compound": "2-3 min", "accessory": "60-90s"}
        
        # 2. Dynamic Warmup (Specific to focus)
        warmup_drills = []
        if "Lower" in focus or "Leg" in focus or "Full" in focus:
            warmup_drills.extend(["90/90 Hip Switch", "World's Greatest Stretch"])
        if "Upper" in focus or "Push" in focus or "Pull" in focus or "Full" in focus:
            warmup_drills.extend(["Band Pull Aparts", "Thoracic Rotations"])
            
        exercises.append({
            "name": "Dynamic Warmup Sequence", 
            "sets": 1, 
            "reps": "5-8 min", 
            "rest": "0s", 
            "note": f"Flow through: {', '.join(warmup_drills)}. Increase body temp."
        })
        
        # 3. Retrieve & Filter Exercises
        all_moves = WorkoutGenerator.kb.strength.get_exercises(focus, equipment, blocked)
        
        # Categorize
        compounds = [e for e in all_moves if e["type"] == "Compound"]
        isolations = [e for e in all_moves if e["type"] != "Compound"]
        
        random.shuffle(compounds)
        random.shuffle(isolations)
        
        # 4. Select Primary Lift (The "Money" Lift)
        # Prioritize matching the exact focus (e.g. Squat for Legs)
        primary = None
        if compounds:
            # Simple heuristic: First compound is usually the biggest movement
            primary = compounds[0]
            exercises.append({
                "name": primary["name"],
                "sets": vol["main_sets"],
                "reps": vol["main_reps"],
                "rest": rest["compound"],
                "note": f"PRIMARY STRENGTH. Focus on perfect form. {intensity}."
            })
            
        # 5. Select Secondary Lift (Assistance/Variation)
        secondary = None
        if len(compounds) > 1:
            # Try to find a compound that hits the secondary muscle of the primary or same muscle different angle
            secondary = next((e for e in compounds[1:] if e["muscle"] == primary["muscle"] or e["muscle"] in primary.get("secondary", [])), compounds[1])
            exercises.append({
                "name": secondary["name"],
                "sets": vol["sec_sets"],
                "reps": vol["sec_reps"],
                "rest": rest["compound"],
                "note": "HYPERTROPHY. Control the eccentric (lowering) phase."
            })
        
        # 5b. Add a third compound for advanced/intermediate
        if len(compounds) > 2 and difficulty in ["Intermediate", "Advanced"]:
            tertiary = compounds[2]
            exercises.append({
                "name": tertiary["name"],
                "sets": 3,
                "reps": "8-10",
                "rest": rest["compound"],
                "note": "VOLUME WORK. Maintain good form throughout."
            })

        # 6. Accessories (Isolation / Weak Points)
        # We want more accessories for a complete workout
        target_acc_count = 3 if difficulty == "Beginner" else 4
        if difficulty == "Advanced": target_acc_count = 5
        
        chosen_accs = []
        # Filter isolations to avoid hitting the same muscle too many times if possible, or prioritize if it's a weak point
        # For now, just take the first few distinct ones
        for acc in isolations:
            if len(chosen_accs) >= target_acc_count:
                break
            if acc["name"] not in [e["name"] for e in exercises]: # Avoid dupe names
                chosen_accs.append(acc)
                
        for acc in chosen_accs:
            exercises.append({
                "name": acc["name"],
                "sets": vol["acc_sets"],
                "reps": vol["acc_reps"],
                "rest": rest["accessory"],
                "note": f"Target {acc['muscle']}. Squeeze at the top."
            })
            
        # 7. Core / Finisher - Add 2 core exercises instead of 1
        core_moves = [e for e in WorkoutGenerator.kb.strength.get_exercises("Core", equipment, blocked)]
        if core_moves:
            # First core exercise
            finisher = core_moves[0]
            exercises.append({
                "name": finisher["name"],
                "sets": 3,
                "reps": "15-20" if finisher["type"] != "Iso" else "45-60s",
                "rest": "60s",
                "note": "Core Stability."
            })
            
            # Second core exercise for variety
            if len(core_moves) > 1:
                finisher2 = core_moves[1]
                exercises.append({
                    "name": finisher2["name"],
                    "sets": 3,
                    "reps": "12-15" if finisher2["type"] != "Iso" else "30-45s",
                    "rest": "45s",
                    "note": "Core Strength."
                })

        return {
            "title": f"Pro {focus} - {difficulty}",
            "focus": focus,
            "duration": duration,
            "exercises": exercises,
            "intensity": intensity,
            "reasoning": f"Professional programming: {primary['name'] if primary else 'Main Lift'} for strength, followed by volume work for {secondary['name'] if secondary else 'assistance'}. Total exercises: {len(exercises)}"
        }


    @staticmethod
    def _build_athletic_session(difficulty: str, duration: int, cns: float, blocked: List[str]) -> Dict[str, Any]:
        exercises = []
        # Dynamic Warmup
        warmups = WorkoutGenerator.kb.athletic.get_warmup("Standard")
        exercises.extend([{"name": d["name"], "sets": 2, "reps": "20 yards", "rest": "0s", "note": "Dynamic Warmup"} for d in warmups])
        
        # Power / Plyo
        if cns < 60: # Only if fresh
            exercises.append({"name": "Box Jumps", "sets": 3, "reps": "5", "rest": "2 min", "note": "Max Height"})
            exercises.append({"name": "Med Ball Slams", "sets": 3, "reps": "8", "rest": "90s", "note": "Explosive Power"})
        
        # Speed / Agility
        exercises.append({"name": "Ladder Drills", "sets": 4, "reps": "45s", "rest": "1 min", "note": "Foot speed"})
        
        return {
            "title": f"{difficulty} Athletic Performance",
            "focus": "Power & Agility",
            "duration": duration,
            "exercises": exercises,
            "intensity": "High",
            "reasoning": "Focusing on explosive power and multidirectional speed."
        }

    @staticmethod
    def _build_cardio_session(difficulty: str, duration: int, cns: float) -> Dict[str, Any]:
        # Difficulty-specific cardio programming
        if difficulty == "Beginner":
            protocol = WorkoutGenerator.kb.cardio.get_protocol("Endurance", 100-cns)
            exercises = [
                {"name": "Walking Warmup", "sets": 1, "reps": "5 min", "rest": "0s", "note": "Easy pace"},
                {"name": protocol["name"], "sets": 1, "reps": f"{duration-10} min", "rest": "0s", "note": protocol["desc"]},
                {"name": "Cool Down Walk", "sets": 1, "reps": "5 min", "rest": "0s", "note": "Recovery"}
            ]
            intensity = "Low-Moderate"
            reasoning = f"Beginner-friendly steady-state cardio. Build aerobic base with {protocol['name']}."
        elif difficulty == "Advanced":
            protocol = WorkoutGenerator.kb.cardio.get_protocol("Fat Loss", 100-cns)
            exercises = [
                {"name": "Dynamic Warmup", "sets": 1, "reps": "5 min", "rest": "0s", "note": "Prep for intensity"},
                {"name": "HIIT Intervals", "sets": 8, "reps": "30s work / 30s rest", "rest": "0s", "note": "Max effort sprints"},
                {"name": protocol["name"], "sets": 1, "reps": f"{duration-20} min", "rest": "0s", "note": protocol["desc"]},
                {"name": "Active Recovery", "sets": 1, "reps": "5 min", "rest": "0s", "note": "Light movement"}
            ]
            intensity = "Very High"
            reasoning = f"Advanced HIIT protocol with {protocol['name']}. High calorie burn and conditioning."
        else:  # Intermediate
            protocol = WorkoutGenerator.kb.cardio.get_protocol("Fat Loss" if cns < 50 else "Endurance", 100-cns)
            exercises = [
                {"name": "Warmup", "sets": 1, "reps": "5 min", "rest": "0s", "note": "Gradual intensity build"},
                {"name": "Tempo Intervals", "sets": 4, "reps": "3 min work / 2 min easy", "rest": "0s", "note": "Moderate-high effort"},
                {"name": protocol["name"], "sets": 1, "reps": f"{duration-25} min", "rest": "0s", "note": protocol["desc"]},
                {"name": "Cool Down", "sets": 1, "reps": "5 min", "rest": "0s", "note": "Easy pace"}
            ]
            intensity = "Moderate-High"
            reasoning = f"Intermediate cardio with tempo work and {protocol['name']}. Balanced conditioning."
        
        return {
            "title": f"{difficulty} {protocol['name']}",
            "focus": protocol["type"],
            "duration": duration,
            "exercises": exercises,
            "intensity": intensity,
            "reasoning": reasoning
        }

    @staticmethod
    def _build_recovery_session(duration: int) -> Dict[str, Any]:
        return {
            "title": "Active Recovery",
            "focus": "Mobility & Flow",
            "duration": duration,
            "exercises": [
                {"name": "Dynamic Stretching", "sets": 1, "reps": "5 min", "rest": "0s", "note": "Flow"},
                {"name": "Foam Rolling", "sets": 1, "reps": "10 min", "rest": "0s", "note": "Myofascial Release"},
                {"name": "Light Yoga Flow", "sets": 1, "reps": "10 min", "rest": "0s", "note": "Decompression"}
            ],
            "intensity": "Low",
            "reasoning": "High CNS fatigue detected. Focus on restoration."
        }
