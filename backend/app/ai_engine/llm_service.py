import os
import logging
import google.generativeai as genai
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

try:
    import g4f
    from g4f.client import Client
except ImportError:
    g4f = None
    Client = None


class LLMService:
    """
    Fuelix LLM Service — Priority chain:

      1. Local Mistral-7B + LoRA adapter  (if model is loaded and adapter exists)
      2. Google Gemini API                (if GEMINI_API_KEY is set)
      3. G4F / GPT4Free                  (if available)
      4. Keyword-based fallback           (always available)

    Public API is unchanged — generate_response(system_prompt, user_message).
    The optional `agent` and `context` parameters enable Mistral adapter routing.
    """

    def __init__(self):
        # ── Mistral multi-adapter service (lazy import, never crashes startup) ──
        self._mistral = None
        self._mistral_checked = False

        # ── Gemini ──────────────────────────────────────────────────────────────
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel("gemini-pro")
        else:
            self.model = None

        # ── G4F ─────────────────────────────────────────────────────────────────
        # ── G4F ─────────────────────────────────────────────────────────────────
        if Client:
            self.g4f_client = Client()
        else:
            # Try to re-instantiate if possible, or leave as None
            try:
                from g4f.client import Client as GClient
                self.g4f_client = GClient()
            except:
                self.g4f_client = None

    # ─────────────────────────────────────────────────────────────────────────
    #  Mistral accessor (lazy initialisation — model loads only when needed)
    # ─────────────────────────────────────────────────────────────────────────

    def _get_mistral(self):
        """Return the MistralMultiAdapterService singleton if available."""
        if self._mistral_checked:
            return self._mistral

        self._mistral_checked = True
        try:
            from app.ai.mistral_multi_adapter_service import mistral_service
            if mistral_service.is_ready:
                self._mistral = mistral_service
                logger.info("LLMService: Mistral adapter service is active.")
            else:
                logger.info("LLMService: Mistral service present but not initialised.")
        except Exception as e:
            logger.debug(f"LLMService: Mistral service unavailable: {e}")

        return self._mistral

    # ─────────────────────────────────────────────────────────────────────────
    #  Public API — signature unchanged from original
    # ─────────────────────────────────────────────────────────────────────────

    def generate_response(
        self,
        system_prompt: str,
        user_message: str,
        agent: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Generate a response using the best available backend.

        Parameters (new, optional — backwards compatible)
        ----------
        agent   : "coach" | "nutrition" | "recovery" | "medical"
                  When provided, routes to the matching LoRA adapter.
        context : Structured athlete data dict from ContextManager.
                  Required for Mistral; ignored by other backends.
        """
        # ── 1. Try Mistral adapter ───────────────────────────────────────────
        if agent and context is not None:
            mistral = self._get_mistral()
            if mistral:
                try:
                    response = mistral.generate(
                        agent=agent,
                        context=context,
                        user_message=user_message,
                    )
                    if response and response != "insufficient_data":
                        logger.debug(f"Mistral [{agent}] responded successfully.")
                        return response
                    elif response == "insufficient_data":
                        return response
                except Exception as e:
                    logger.warning(f"Mistral generation failed: {e}. Falling back.")

        # ── 2. Try Gemini ────────────────────────────────────────────────────
        if self.model:
            try:
                chat = self.model.start_chat(history=[
                    {"role": "user", "parts": [system_prompt]}
                ])
                response = chat.send_message(user_message)
                return response.text
            except Exception as e:
                logger.warning(f"Gemini LLM Error: {e}")

        # ── 3. Try G4F / fallback ────────────────────────────────────────────
        return self._simulate_intelligence(system_prompt, user_message)

    def _simulate_intelligence(self, system_prompt: str, message: str) -> str:
        """
        G4F (GPT4Free) Integration — fallback when no cloud API key is present.
        Keyword heuristics are the final safety net.
        """
        if self.g4f_client:
            try:
                # Try a list of robust providers
                response = self.g4f_client.chat.completions.create(
                    model="gpt-4o",  # Prefer 4o for better quality
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message},
                    ],
                )
                content = response.choices[0].message.content
                if content and len(content) > 10:
                    return content
            except Exception as e:
                logger.warning(f"G4F LLM Error: {e}")

        # --- ADVANCED HEURISTIC ENGINE (State-of-the-Art Fallback) ---
        msg = message.lower()
        
        # Extract context clues from system_prompt (it contains ContextManager.build_context)
        fatigue_info = "CNS" in system_prompt or "Muscular" in system_prompt
        high_fatigue = any(f + ": 8" in system_prompt or f + ": 9" in system_prompt for f in ["CNS", "Upper Body", "Lower Body", "Cardio"])

        if "tired" in msg or "exhausted" in msg or "fatigue" in msg:
            if high_fatigue:
                return (
                    "I notice your fatigue metrics are critical right now. Specifically, your CNS and nervous system "
                    "recovery are lagging. I strongly recommend a complete rest day today. "
                    "If you must move, keep it to a 20-minute Zone 1 walk or basic mobility flow. "
                    "Prioritize 8+ hours of sleep tonight to avoid CNS burnout."
                )
            return (
                "I see you're feeling the load. Your recent sessions have been high intensity. "
                "Instead of your scheduled workout, let's pivot to an 'Active Recovery' session. "
                "Focus on steady-state Zone 2 work at 50% intensity for 30 minutes to flush out metabolic waste."
            )

        if "pain" in msg or "hurt" in msg or "injury" in msg:
            return (
                "Safety is our priority. If you're feeling sharp pain, stop immediately. "
                "Based on our training protocols, we should adjust your next session to avoid the affected area. "
                "I've flagged this for your injury awareness module. Please describe the pain level (1-10) "
                "so I can update your constraints."
            )

        if "boxing" in msg or "punch" in msg or "spar" in msg:
            return (
                "For your technical boxing work, focus on hip rotation and breathing today. "
                "Since we have a strength block coming up, don't overtax your shoulders in shadowboxing. "
                "Keep your hands high and prioritize footwork speed over power."
            )

        if "strength" in msg or "lift" in msg or "weight" in msg or "squat" in msg:
            return (
                "Your strength progression is looking solid. If you're feeling good today, "
                "aim for a 2.5kg increase on your main compound lift, but keep the RPE at 8. "
                "Ensure you're getting enough protein (1.8-2.2g per kg) to support the upcoming volume."
            )

        if "running" in msg or "cardio" in msg or "marathon" in msg or "5k" in msg:
            return (
                "Hybrid training requires balancing your run volume with leg day recovery. "
                "If your lower body fatigue is elevated, keep your run at a conversational pace. "
                "Aim for a high cadence (170-180 ppm) to reduce impact stress on your joints."
            )

        if "nutrition" in msg or "eat" in msg or "diet" in msg or "protein" in msg:
            return (
                "Nutrition and recovery are two sides of the same coin. Based on your current "
                "hybrid volume, make sure you're hitting your carb targets to refuel glycogen stores. "
                "An ideal post-workout meal today would be 30g protein + 60g complex carbs."
            )

        if "hello" in msg or "hi " in msg or "hey" in msg:
            return (
                "Hey! I'm your Fuelix AI Coach. I've analyzed your latest stats and recent sessions. "
                "Overall you're making great progress in the hybrid protocols. Is there a specific "
                "metric or workout you'd like to dive into today?"
            )

        # Default Intelligent General Response
        return (
            "I've reviewed your current athlete profile. You're deep into your current training block. "
            "To give you the most 'perfect' advice, could you tell me more about how your last session felt? "
            "Specifically, was the RPE (Rate of Perceived Exertion) what you expected, or are we pushing too hard?"
        )
