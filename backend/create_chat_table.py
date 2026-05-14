"""
Update database tables to include chat_messages
"""
from app.db.base import Base
from app.db.session import engine
from app.models.chat_message import ChatMessage

def create_chat_table():
    """Create chat_messages table."""
    print("Creating chat_messages table...")
    Base.metadata.create_all(bind=engine, tables=[ChatMessage.__table__])
    print("✅ chat_messages table created successfully!")

if __name__ == "__main__":
    create_chat_table()
