"""
Demo script for Fine-Tuning System
Shows data collection and export workflow without requiring database
"""
import json
from datetime import datetime

# Simulate collected conversations from AI Coach
conversations = [
    {
        "id": 1,
        "user_message": "I'm feeling really tired today, should I still train?",
        "ai_response": "Based on your elevated CNS fatigue at 65%, I recommend an active recovery session today. Focus on light movement, mobility work, and stretching. This will aid recovery without adding stress.",
        "user_context": {
            "cns_fatigue": 65,
            "muscular_upper_fatigue": 45,
            "muscular_lower_fatigue": 55,
            "sleep_hours": 6.5,
            "mood": "tired"
        },
        "rating": 5,
        "was_helpful": True
    },
    {
        "id": 2,
        "user_message": "What should I eat before boxing training?",
        "ai_response": "For boxing, aim for easily digestible carbs 1-2 hours before. Try a banana with peanut butter, or oatmeal with honey. Stay hydrated and avoid heavy meals that might cause discomfort during intense movement.",
        "user_context": {
            "next_workout": "boxing",
            "time_until_workout": "2 hours",
            "last_meal": "4 hours ago"
        },
        "rating": 5,
        "was_helpful": True
    },
    {
        "id": 3,
        "user_message": "My shoulder hurts when I do overhead press",
        "ai_response": "Sharp pain is a red flag. Stop overhead pressing immediately. I'm adding this to your injury log and will exclude overhead movements from your workouts. Consider seeing a physiotherapist. In the meantime, focus on horizontal pressing and pulling exercises.",
        "user_context": {
            "pain_location": "shoulder",
            "pain_type": "sharp",
            "pain_level": 7
        },
        "rating": 5,
        "was_helpful": True
    },
    {
        "id": 4,
        "user_message": "How can I improve my cardio for boxing?",
        "ai_response": "For boxing-specific cardio, focus on interval training that mimics round structure: 3-minute high-intensity intervals with 1-minute rest. Include jump rope, shadowboxing, and heavy bag work. Aim for 3-4 sessions per week, separate from technical boxing training.",
        "user_context": {
            "current_cardio_level": "intermediate",
            "goal": "improve boxing endurance",
            "training_frequency": "4x/week"
        },
        "rating": 4,
        "was_helpful": True
    },
    {
        "id": 5,
        "user_message": "I only have 30 minutes to train today",
        "ai_response": "Perfect for a high-intensity circuit. I'll design a 30-minute session with compound movements: 5 rounds of (Push-ups, Squats, Rows, Plank - 40s work, 20s rest). This hits all major muscle groups efficiently. Warm up for 5 minutes, cool down for 3 minutes.",
        "user_context": {
            "time_available": 30,
            "equipment": ["bodyweight", "resistance bands"],
            "energy_level": "moderate"
        },
        "rating": 5,
        "was_helpful": True
    }
]

def export_to_jsonl(conversations, filename="training_data_demo.jsonl"):
    """Export conversations to JSONL format for fine-tuning."""
    with open(filename, 'w', encoding='utf-8') as f:
        for conv in conversations:
            if conv['rating'] >= 4 and conv['was_helpful']:
                # Format context
                context_str = "\n".join([f"- {k}: {v}" for k, v in conv['user_context'].items()])
                
                training_example = {
                    "text_input": f"""System: You are an expert AI fitness coach specializing in hybrid athlete training (boxing, strength, cardio, athletics). You provide personalized advice based on the athlete's current state, including fatigue levels, sleep quality, injuries, and goals. Always prioritize safety and recovery.

User Context:
{context_str}

User: {conv['user_message']}""",
                    "output": conv['ai_response']
                }
                f.write(json.dumps(training_example, ensure_ascii=False) + '\n')
    
    print(f"✅ Exported {len([c for c in conversations if c['rating'] >= 4])} conversations to {filename}")
    return filename

def show_statistics(conversations):
    """Display dataset statistics."""
    total = len(conversations)
    rated = len([c for c in conversations if 'rating' in c])
    high_quality = len([c for c in conversations if c.get('rating', 0) >= 4 and c.get('was_helpful', False)])
    
    print("\n📊 Dataset Statistics")
    print("=" * 50)
    print(f"Total conversations:          {total}")
    print(f"Rated conversations:          {rated} ({rated/total*100:.1f}%)")
    print(f"High-quality (4+ stars):      {high_quality} ({high_quality/total*100:.1f}%)")
    print(f"Available for training:       {high_quality}")
    print("=" * 50)

def show_sample_conversation(conversation):
    """Display a sample conversation."""
    print("\n💬 Sample Conversation")
    print("=" * 50)
    print(f"User: {conversation['user_message']}")
    print(f"\nAI: {conversation['ai_response']}")
    print(f"\nRating: {'⭐' * conversation['rating']}")
    print(f"Helpful: {'✅' if conversation['was_helpful'] else '❌'}")
    print(f"\nContext:")
    for key, value in conversation['user_context'].items():
        print(f"  - {key}: {value}")
    print("=" * 50)

def show_training_example(filename):
    """Display formatted training example."""
    print("\n📝 Training Data Format (JSONL)")
    print("=" * 50)
    with open(filename, 'r', encoding='utf-8') as f:
        first_example = json.loads(f.readline())
        print(json.dumps(first_example, indent=2, ensure_ascii=False))
    print("=" * 50)

def main():
    print("\n" + "=" * 50)
    print("🤖 FUELIX AI COACH - FINE-TUNING DEMO")
    print("=" * 50)
    
    # Show statistics
    show_statistics(conversations)
    
    # Show sample conversation
    show_sample_conversation(conversations[0])
    
    # Export training data
    print("\n🔄 Exporting Training Dataset...")
    filename = export_to_jsonl(conversations)
    
    # Show training example format
    show_training_example(filename)
    
    # Next steps
    print("\n🚀 Next Steps for Fine-Tuning")
    print("=" * 50)
    print("1. Upload training_data_demo.jsonl to Gemini API")
    print("2. Configure fine-tuning job with:")
    print("   - Base model: gemini-pro")
    print("   - Training steps: 100-500")
    print("   - Learning rate: 0.001")
    print("3. Monitor training progress")
    print("4. Deploy fine-tuned model")
    print("5. A/B test against base model")
    print("=" * 50)
    
    print("\n✅ Demo Complete!")
    print(f"📁 Training data saved to: {filename}")
    print("\n💡 This demonstrates the complete data collection")
    print("   and export pipeline for NLP model fine-tuning.")

if __name__ == "__main__":
    main()
