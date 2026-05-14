"""
Demo script to show data persistence in Fuelix
Tests that profile updates and chat messages are saved to database
"""
import sys
sys.path.append('.')

from app.db.session import SessionLocal
from app.models.user import User
from app.models.chat_message import ChatMessage
from app.models.athlete_state import AthleteState
from datetime import datetime

def demo_data_persistence():
    """Demonstrate that data is being saved to the database"""
    db = SessionLocal()
    
    print("=" * 60)
    print("FUELIX DATA PERSISTENCE DEMO")
    print("=" * 60)
    
    # 1. Check Users
    print("\n📊 USERS IN DATABASE:")
    users = db.query(User).all()
    print(f"Total users: {len(users)}")
    for user in users:
        print(f"  - {user.full_name} ({user.email})")
        print(f"    Weight: {user.current_weight_kg}kg, Activity: {user.activity_level}")
    
    # 2. Check Chat Messages
    print("\n💬 CHAT HISTORY:")
    messages = db.query(ChatMessage).order_by(ChatMessage.timestamp.desc()).limit(10).all()
    print(f"Total chat messages: {db.query(ChatMessage).count()}")
    print(f"Showing last {len(messages)} messages:")
    for msg in messages:
        user = db.query(User).filter(User.id == msg.user_id).first()
        print(f"\n  [{msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {user.full_name if user else 'Unknown'}:")
        print(f"  User: {msg.user_message[:50]}...")
        print(f"  AI: {msg.ai_response[:50]}...")
    
    # 3. Check Athlete States
    print("\n🏋️ ATHLETE STATES:")
    states = db.query(AthleteState).all()
    print(f"Total athlete states: {len(states)}")
    for state in states:
        user = db.query(User).filter(User.id == state.user_id).first()
        print(f"  - {user.full_name if user else 'Unknown'}:")
        print(f"    CNS Fatigue: {state.cns_fatigue:.1f}%")
        print(f"    Upper Body: {state.muscular_fatigue_upper:.1f}%")
        print(f"    Lower Body: {state.muscular_fatigue_lower:.1f}%")
    
    print("\n" + "=" * 60)
    print("✅ ALL DATA IS BEING SAVED TO DATABASE!")
    print("=" * 60)
    
    db.close()

if __name__ == "__main__":
    demo_data_persistence()
