"""
_train_base.py
--------------
Shared QLoRA training logic used by all four domain training scripts.
Not executed directly — imported by train_*_adapter.py scripts.

Architecture:
  - Mistral-7B-Instruct-v0.2 loaded once in 4-bit quantisation
  - LoRA adapters trained per domain
  - SFTTrainer from trl handles formatting

Guardrails baked into training:
  - System prompt injected in every sample
  - Format: [INST] ... [/INST] response </s>
"""

import os
import json
import yaml
from typing import Optional, List

try:
    import torch
    from transformers import (
        AutoTokenizer,
        AutoModelForCausalLM,
        BitsAndBytesConfig,
        TrainingArguments,
    )
    from peft import LoraConfig, get_peft_model, TaskType
    from trl import SFTTrainer
    from datasets import Dataset
    TRAINING_AVAILABLE = True
except ImportError as e:
    TRAINING_AVAILABLE = False
    print(f"[WARNING] Training libraries not available: {e}")
    print("  Install with: pip install transformers peft trl bitsandbytes datasets torch")


CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")


def load_config() -> dict:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


SYSTEM_PROMPT = (
    "You are Fuelix AI, an expert hybrid athlete coach specializing in strength training, "
    "boxing performance, endurance development, nutrition analysis, and recovery optimization. "
    "You provide accurate, evidence-based coaching insights based on the athlete's real data. "
    "You never invent metrics or prescribe medical treatments. "
    "If context is insufficient, respond with 'insufficient_data'."
)


def format_sample(sample: dict) -> str:
    """
    Convert an instruction-format sample to Mistral chat format.

    [INST] <<SYS>>system<</SYS>>

    Context: {context}

    {instruction} [/INST] {response} </s>
    """
    instruction = sample.get("instruction", "")
    context = sample.get("context", {})
    response = sample.get("response", "")

    if not response or response.strip() == "":
        return None    # Will be filtered

    # Build context string
    if context and isinstance(context, dict):
        ctx_lines = [f"  {k}: {v}" for k, v in context.items()
                     if k not in ("_source",) and v != ""]
        ctx_str = "Athlete Context:\n" + "\n".join(ctx_lines) if ctx_lines else ""
    else:
        ctx_str = ""

    user_content = f"{ctx_str}\n\n{instruction}".strip() if ctx_str else instruction

    prompt = (
        f"<s>[INST] <<SYS>>\n{SYSTEM_PROMPT}\n<</SYS>>\n\n"
        f"{user_content} [/INST] {response} </s>"
    )
    return prompt


def load_dataset_from_jsonl(train_path: str, val_path: Optional[str] = None):
    """Load JSONL files into HuggingFace Dataset objects."""
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Training file not found: {train_path}")

    def read_jsonl(path):
        records = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return records

    train_records = read_jsonl(train_path)
    print(f"  Train samples loaded: {len(train_records):,}")

    # Format to text
    train_texts = [format_sample(r) for r in train_records]
    train_texts = [t for t in train_texts if t is not None]

    train_ds = Dataset.from_dict({"text": train_texts})

    val_ds = None
    if val_path and os.path.exists(val_path):
        val_records = read_jsonl(val_path)
        val_texts = [format_sample(r) for r in val_records]
        val_texts = [t for t in val_texts if t is not None]
        val_ds = Dataset.from_dict({"text": val_texts})
        print(f"  Val samples loaded  : {len(val_texts):,}")

    return train_ds, val_ds


def build_bnb_config(cfg: dict) -> "BitsAndBytesConfig":
    """Build 4-bit quantisation config from YAML."""
    import torch
    from transformers import BitsAndBytesConfig

    dtype_map = {"float16": torch.float16, "bfloat16": torch.bfloat16, "float32": torch.float32}
    compute_dtype = dtype_map.get(cfg["base_model"]["bnb_4bit_compute_dtype"], torch.float16)

    return BitsAndBytesConfig(
        load_in_4bit=cfg["base_model"]["load_in_4bit"],
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_quant_type=cfg["base_model"].get("bnb_4bit_quant_type", "nf4"),
        bnb_4bit_use_double_quant=cfg["base_model"].get("bnb_4bit_use_double_quant", True),
    )


