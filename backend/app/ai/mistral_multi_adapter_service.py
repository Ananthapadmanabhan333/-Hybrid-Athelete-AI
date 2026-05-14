"""
mistral_multi_adapter_service.py
---------------------------------
Fuelix AI — Mistral-7B Multi-Adapter Inference Service

Responsibilities:
  1. Load base model ONCE at startup (4-bit quantised)
  2. Load LoRA adapters dynamically per domain
  3. Cache loaded adapters in memory (avoid reload per request)
  4. Generate coaching responses with strict guardrails
  5. Fallback gracefully to LLMService if model unavailable

Architecture:
  Base model: mistralai/Mistral-7B-Instruct-v0.2  (loaded once)
  Adapters  : coach | nutrition | recovery | medical  (cached after first load)

Guardrails (hard-coded, never bypassed):
  - Never invent athlete metrics
  - Never perform calculations
  - Never prescribe medical treatment
  - Return "insufficient_data" when context is missing
"""

import os
import logging
import json
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# ─── Adapter directory (relative to backend root) ────────────────────────────
_BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_MODELS_DIR  = os.path.join(_BACKEND_DIR, "models")

ADAPTER_DIRS: Dict[str, str] = {
    "coach":     os.path.join(_MODELS_DIR, "coach_adapter"),
    "nutrition": os.path.join(_MODELS_DIR, "nutrition_adapter"),
    "recovery":  os.path.join(_MODELS_DIR, "recovery_adapter"),
    "medical":   os.path.join(_MODELS_DIR, "medical_adapter"),
}

BASE_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.2"

SYSTEM_PROMPT = (
    "You are Fuelix AI, an expert hybrid athlete coach specializing in strength training, "
    "boxing performance, endurance development, nutrition analysis, and recovery optimization. "
    "You provide accurate, evidence-based coaching insights based on the athlete's real data. "
    "You MUST NOT invent athlete metrics, perform calculations, or prescribe medical treatments. "
    "If the athlete context is missing or insufficient, respond only with: insufficient_data"
)

VALID_AGENTS = frozenset(["coach", "nutrition", "recovery", "medical"])


