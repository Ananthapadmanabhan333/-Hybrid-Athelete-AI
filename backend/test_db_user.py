import sys
sys.path.insert(0, '.')

from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

db = SessionLocal()

try:
    print("Creating user...")
    hashed_pw = get_password_hash('password123')
    print(f"Password hashed successfully: {hashed_pw[:50]}...")
    
    user = User(
        email='testuser999@example.com',
        hashed_password=hashed_pw,
        full_name='Test User',
        is_active=True
    )
    
    print("Adding to database...")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    print(f"✓ SUCCESS! User created with ID: {user.id}")
    
except Exception as e:
    print(f"✗ ERROR: {e}")
    import traceback
    traceback.print_exc()
finally:
    db.close()
