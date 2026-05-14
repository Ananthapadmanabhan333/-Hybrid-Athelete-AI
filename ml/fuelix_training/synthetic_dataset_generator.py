"""
synthetic_dataset_generator.py
-------------------------------
Generates large-scale synthetic coaching datasets for all four Fuelix
LoRA adapters: coach, nutrition, recovery, medical.

Each sample is in instruction format:
  { "instruction": "...", "context": {...}, "response": "..." }

Rule: The model NEVER invents metrics. Context is always provided.
      If context is empty, response = "insufficient_data".
"""

import json
import random
import os
import argparse
from typing import List, Dict, Any

# ─────────────────────────── SEEDED RNG ────────────────────────────
random.seed(42)

# ══════════════════════════════════════════════════════════════════
#  COACH ADAPTER TEMPLATES
# ══════════════════════════════════════════════════════════════════

COACH_INSTRUCTIONS = [
    "Why am I feeling fatigued after training?",
    "Should I train today based on my recovery?",
    "What type of session should I do today?",
    "How do I improve my boxing performance?",
    "Give me a strength and conditioning plan for this week.",
    "How should I balance boxing and weightlifting?",
    "What does my training load indicate about overtraining?",
    "How do I peak for a boxing competition?",
    "My CNS fatigue is high. What should I do?",
    "How can I improve my cardio without losing muscle?",
    "What is hybrid training and how should I program it?",
    "Should I deload this week?",
    "How do I improve my VO2 Max while maintaining strength?",
    "What intensity should I train at given my recovery score?",
    "Is my training frequency optimal for a hybrid athlete?",
    "How do I structure my training week for boxing and powerlifting?",
    "What are signs of overreaching vs overtraining?",
    "How should I modify my training given high muscular soreness?",
    "Can I do HIIT and heavy lifting in the same week?",
    "What is the best way to track hybrid athlete progress?",
]

COACH_CONTEXTS = [
    {"recovery_score": random.randint(30, 100),
     "sleep_hours": round(random.uniform(4, 9), 1),
     "training_load": random.choice(["low", "moderate", "high", "very_high"]),
     "cns_fatigue": random.randint(10, 95),
     "goal": random.choice(["hybrid_athlete", "boxing_performance", "strength_focused", "endurance"]),
     "sessions_this_week": random.randint(0, 7)}
    for _ in range(500)
]

def generate_coach_response(ctx: Dict) -> str:
    rs = ctx.get("recovery_score", 0)
    sleep = ctx.get("sleep_hours", 0)
    load = ctx.get("training_load", "unknown")
    cns = ctx.get("cns_fatigue", 0)
    goal = ctx.get("goal", "hybrid_athlete")

    if rs < 40:
        return (
            f"With a recovery score of {rs}/100, your body is under significant stress. "
            f"Your CNS fatigue at {cns}% and only {sleep} hours of sleep are key contributors. "
            "I strongly recommend a full rest day or light mobility session only. "
            "Avoid high-intensity training until your recovery score exceeds 55."
        )
    elif rs < 65:
        return (
            f"Recovery score: {rs}/100 — moderate recovery. "
            f"With {sleep}h sleep and {load} training load, you can train today but keep "
            "intensity at 65-70% of your maximum. Prioritize technique work over heavy loading. "
            f"For a {goal} athlete, focus on skill-based sessions rather than volume today."
        )
    else:
        return (
            f"Excellent recovery score of {rs}/100. Sleep at {sleep}h has primed your CNS well. "
            f"Given {load} training load and your goal of {goal}, today is optimal for "
            "high-intensity work. It's a strong day for progressive overload or sparring sessions."
        )


# ══════════════════════════════════════════════════════════════════
#  NUTRITION ADAPTER TEMPLATES
# ══════════════════════════════════════════════════════════════════

