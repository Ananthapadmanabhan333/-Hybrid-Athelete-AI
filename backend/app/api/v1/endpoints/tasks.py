from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.models.user import User
from app.ai_engine.notification_agent import NotificationAgent
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()
agent = NotificationAgent()

class TaskOut(BaseModel):
    id: int
    title: str
    message: str
    category: str
    priority: str
    is_completed: bool
    due_date: datetime

    class Config:
        orm_mode = True

@router.get("/today", response_model=List[TaskOut])
def get_daily_tasks(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get today's prioritized tasks. Generates them if missing.
    """
    return agent.get_or_create_daily_tasks(current_user, db)

@router.post("/{task_id}/complete")
def complete_task(
    task_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Mark a task as completed.
    """
    success = agent.complete_task(task_id, db)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success"}
