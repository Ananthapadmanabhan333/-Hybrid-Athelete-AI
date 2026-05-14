"""
Show all strength exercises available in Fuelix
"""
from app.ai_engine.knowledge.strength import StrengthKnowledge

sk = StrengthKnowledge()

print("=" * 70)
print("FUELIX STRENGTH EXERCISES DATABASE")
print("=" * 70)
print(f"\nTotal Exercises: {len(sk.EXERCISE_DB)}\n")

# Group by muscle
categories = {}
for ex in sk.EXERCISE_DB:
    muscle = ex['muscle']
    if muscle not in categories:
        categories[muscle] = []
    categories[muscle].append(ex['name'])

# Display by category
for muscle in sorted(categories.keys()):
    exercises = categories[muscle]
    print(f"\n{muscle.upper()} ({len(exercises)} exercises):")
    for ex in exercises:
        print(f"  • {ex}")

print("\n" + "=" * 70)
print(f"✅ {len(sk.EXERCISE_DB)} professional exercises ready!")
print("=" * 70)