def build_lora_config(cfg: dict) -> "LoraConfig":
    from peft import LoraConfig, TaskType

    lora_cfg = cfg["lora"]
    return LoraConfig(
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["lora_alpha"],
        target_modules=lora_cfg["target_modules"],
        lora_dropout=lora_cfg["lora_dropout"],
        bias=lora_cfg["bias"],
        task_type=TaskType.CAUSAL_LM,
    )


def train_adapter(domain: str, output_dir: Optional[str] = None):
    """
    Main training entry point called by each domain script.

    Parameters
    ----------
    domain      : one of coach | nutrition | recovery | medical
    output_dir  : optional override for adapter save path
    """
    if not TRAINING_AVAILABLE:
        print("[ERROR] Training libraries not installed. Cannot train.")
        print("  pip install transformers peft trl bitsandbytes datasets torch")
        return

    import torch

    cfg = load_config()

    adapter_cfg = cfg["adapters"][domain]
    model_name  = cfg["base_model"]["name"]
    train_cfg   = cfg["training"]

    # Resolve paths
    script_dir   = os.path.dirname(os.path.abspath(__file__))
    dataset_base = os.path.join(script_dir, "datasets", "final")
    train_path   = os.path.join(dataset_base, f"{domain}_train.jsonl")
    val_path     = os.path.join(dataset_base, f"{domain}_val.jsonl")

    out_dir = output_dir or adapter_cfg["output_dir"]
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"  FUELIX QLoRA TRAINER — {domain.upper()} ADAPTER")
    print(f"{'='*60}")
    print(f"  Base model : {model_name}")
    print(f"  Train data : {train_path}")
    print(f"  Output     : {out_dir}")
    print(f"  Device     : {'GPU' if torch.cuda.is_available() else 'CPU (slow)'}")
    print()

    # ── 1. Load tokenizer ─────────────────────────────────────────
    print("  [1/5] Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # ── 2. Load base model in 4-bit ───────────────────────────────
    print("  [2/5] Loading base model (4-bit quantised)...")
    bnb_config = build_bnb_config(cfg)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
    )
    model.config.use_cache = False
    model.config.pretraining_tp = 1

    # ── 3. Apply LoRA ─────────────────────────────────────────────
    print("  [3/5] Applying LoRA configuration...")
    lora_config = build_lora_config(cfg)
    model = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # ── 4. Load datasets ──────────────────────────────────────────
    print("  [4/5] Loading datasets...")
    train_ds, val_ds = load_dataset_from_jsonl(train_path, val_path)

    # ── 5. Train ──────────────────────────────────────────────────
    print("  [5/5] Starting training...")

    training_args = TrainingArguments(
        output_dir=os.path.join(out_dir, "checkpoints"),
        num_train_epochs=train_cfg["num_train_epochs"],
        per_device_train_batch_size=train_cfg["batch_size"],
        gradient_accumulation_steps=train_cfg["gradient_accumulation_steps"],
        learning_rate=train_cfg["learning_rate"],
        fp16=train_cfg["fp16"],
        logging_steps=train_cfg["logging_steps"],
        save_steps=train_cfg["save_steps"],
        save_total_limit=train_cfg["save_total_limit"],
        evaluation_strategy="steps" if val_ds else "no",
        eval_steps=train_cfg["eval_steps"] if val_ds else None,
        warmup_ratio=train_cfg["warmup_ratio"],
        lr_scheduler_type=train_cfg["lr_scheduler_type"],
        optim=train_cfg["optim"],
        report_to=train_cfg.get("report_to", "none"),
        dataloader_num_workers=train_cfg.get("dataloader_num_workers", 0),
        remove_unused_columns=False,
    )

    trainer = SFTTrainer(
        model=model,
        tokenizer=tokenizer,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        dataset_text_field="text",
        max_seq_length=train_cfg["max_seq_length"],
        args=training_args,
    )

    trainer.train()

    # ── Save adapter ──────────────────────────────────────────────
    print(f"\n  Saving adapter to: {out_dir}")
    trainer.model.save_pretrained(out_dir)
    tokenizer.save_pretrained(out_dir)

    print(f"\n  ✓ {domain.upper()} adapter training complete.")
    print(f"  ✓ Adapter saved: {out_dir}\n")
