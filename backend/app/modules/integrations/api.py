
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Any
from sqlalchemy.orm import Session
from app.api import deps
from . import models, schemas
from datetime import datetime

router = APIRouter()

@router.get("/status", response_model=List[schemas.WearableSyncStatus])
def get_sync_status(
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Get sync status for all connected providers.
    """
    statuses = db.query(models.WearableSyncStatus).filter(
        models.WearableSyncStatus.user_id == current_user.id
    ).all()
    return statuses

@router.post("/trigger-sync/{provider}")
def trigger_sync(
    provider: str,
    db: Session = Depends(deps.get_db),
    current_user = Depends(deps.get_current_active_user)
) -> Any:
    """
    Trigger a manual sync for a provider.
    """
    # Logic to trigger sync job
    return {"message": f"Sync triggered for {provider}"}
