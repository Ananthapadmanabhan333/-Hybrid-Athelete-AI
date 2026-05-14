from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.finetuning import ConversationRating, DatasetExportRequest, DatasetStatistics
from app.ai_engine.finetuning_service import FineTuningService

router = APIRouter()
finetuning_service = FineTuningService()

@router.post("/rate-conversation")
def rate_conversation(
    rating: ConversationRating,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Rate an AI Coach conversation for quality assessment.
    High-rated conversations will be used for fine-tuning.
    """
    finetuning_service.rate_conversation(
        db=db,
        conversation_id=rating.conversation_id,
        rating=rating.rating,
        was_helpful=rating.was_helpful,
        feedback_text=rating.feedback_text
    )
    return {"status": "success", "message": "Conversation rated successfully"}

@router.post("/export-dataset")
def export_training_dataset(
    request: DatasetExportRequest,
    db: Session = Depends(deps.get_db)
) -> dict:
    """
    Export high-quality conversations as training dataset.
    Supports JSONL format for Gemini fine-tuning.
    """
    try:
        filename = finetuning_service.export_training_dataset(
            db=db,
            min_rating=request.min_rating,
            format=request.format,
            dataset_version=request.dataset_version
        )
        return {
            "status": "success",
            "filename": filename,
            "message": f"Training dataset exported successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/dataset-stats", response_model=DatasetStatistics)
def get_dataset_statistics(
    db: Session = Depends(deps.get_db)
) -> Any:
    """
    Get statistics about collected training data.
    Useful for monitoring data collection progress.
    """
    stats = finetuning_service.get_dataset_statistics(db)
    return stats
