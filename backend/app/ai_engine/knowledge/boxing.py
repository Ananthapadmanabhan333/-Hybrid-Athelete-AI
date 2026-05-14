from typing import List, Dict, Any

class BoxingKnowledge:
    def get_moves(self) -> Dict[str, str]:
        return {
            "1": "Jab", "2": "Cross", "3": "Lead Hook", "4": "Rear Hook",
            "5": "Lead Uppercut", "6": "Rear Uppercut",
            "slip_L": "Slip Left", "slip_R": "Slip Right",
            "roll_L": "Roll Left", "roll_R": "Roll Right",
            "pull": "Pull", "pivot": "Pivot"
        }

    def get_combos(self, difficulty: str = "Beginner") -> List[Dict[str, Any]]:
        combos = [
            # Beginner
            {"seq": ["1", "2"], "diff": "Beginner", "type": "Fundamentals", "cost": "Low"},
            {"seq": ["1", "1", "2"], "diff": "Beginner", "type": "Rhythm", "cost": "Low"},
            {"seq": ["1", "2", "3"], "diff": "Beginner", "type": "Flow", "cost": "Low"},
            {"seq": ["1", "slip_L", "3"], "diff": "Beginner", "type": "Defense", "cost": "Low"},
            
            # Intermediate
            {"seq": ["1", "2", "roll_L", "3"], "diff": "Intermediate", "type": "Defense", "cost": "Medium"},
            {"seq": ["1", "2", "3", "2"], "diff": "Intermediate", "type": "Power", "cost": "Medium"},
            {"seq": ["1", "pull", "2", "3"], "diff": "Intermediate", "type": "Counter", "cost": "Medium"},
            {"seq": ["6", "3", "2"], "diff": "Intermediate", "type": "Inside", "cost": "High"},
            
            # Advanced
            {"seq": ["1", "slip_R", "throw_2", "roll_L", "3"], "diff": "Advanced", "type": "Technical", "cost": "High"},
            {"seq": ["1", "1", "2", "pivot", "2"], "diff": "Advanced", "type": "Footwork", "cost": "High"},
            {"seq": ["3", "roll_L", "3", "6", "roll_R", "2"], "diff": "Advanced", "type": "Inside Flow", "cost": "High"},
        ]
        return [c for c in combos if c["diff"] == difficulty]
    
    def get_tactical_drills(self, focus: str) -> List[Dict[str, Any]]:
        if focus == "Defense":
            return [
                {"name": "Wall Defense Drill", "duration": "3 min", "desc": "Back to wall, practice slipping vs shadow"},
                {"name": "Double End Bag - Head Movement", "duration": "3 min", "desc": "Focus on slipping after every punch"}
            ]
        elif focus == "Footwork":
             return [
                {"name": "Quadrant Drill", "duration": "3 min", "desc": "Move in 4 cardinal directions in stance"},
                {"name": "Circle Drill", "duration": "3 min", "desc": "Circle heavy bag, maintaining distance"}
            ]
        return [{"name": "Freestyle Shadowboxing", "duration": "3 min", "desc": "Flow state, mix everything"}]
