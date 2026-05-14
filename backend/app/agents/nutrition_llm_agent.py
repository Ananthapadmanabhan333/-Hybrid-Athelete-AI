from typing import Dict, Any, List
import json
from app.ai_engine.llm_service import LLMService

class NutritionLLMAgent:
    def __init__(self):
        self.llm = LLMService()

    def generate_insights(self, context: Dict[str, Any]) -> Dict[str, Any]:
        system_prompt = """
        You are an expert AI Nutrition Agent for an elite hybrid athlete platform.
        Your goal is to provide a brief summary insight, actionable steps, and any warnings based on the provided data.
        You MUST NOT invent calorie values, weight data, or metrics.
        You MUST NOT prescribe medication or perform mathematical calculations.

        Respond strictly in valid JSON format ONLY:
        {
          "summary_insight": "A brief overview of their current trajectory.",
          "actionable_steps": ["Step 1", "Step 2"],
          "warning": "Any red flags (or null if none)."
        }
        """

        context_str = "\n".join([f"- {k}: {v}" for k, v in context.items()])
        user_message = f"Based on the following deterministic data, provide the required structured JSON response:\n\n{context_str}"

        try:
            # Route to nutrition adapter if Mistral is available, fallback transparently
            response_text = self.llm.generate_response(
                system_prompt=system_prompt,
                user_message=user_message,
                agent="nutrition",
                context=context,
            )
            # Try to parse the JSON
            # Sometimes LLMs wrap JSON in markdown blocks like ```json ... ```
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            return json.loads(clean_text)
        except Exception as e:
            print(f"Failed to parse Nutrition AI response: {e}")
            return {
                "summary_insight": "Your nutrition data is being analyzed, keep logging your meals to build a stable trend.",
                "actionable_steps": ["Ensure your protein tracking is accurate", "Stay hydrated"],
                "warning": None
            }

    def chat_response(self, context: Dict[str, Any], chat_history: List[Dict[str, str]], user_message: str) -> str:
        system_prompt = """
        You are an expert AI Nutrition Coach answering a question from a hybrid athlete.
        Use their current nutrition context below to personalize your advice.
        Be concise, accurate, and supportive. DO NOT invent fake logged data.
        
        Current Context:
        """
        system_prompt += "\n".join([f"- {k}: {v}" for k, v in context.items()])

        # Instead of feeding raw history directly to the generic LLM service (which only takes sys and user msg),
        # we'll append the last few messages to the prompt to give it context.
        recent_history = ""
        if chat_history:
            recent_history = "\n\nRecent Conversation History:\n"
            for msg in chat_history[-4:]: # last 4 messages
                recent_history += f"{'Athlete' if msg['is_user'] else 'Coach'}: {msg['text']}\n"
        
        final_user_msg = f"{recent_history}\nAthlete: {user_message}"
        
        return self.llm.generate_response(
            system_prompt=system_prompt,
            user_message=final_user_msg,
            agent="nutrition",
            context=context,
        )
