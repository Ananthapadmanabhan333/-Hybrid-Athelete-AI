from typing import List, Dict, Any

class AthleticKnowledge:
    DRILLS = [
        {"name": "A-Skips", "category": "Speed Mechanics", "intensity": "Low"},
        {"name": "B-Skips", "category": "Speed Mechanics", "intensity": "Medium"},
        {"name": "Lateral Heidens", "category": "Plyometrics", "intensity": "High"},
        {"name": "Depth Jumps", "category": "Plyometrics", "intensity": "Very High"},
        {"name": "Ladder Ickey Shuffle", "category": "Agility", "intensity": "Medium"},
        {"name": "Cone 5-10-5", "category": "Agility", "intensity": "High"},
    ]

    def get_warmup(self, intensity: str = "Standard") -> List[Dict[str, Any]]:
        if intensity == "High":
             return [d for d in self.DRILLS if d["intensity"] in ["Low", "Medium"]]
        return [d for d in self.DRILLS if d["intensity"] == "Low"]

class CardioKnowledge:
    PROTOCOLS = [
        {"name": "Zone 2 Base", "type": "Steady", "desc": "Keep HR at 130-150 bpm. Conversation pace."},
        {"name": "VO2 Max Intervals", "type": "Interval", "desc": "4 min Hard / 3 min Rest x 4 rounds."},
        {"name": "Tempo Run", "type": "Threshold", "desc": "Comfortably hard pace for 20-30 mins."},
        {"name": "Sprints", "type": "Power", "desc": "10s All Out / 50s Rest x 10 rounds."}
    ]

    def get_protocol(self, goal: str, recovery_score: int) -> Dict[str, Any]:
        if recovery_score < 50:
            return self.PROTOCOLS[0] # Zone 2
        
        if goal == "Endurance":
            return self.PROTOCOLS[2] # Tempo
        elif goal == "Fat Loss" or goal == "Speed":
            return self.PROTOCOLS[3] # Sprints
            
        return self.PROTOCOLS[0]
