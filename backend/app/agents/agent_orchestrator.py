import time
import asyncio
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.api import deps
from app.models.user import User

from app.agents.medical_agent import analyze_lab_values, generate_medical_explanation
from app.agents.nutrition_agent import analyze_nutrition_context, nutrition_agent
from app.recovery_engine_v4.models import RecoveryScore
from app.agents.recovery_agent import generate_recovery_explanation
from app.ai_engine.llm_service import LLMService
from datetime import date, timedelta

router = APIRouter()

# Shared LLM service instance (uses the Mistral singleton when model is available)
_llm = LLMService()


class OrchestratorRequest(BaseModel):
    intent: str # "medical", "nutrition", "recovery"
    raw_input: dict

@router.post("/orchestrate")
async def route_request_to_agent(
    payload: OrchestratorRequest,
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    start_time = time.time()
    response = {}
    
    try:
        if payload.intent == "medical":
            # Deterministic lab analysis (never changes)
            analysis = analyze_lab_values(payload.raw_input)
            if analysis["status"] == "insufficient_data":
                response = {"status": "error", "message": "insufficient_data"}
            else:
                # Route explanation through Mistral medical adapter if available
                context = {k: v for k, v in payload.raw_input.items() if v is not None}
                flags_str = ", ".join(analysis.get("flags", [])) or "no flags"
                user_message = (
                    f"The athlete's lab analysis shows: severity={analysis.get('severity')}, "
                    f"flags=[{flags_str}]. Provide a clear, evidence-based explanation."
                )
                explanation = _llm.generate_response(
                    system_prompt=(
                        "You are Fuelix AI Medical Advisor. "
                        "Explain lab results clearly. Never prescribe medication or diagnose conditions. "
                        "Always include a medical disclaimer."
                    ),
                    user_message=user_message,
                    agent="medical",
                    context=context,
                )
                # Fallback to deterministic if LLM returns insufficient_data
                if explanation == "insufficient_data" or not explanation:
                    response = generate_medical_explanation(analysis)
                else:
                    response = {"message": explanation, "disclaimer": True, "analysis": analysis}
                    
        elif payload.intent == "nutrition":
            # Reuse the same deterministic context as the dedicated nutrition agent
            context = analyze_nutrition_context(current_user, db)

            if "error" in context:
                response = {"status": "error", "message": "insufficient_data"}
            else:
                user_query = payload.raw_input.get("query", "How am I doing?")
                # Wrap NutritionLLMAgent.chat_response to keep output structured
                answer = nutrition_agent.chat_response(
                    context=context,
                    chat_history=payload.raw_input.get("history", []),
                    user_message=user_query,
                )
                response = {
                    "issues": [],
                    "recommendations": [],
                    "message": answer,
                    "context": context,
                }
                
        elif payload.intent == "recovery":
            target_date = date.today()
            score_record = db.query(RecoveryScore).filter(
                RecoveryScore.user_id == current_user.id,
                RecoveryScore.date == target_date
            ).first()
            
            if not score_record:
                response = {"status": "error", "message": "insufficient_data"}
            else:
                # Route recovery explanation through Mistral recovery adapter if available
                recovery_context = {
                    "recovery_score": score_record.recovery_score,
                    "fatigue_flag": score_record.fatigue_flag,
                    "date": str(target_date),
                }
                user_message = (
                    f"The athlete's recovery score is {score_record.recovery_score}/100 "
                    f"with fatigue flag: {score_record.fatigue_flag}. "
                    "Provide specific recovery advice."
                )
                explanation = _llm.generate_response(
                    system_prompt=(
                        "You are Fuelix AI Recovery Coach. "
                        "Provide clear recovery advice based on the athlete's data. "
                        "Never invent metrics."
                    ),
                    user_message=user_message,
                    agent="recovery",
                    context=recovery_context,
                )
                # Fallback to deterministic if Mistral unavailable
                if explanation == "insufficient_data" or not explanation:
                    response = generate_recovery_explanation(score_record.recovery_score, score_record.fatigue_flag)
                else:
                    response = {
                        "insight": explanation,
                        "recommended_action": score_record.fatigue_flag,
                        "recovery_score": score_record.recovery_score,
                    }
                
        else:
            raise HTTPException(status_code=400, detail="Invalid intent")
            
        latency = time.time() - start_time
        # log_ai_latency(current_user.id, payload.intent, latency) # Simulated Background task
        
        return {"data": response, "meta": {"latency_sec": round(latency, 2)}}
        
    except Exception as e:
        # Catch LLM timeouts or unexpected JSON parse errors safely
        print(f"Orchestrator Error: {e}")
        return {"status": "error", "message": "The AI service is currently unavailable. Please check your data manually."}


@router.get("/ai/status")
async def get_ai_status(current_user: User = Depends(deps.get_current_user)):
    """
    Returns the current AI backend status.
    Indicates which model tier is active (Mistral/Gemini/G4F/fallback).
    """
    try:
        from app.ai.mistral_multi_adapter_service import mistral_service
        status = mistral_service.get_status()
        active_backend = "mistral" if status["model_ready"] else "gemini_or_fallback"
        return {
            "active_backend": active_backend,
            "mistral_status": status,
        }
    except Exception:
        return {
            "active_backend": "gemini_or_fallback",
            "mistral_status": {"model_ready": False},
        }