NUTRITION_INSTRUCTIONS = [
    "Analyze my protein intake for this week.",
    "Am I in a calorie surplus or deficit?",
    "Why is my weight trend increasing despite training hard?",
    "How can I improve my protein compliance?",
    "What should I eat for recovery after a hard session?",
    "How does my nutrition relate to my recovery score?",
    "Am I eating enough for hybrid athlete performance?",
    "How can I optimize my macros for muscle gain and endurance?",
    "What are the signs of under-fueling for a hybrid athlete?",
    "Should I adjust my calorie target given my current weight trend?",
    "How much protein do I need per day as a hybrid athlete?",
    "What is my current nutrition compliance level?",
    "How do my eating habits affect my fatigue levels?",
    "Give me a meal strategy for my goal.",
    "What nutrition gaps do I have this week?",
]

def build_nutrition_context() -> Dict:
    avg_protein = random.randint(60, 200)
    avg_cals = random.randint(1500, 3500)
    target_protein = 150
    target_cals = 2500
    return {
        "goal": random.choice(["hybrid_muscle_gain", "fat_loss_performance", "endurance_base"]),
        "avg_daily_protein_g": avg_protein,
        "avg_daily_calories": avg_cals,
        "protein_compliance_pct": round((avg_protein / target_protein) * 100, 1),
        "calorie_surplus_deficit": avg_cals - target_cals,
        "weight_trend": random.choice(["increasing", "stable", "decreasing"]),
        "recovery_score": random.randint(30, 100),
        "hydration_adherence_pct": random.randint(40, 100),
    }

def generate_nutrition_response(ctx: Dict) -> str:
    p = ctx.get("avg_daily_protein_g", 0)
    compliance = ctx.get("protein_compliance_pct", 0)
    surplus = ctx.get("calorie_surplus_deficit", 0)
    trend = ctx.get("weight_trend", "stable")
    goal = ctx.get("goal", "hybrid_muscle_gain")

    parts = []
    if compliance < 70:
        parts.append(
            f"Protein compliance is critically low at {compliance}%. "
            f"You're averaging only {p}g/day against a target of 150g. "
            "Prioritize lean protein sources at every meal: chicken, eggs, Greek yogurt, or whey."
        )
    elif compliance < 90:
        parts.append(
            f"Protein at {p}g/day ({compliance}% compliance) — close but not optimal. "
            "Add one protein-focused snack daily to close the gap."
        )
    else:
        parts.append(f"Protein compliance is excellent at {compliance}% ({p}g/day). Keep it up.")

    if surplus > 300:
        parts.append(
            f"You are in a {surplus}kcal surplus. For {goal}, this is appropriate for muscle building "
            "but monitor body composition to ensure you are not gaining excess fat."
        )
    elif surplus < -300:
        parts.append(
            f"Calorie deficit of {abs(surplus)}kcal detected. For {goal}, this deficit "
            "may impair recovery and performance. Consider increasing carbohydrate intake on training days."
        )
    else:
        parts.append("Calorie balance is near maintenance — well controlled.")

    return " ".join(parts)


# ══════════════════════════════════════════════════════════════════
#  RECOVERY ADAPTER TEMPLATES
# ══════════════════════════════════════════════════════════════════

RECOVERY_INSTRUCTIONS = [
    "What does my recovery score mean?",
    "How should I train given my current recovery status?",
    "Why is my recovery score low despite sleeping 8 hours?",
    "How does sleep affect my recovery as a hybrid athlete?",
    "What recovery protocols should I follow post heavy training?",
    "My HRV is low today. How does this affect my training?",
    "What is the relationship between training load and recovery?",
    "How many rest days do I need per week?",
    "How do I interpret a fatigue flag of 'reduce_intensity'?",
    "What active recovery techniques are best for hybrid athletes?",
    "Should I skip training if my recovery score is below 50?",
    "How long does it take to recover from a high-volume training week?",
]

def build_recovery_context() -> Dict:
    return {
        "recovery_score": random.randint(20, 100),
        "sleep_hours": round(random.uniform(3.5, 9.5), 1),
        "sleep_quality": random.choice(["poor", "fair", "good", "excellent"]),
        "fatigue_flag": random.choice(["reduce_intensity", "moderate_load", "full_go"]),
        "training_load_yesterday": random.choice(["rest", "low", "moderate", "high", "very_high"]),
        "soreness_level": random.randint(1, 10),
        "cns_fatigue_pct": random.randint(10, 95),
    }

