from datetime import datetime, timedelta
from typing import Dict, Any

class FatigueModel:
    """
    Simulates the accumulation and decay of fatigue across different bodily systems.
    Decay rates are per 24 hours.
    """
    
    DECAY_RATES = {
        "cns": 0.4,          # CNS recovers moderately fast
        "muscular_upper": 0.3, # Muscles need 48-72h
        "muscular_lower": 0.3,
        "cardio": 0.6        # Cardio recovers fast (daily)
    }
    
    IMPACT_MATRIX = {
        "boxing_heavy": {"cns": 25, "muscular_upper": 15, "cardio": 20},
        "boxing_tech": {"cns": 10, "muscular_upper": 5, "cardio": 10},
        "strength_legs": {"cns": 30, "muscular_lower": 40, "cardio": 5},
        "strength_upper": {"cns": 20, "muscular_upper": 35, "cardio": 5},
        "cardio_sprint": {"cns": 25, "muscular_lower": 20, "cardio": 30},
        "cardio_LISS": {"cns": 5, "muscular_lower": 5, "cardio": 15},
    }

    @staticmethod
    def calculate_decay(state: Dict[str, float], hours_passed: float) -> Dict[str, float]:
        """Apply exponential decay based on time passed."""
        new_state = state.copy()
        days_passed = hours_passed / 24.0
        
        for system, decay_rate in FatigueModel.DECAY_RATES.items():
            # Simple linear decay for MVP, capped at 0
            # Ideally exponential: initial * (1 - rate) ^ days
            recovery = (decay_rate * 100) * days_passed
            new_state[f"{system}_fatigue"] = max(0.0, state.get(f"{system}_fatigue", 0.0) - recovery)
            
        return new_state

    @staticmethod
    def apply_impact(state: Dict[str, float], session_type: str, rpe: int, duration_min: int) -> Dict[str, float]:
        """Apply fatigue impact from a completed session."""
        impact = FatigueModel.IMPACT_MATRIX.get(session_type, {"cns": 10, "muscular_upper": 5, "muscular_lower": 5, "cardio": 5})
        
        # Intensity Multiplier (RPE 1-10)
        intensity_mult = (rpe / 5.0) # RPE 5 is baseline, 10 is double impact
        duration_mult = (duration_min / 45.0) # 45 mins is baseline
        
        total_mult = intensity_mult * duration_mult
        
        new_state = state.copy()
        for system, base_val in impact.items():
            current = state.get(f"{system}_fatigue", 0.0)
            added = base_val * total_mult
            new_state[f"{system}_fatigue"] = min(100.0, current + added)
            
        return new_state

    @staticmethod
    def get_readiness_score(state: Dict[str, float]) -> int:
        """Returns 0-100 readiness score based on average fatigue."""
        avg_fatigue = sum([
            state.get("cns_fatigue", 0),
            state.get("muscular_upper_fatigue", 0),
            state.get("muscular_lower_fatigue", 0),
            state.get("cardio_fatigue", 0)
        ]) / 4.0
        
        return int(max(0, 100 - avg_fatigue))
