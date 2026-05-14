"""
Fine-Tuning Service for AI Coach
Collects training data from user interactions and prepares datasets for model fine-tuning.
"""
import json
import os
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.training_conversation import TrainingConversation
from app.models.user import User


class FineTuningService:
    """
    Manages the collection and preparation of training data for fine-tuning.
    Supports both Gemini fine-tuning and custom model training.
    """
    
    def __init__(self):
        self.training_data_dir = "training_data"
        os.makedirs(self.training_data_dir, exist_ok=True)
    
    def log_conversation(
        self,
        db: Session,
        user_id: int,
        user_message: str,
        ai_response: str,
        system_prompt: str,
        user_context: Dict[str, Any],
        model_version: str = "gemini-pro",
        response_time_ms: float = None
    ) -> TrainingConversation:
        """
        Log a conversation for potential use in fine-tuning.
        """
        conversation = TrainingConversation(
            user_id=user_id,
            user_message=user_message,
            ai_response=ai_response,
            system_prompt=system_prompt,
            user_context=user_context,
            model_version=model_version,
            response_time_ms=response_time_ms
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    def rate_conversation(
        self,
        db: Session,
        conversation_id: int,
        rating: int,
        was_helpful: bool,
        feedback_text: str = None
    ):
        """
        Allow users to rate AI responses for quality filtering.
        """
        conversation = db.query(TrainingConversation).filter(
            TrainingConversation.id == conversation_id
        ).first()
        
        if conversation:
            conversation.user_rating = rating
            conversation.was_helpful = was_helpful
            conversation.feedback_text = feedback_text
            conversation.rated_at = datetime.now()
            db.commit()
    
    def export_training_dataset(
        self,
        db: Session,
        min_rating: int = 4,
        format: str = "jsonl",
        dataset_version: str = None
    ) -> str:
        """
        Export high-quality conversations as training data.
        Formats: 'jsonl' (for Gemini), 'csv', 'json'
        """
        # Query high-quality conversations
        conversations = db.query(TrainingConversation).filter(
            TrainingConversation.user_rating >= min_rating,
            TrainingConversation.was_helpful == True,
            TrainingConversation.included_in_training == False
        ).all()
        
        if not dataset_version:
            dataset_version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = f"{self.training_data_dir}/training_data_{dataset_version}.{format}"
        
        if format == "jsonl":
            self._export_jsonl(conversations, filename, dataset_version, db)
        elif format == "json":
            self._export_json(conversations, filename, dataset_version, db)
        
        return filename
    
    def _export_jsonl(self, conversations: List[TrainingConversation], filename: str, version: str, db: Session):
        """
        Export in JSONL format for Gemini fine-tuning.
        Format: {"text_input": "...", "output": "..."}
        """
        with open(filename, 'w', encoding='utf-8') as f:
            for conv in conversations:
                # Construct input with context
                context_str = self._format_context(conv.user_context)
                text_input = f"{conv.system_prompt}\n\nUser Context:\n{context_str}\n\nUser: {conv.user_message}"
                
                training_example = {
                    "text_input": text_input,
                    "output": conv.ai_response
                }
                f.write(json.dumps(training_example) + '\n')
                
                # Mark as included
                conv.included_in_training = True
                conv.training_dataset_version = version
            
            db.commit()
    
    def export_mistral_dataset(
        self,
        db: Session,
        min_rating: int = 4,
        dataset_version: str = None
    ) -> str:
        """
        Export high-quality conversations for Fuelix Mistral-7B LoRA fine-tuning.
        Format: JSONL with {instruction, context, response} keys.
        """
        conversations = db.query(TrainingConversation).filter(
            TrainingConversation.user_rating >= min_rating,
            TrainingConversation.was_helpful == True,
            TrainingConversation.included_in_training == False
        ).all()
        
        if not dataset_version:
            dataset_version = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = f"{self.training_data_dir}/mistral_finetune_{dataset_version}.jsonl"
        
        with open(filename, 'w', encoding='utf-8') as f:
            for conv in conversations:
                example = {
                    "instruction": conv.user_message,
                    "context": conv.user_context,
                    "response": conv.ai_response
                }
                f.write(json.dumps(example) + '\n')
                
                conv.included_in_training = True
                conv.training_dataset_version = dataset_version
        
        db.commit()
        return filename

    def _export_json(self, conversations: List[TrainingConversation], filename: str, version: str, db: Session):
        """
        Export in JSON format for custom training pipelines.
        """
        dataset = []
        for conv in conversations:
            dataset.append({
                "id": conv.id,
                "user_message": conv.user_message,
                "ai_response": conv.ai_response,
                "system_prompt": conv.system_prompt,
                "context": conv.user_context,
                "rating": conv.user_rating,
                "timestamp": conv.created_at.isoformat()
            })
            
            conv.included_in_training = True
            conv.training_dataset_version = version
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dataset, f, indent=2, ensure_ascii=False)
        
        db.commit()
    def _format_context(self, context: Dict[str, Any]) -> str:
        """Format user context for training examples."""
        if not context:
            return "No context available"
        
        formatted = []
        for key, value in context.items():
            formatted.append(f"- {key}: {value}")
        return "\n".join(formatted)
    
    def get_dataset_statistics(self, db: Session) -> Dict[str, Any]:
        """
        Get statistics about collected training data.
        """
        total = db.query(TrainingConversation).count()
        rated = db.query(TrainingConversation).filter(
            TrainingConversation.user_rating.isnot(None)
        ).count()
        high_quality = db.query(TrainingConversation).filter(
            TrainingConversation.user_rating >= 4,
            TrainingConversation.was_helpful == True
        ).count()
        included = db.query(TrainingConversation).filter(
            TrainingConversation.included_in_training == True
        ).count()
        
        return {
            "total_conversations": total,
            "rated_conversations": rated,
            "high_quality_conversations": high_quality,
            "included_in_training": included,
            "available_for_training": high_quality - included
        }
