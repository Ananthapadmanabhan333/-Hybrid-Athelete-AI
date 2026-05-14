from typing import List, Dict, Any, Optional

class RuleBasedEngine:
    def evaluate(
        self,
        fatigue: int,
        sleep: float,
        soreness: List[str],
        motivation: int
    ) -> Dict[str, Any]:
        
        response = {
            "recommendation": "",
            "warning": None,
            "adjusted_plan": None
        }
        
        # Rule 1: Safety First - Sleep
        if sleep < 5.0:
            response["warning"] = "CRITICAL: Sleep detected below 5 hours."
            response["recommendation"] = "Do not train heavy today. High injury risk. Recommendation: 30 mins light active recovery or full rest."
            return response
            
        # Rule 2: High Systemic Fatigue
        if fatigue >= 8:
            response["warning"] = "Systemic Fatigue High."
            response["recommendation"] = "Body is indicating overload. reduce intensity by 50% or take a complete rest day."
            return response
            
        # Rule 3: Soreness Checks
        if "legs" in [s.lower() for s in soreness]:
            response["recommendation"] = "Legs are sore. Avoid heavy squats or plyometrics. Focus on Upper Body or low-impact cardio."
            
        # Rule 4: Motivation Check
        if motivation < 3 and fatigue < 6:
            response["recommendation"] = "Motivation is low but body is fresh. Try a 'start small' approach: Commit to just 10 minutes of warm-up. You'll likely continue."
        
        if not response["recommendation"]:
            response["recommendation"] = "All systems go. Attack your training plan with intent!"
            
        return response

engine = RuleBasedEngine()
