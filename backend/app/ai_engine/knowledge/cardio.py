from typing import List, Dict, Any

class CardioKnowledge:
    PROTOCOLS = [
        {"name": "Zone 2 Base", "type": "Steady", "desc": "Keep HR at 130-150 bpm. Conversation pace.", "cns": 3},
        {"name": "VO2 Max Intervals", "type": "Interval", "desc": "4 min Hard / 3 min Rest x 4 rounds.", "cns": 8},
        {"name": "Tempo Run", "type": "Threshold", "desc": "Comfortably hard pace for 20-30 mins.", "cns": 6},
        {"name": "Tabata Sprints", "type": "HIIT", "desc": "20s Work / 10s Rest x 8 rounds.", "cns": 9},
        {"name": "Boxing Roadwork", "type": "Steady", "desc": "3-5 miles steady run + shadowboxing intervals.", "cns": 5}
    ]

    def get_protocol(self, goal: str, recovery_score: int) -> Dict[str, Any]:
        # Safety / Recovery check
        if recovery_score < 40:
            return {"name": "Recovery Walk", "type": "Rest", "desc": "30 min brisk walk.", "cns": 1}
        
        if recovery_score < 60:
            return self.PROTOCOLS[0] # Zone 2
        
        if goal == "Endurance":
            return self.PROTOCOLS[2] # Tempo
        elif goal == "Fat Loss":
            return self.PROTOCOLS[3] # Tabata
        elif goal == "Boxing":
            return self.PROTOCOLS[4] # Roadwork
            
        return self.PROTOCOLS[0]
