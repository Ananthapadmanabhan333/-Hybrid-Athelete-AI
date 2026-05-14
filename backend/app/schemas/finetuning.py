from pydantic import BaseModel
from typing import Optional

class ConversationRating(BaseModel):
    conversation_id: int
    rating: int  # 1-5
    was_helpful: bool
    feedback_text: Optional[str] = None

class DatasetExportRequest(BaseModel):
    min_rating: int = 4
    format: str = "jsonl"  # jsonl, json, csv
    dataset_version: Optional[str] = None

class DatasetStatistics(BaseModel):
    total_conversations: int
    rated_conversations: int
    high_quality_conversations: int
    included_in_training: int
    available_for_training: int