class MistralMultiAdapterService:
    """
    Singleton-pattern inference service for Fuelix Mistral-7B adapters.

    Usage (within FastAPI lifespan or endpoint):
        service = MistralMultiAdapterService()
        response = service.generate("coach", context_dict, "Why am I fatigued?")
    """

    _instance: Optional["MistralMultiAdapterService"] = None
    _base_model = None
    _tokenizer = None
    _adapter_cache: Dict[str, Any] = {}
    _model_ready: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def initialize(self) -> bool:
        """
        Load base model and tokenizer once.
        Called at application startup.
        Returns True if successful, False if libraries unavailable.
        """
        if self._model_ready:
            logger.info("MistralMultiAdapterService already initialised.")
            return True

        try:
            import torch
            from transformers import (
                AutoTokenizer,
                AutoModelForCausalLM,
                BitsAndBytesConfig,
            )

            logger.info(f"Loading base model: {BASE_MODEL_NAME}")
            logger.info(f"GPU available: {torch.cuda.is_available()}")

            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
            )

            self._tokenizer = AutoTokenizer.from_pretrained(
                BASE_MODEL_NAME,
                trust_remote_code=True,
            )
            self._tokenizer.pad_token = self._tokenizer.eos_token
            self._tokenizer.padding_side = "right"

            self._base_model = AutoModelForCausalLM.from_pretrained(
                BASE_MODEL_NAME,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True,
            )
            self._base_model.config.use_cache = False

            self._model_ready = True
            logger.info("✓ Base model loaded successfully.")
            return True

        except ImportError as e:
            logger.warning(
                f"Mistral inference libraries not installed: {e}. "
                "Falling back to LLMService. "
                "Install with: pip install transformers peft bitsandbytes torch"
            )
            return False

        except Exception as e:
            logger.error(f"Failed to load base model: {e}", exc_info=True)
            return False

    def _load_adapter(self, agent: str):
        """
        Load adapter for a domain and cache it.
        Returns PeftModel or None if adapter not found.
        """
        if agent in self._adapter_cache:
            logger.debug(f"Cache hit for adapter: {agent}")
            return self._adapter_cache[agent]

        adapter_dir = ADAPTER_DIRS.get(agent)
        if not adapter_dir or not os.path.isdir(adapter_dir):
            logger.warning(
                f"Adapter directory not found for '{agent}': {adapter_dir}. "
                "Train the adapter first. Falling back to base model."
            )
            self._adapter_cache[agent] = None
            return None

        try:
            from peft import PeftModel
            logger.info(f"Loading adapter: {agent} from {adapter_dir}")
            model_with_adapter = PeftModel.from_pretrained(
                self._base_model,
                adapter_dir,
                is_trainable=False,
            )
            model_with_adapter.eval()
            self._adapter_cache[agent] = model_with_adapter
            logger.info(f"✓ Adapter cached: {agent}")
            return model_with_adapter

        except Exception as e:
            logger.error(f"Failed to load adapter '{agent}': {e}", exc_info=True)
            self._adapter_cache[agent] = None
            return None

    def _build_prompt(self, context: Dict[str, Any], user_message: str) -> str:
        """
        Build Mistral instruction prompt with structured athlete context.

        Format:
          <s>[INST] <<SYS>>
          {system_prompt}
          <</SYS>>

          Athlete Context:
          {context_lines}

          {user_message} [/INST]
        """
        ctx_lines = []
        for k, v in context.items():
            if v is not None and v != "" and k not in ("_source",):
                ctx_lines.append(f"  {k}: {v}")

        if ctx_lines:
            ctx_block = "Athlete Context:\n" + "\n".join(ctx_lines)
            full_message = f"{ctx_block}\n\n{user_message}"
        else:
            # Empty context → guardrail should trigger insufficient_data
            full_message = user_message

        return (
            f"<s>[INST] <<SYS>>\n{SYSTEM_PROMPT}\n<</SYS>>\n\n"
            f"{full_message} [/INST]"
        )

    def generate(
        self,
        agent: str,
        context: Dict[str, Any],
        user_message: str,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
        top_p: float = 0.9,
    ) -> str:
        """
        Generate a coaching response using the appropriate LoRA adapter.

        Parameters
        ----------
        agent        : one of coach | nutrition | recovery | medical
        context      : structured athlete data (from ContextManager)
        user_message : the athlete's question or the agent's trigger message
        """
        # ── Validation ────────────────────────────────────────────
        if agent not in VALID_AGENTS:
            logger.error(f"Unknown agent: {agent}")
            return "insufficient_data"

        if not self._model_ready:
            logger.warning("Model not ready. Returning insufficient_data.")
            return "insufficient_data"

        # ── Guard: empty context ───────────────────────────────────
        if not context:
            logger.warning(f"[{agent}] Empty context — returning insufficient_data.")
            return "insufficient_data"

        try:
            import torch

            # Route to correct adapter
            model = self._load_adapter(agent) or self._base_model

            # Build prompt
            prompt = self._build_prompt(context, user_message)

            # Tokenise
            device = next(model.parameters()).device
            encodings = self._tokenizer(
                prompt,
                return_tensors="pt",
                max_length=512,
                truncation=True,
            ).to(device)

            # Generate
            with torch.no_grad():
                output_ids = model.generate(
                    **encodings,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    do_sample=True,
                    repetition_penalty=1.1,
                    pad_token_id=self._tokenizer.eos_token_id,
                )

            # Decode only the newly generated tokens
            new_tokens = output_ids[0][encodings["input_ids"].shape[1]:]
            response = self._tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

            # Post-generation guardrail: never return empty
            if not response:
                return "insufficient_data"

            return response

        except Exception as e:
            logger.error(f"Generation error [{agent}]: {e}", exc_info=True)
            return "insufficient_data"

    @property
    def is_ready(self) -> bool:
        return self._model_ready

    def get_status(self) -> Dict[str, Any]:
        """Return health/status information for monitoring."""
        return {
            "model_ready": self._model_ready,
            "base_model": BASE_MODEL_NAME,
            "adapters_cached": list(self._adapter_cache.keys()),
            "adapters_available": {
                agent: os.path.isdir(path)
                for agent, path in ADAPTER_DIRS.items()
            },
        }


# ─── Module-level singleton ───────────────────────────────────────────────────
mistral_service = MistralMultiAdapterService()
