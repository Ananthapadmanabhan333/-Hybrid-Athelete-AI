from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.coach import CoachResponse
from app.ai_engine.coach_orchestrator import CoachOrchestrator
from app.ai_engine.llm_service import LLMService
from app.models.user import User
from app.models.chat_message import ChatMessage
from datetime import datetime

router = APIRouter()
orchestrator = CoachOrchestrator()
llm = LLMService()

@router.post("/chat", response_model=CoachResponse)
def chat_with_coach(
    message: str,
    user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """
    Chat with the AI Coach. Saves conversation history to database.
    Uses CoachOrchestrator for context-aware responses.
    """
    # Generate AI response using orchestrator for better context
    response_text = orchestrator.process_message(user, message, db)
    
    # Save to database if available
    if db is not None:
        try:
            chat_record = ChatMessage(
                user_id=user.id,
                user_message=message,
                ai_response=response_text,
                timestamp=datetime.utcnow()
            )
            db.add(chat_record)
            db.commit()
        except Exception as e:
            print(f"Failed to save chat message: {e}")
            # Continue even if save fails
    
    return CoachResponse(
        recommendation=response_text,
        warning=None,
        adjusted_plan=None
    )

@router.get("/history")
def get_chat_history(
    limit: int = 20,
    user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db)
):
    """
    Get user's chat history with the AI Coach.
    """
    if db is None:
        return {"messages": [], "message": "Database unavailable"}
    
    try:
        messages = db.query(ChatMessage).filter(
            ChatMessage.user_id == user.id
        ).order_by(ChatMessage.timestamp.desc()).limit(limit).all()
        
        return {
            "messages": [
                {
                    "id": msg.id,
                    "user_message": msg.user_message,
                    "ai_response": msg.ai_response,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in messages
            ]
        }
    except Exception as e:
        print(f"Failed to retrieve chat history: {e}")
        return {"messages": [], "error": str(e)}