def generate_recovery_response(ctx: Dict) -> str:
    rs = ctx.get("recovery_score", 0)
    flag = ctx.get("fatigue_flag", "moderate_load")
    sleep = ctx.get("sleep_hours", 0)
    soreness = ctx.get("soreness_level", 0)
    cns = ctx.get("cns_fatigue_pct", 0)

    if flag == "reduce_intensity":
        return (
            f"Recovery score of {rs}/100 with {sleep}h of sleep and soreness at {soreness}/10 "
            f"indicates significant accumulated fatigue (CNS at {cns}%). "
            "Today's recommendation: active recovery only. Focus on 20-30 minutes of low-intensity "
            "movement — mobility work, yoga, or a slow walk. Avoid any resistance training or sparring. "
            "Prioritize nutrition and sleep quality tonight."
        )
    elif flag == "moderate_load":
        return (
            f"Recovery at {rs}/100 — moderate state. Sleep of {sleep}h is adequate but not optimal. "
            f"Soreness level {soreness}/10 suggests residual muscle fatigue. "
            "You can train today at 65-75% intensity. Avoid maximal efforts. "
            "Prioritize compound movements with reduced volume."
        )
    else:
        return (
            f"Recovery score {rs}/100 — excellent readiness. {sleep}h sleep and low soreness ({soreness}/10) "
            f"indicate full recovery. CNS fatigue at {cns}% is manageable. "
            "Today is optimal for high-intensity training, sparring or PR attempts."
        )


# ══════════════════════════════════════════════════════════════════
#  MEDICAL ADAPTER TEMPLATES
# ══════════════════════════════════════════════════════════════════

MEDICAL_INSTRUCTIONS = [
    "What does my HbA1c result mean for an athlete?",
    "Is my blood pressure normal for someone who trains intensely?",
    "What do elevated LDL cholesterol levels mean?",
    "How does high blood pressure affect my athletic performance?",
    "Should I be concerned about my lab values?",
    "What lifestyle changes can improve my metabolic health markers?",
    "How does high HbA1c affect endurance performance?",
    "What is pre-diabetes and how does it affect training?",
    "Explain my cholesterol profile in relation to training.",
    "Are my cardiovascular risk markers concerning?",
    "How do I manage blood pressure as an athlete?",
]

def build_medical_context() -> Dict:
    return {
        "hba1c": round(random.uniform(4.5, 9.0), 1),
        "fasting_glucose": random.randint(70, 200),
        "cholesterol_ldl": random.randint(80, 220),
        "cholesterol_hdl": random.randint(30, 90),
        "systolic_bp": random.randint(100, 165),
        "diastolic_bp": random.randint(60, 105),
        "risk_flags": [],
    }

def generate_medical_response(ctx: Dict) -> str:
    hba1c = ctx.get("hba1c", 5.0)
    ldl = ctx.get("cholesterol_ldl", 100)
    sys_bp = ctx.get("systolic_bp", 120)
    dia_bp = ctx.get("diastolic_bp", 80)

    notes = []
    disclaimer = (
        "\n\nDISCLAIMER: This is an informational explanation only. "
        "This system cannot diagnose conditions or prescribe treatment. "
        "Please consult a licensed physician for medical advice."
    )

    if hba1c >= 6.5:
        notes.append(
            f"HbA1c of {hba1c}% exceeds the diagnostic threshold for type 2 diabetes (≥6.5%). "
            "As an athlete, this can impair glucose regulation during endurance training and recovery. "
            "Please consult your physician immediately."
        )
    elif hba1c >= 5.7:
        notes.append(
            f"HbA1c of {hba1c}% falls in the pre-diabetes range (5.7-6.4%). "
            "Regular aerobic exercise and dietary management can improve insulin sensitivity. "
            "This is manageable but requires monitoring."
        )

    if sys_bp > 140 or dia_bp > 90:
        notes.append(
            f"Blood pressure of {sys_bp}/{dia_bp} mmHg is elevated (Stage 2 hypertension). "
            "Intense exercise at this level carries cardiovascular risk. Seek medical review before continuing high-intensity training."
        )
    elif sys_bp > 130 or dia_bp > 80:
        notes.append(
            f"Blood pressure of {sys_bp}/{dia_bp} mmHg indicates Stage 1 hypertension. "
            "Monitor closely. Manage through sodium reduction, stress reduction, and aerobic conditioning."
        )

    if ldl > 160:
        notes.append(
            f"LDL cholesterol of {ldl} mg/dL is above optimal. "
            "Dietary adjustments — reducing saturated fats, increasing omega-3 intake — are recommended."
        )

    if not notes:
        return "Your provided lab values appear within normal ranges for an active individual. Maintain your current healthy habits and continue regular monitoring."

    return " ".join(notes) + disclaimer


# ══════════════════════════════════════════════════════════════════
#  CORE GENERATOR
# ══════════════════════════════════════════════════════════════════

def generate_samples(domain: str, count: int) -> List[Dict[str, Any]]:
    samples = []
    print(f"  Generating {count:,} samples for domain: {domain}")

    for i in range(count):
        if domain == "coach":
            instruction = random.choice(COACH_INSTRUCTIONS)
            ctx = random.choice(COACH_CONTEXTS).copy()
            # Vary context slightly per sample
            ctx["recovery_score"] = random.randint(20, 100)
            ctx["sleep_hours"] = round(random.uniform(3.5, 9.5), 1)
            ctx["training_load"] = random.choice(["low", "moderate", "high", "very_high"])
            ctx["cns_fatigue"] = random.randint(10, 95)
            response = generate_coach_response(ctx)

        elif domain == "nutrition":
            instruction = random.choice(NUTRITION_INSTRUCTIONS)
            ctx = build_nutrition_context()
            response = generate_nutrition_response(ctx)

        elif domain == "recovery":
            instruction = random.choice(RECOVERY_INSTRUCTIONS)
            ctx = build_recovery_context()
            response = generate_recovery_response(ctx)

        elif domain == "medical":
            instruction = random.choice(MEDICAL_INSTRUCTIONS)
            ctx = build_medical_context()
            response = generate_medical_response(ctx)
        else:
            raise ValueError(f"Unknown domain: {domain}")

        samples.append({
            "instruction": instruction,
            "context": ctx,
            "response": response
        })

        if (i + 1) % 100_000 == 0:
            print(f"    → {i + 1:,} / {count:,} generated")

    return samples


def write_jsonl(samples: List[Dict], path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"  ✓ Written {len(samples):,} samples → {path}")


def main():
    parser = argparse.ArgumentParser(description="Fuelix Synthetic Dataset Generator")
    parser.add_argument("--domain", type=str, default="all",
                        choices=["all", "coach", "nutrition", "recovery", "medical"],
                        help="Which domain to generate")
    parser.add_argument("--scale", type=float, default=1.0,
                        help="Scale factor for sample counts (0.01 = 1%, 1.0 = full)")
    parser.add_argument("--output_dir", type=str, default="datasets",
                        help="Output directory for JSONL files")
    args = parser.parse_args()

    # Full target counts from spec
    TARGET_COUNTS = {
        "coach":     5_000_000,
        "nutrition": 2_000_000,
        "recovery":  1_500_000,
        "medical":   1_000_000,
    }

    domains = ["coach", "nutrition", "recovery", "medical"] if args.domain == "all" else [args.domain]

    for domain in domains:
        count = max(1000, int(TARGET_COUNTS[domain] * args.scale))
        print(f"\n[{domain.upper()}] Target: {count:,} samples")
        samples = generate_samples(domain, count)
        out_path = os.path.join(args.output_dir, f"{domain}_dataset.jsonl")
        write_jsonl(samples, out_path)

    print("\n✓ Synthetic dataset generation complete.")


if __name__ == "__main__":
    main()
