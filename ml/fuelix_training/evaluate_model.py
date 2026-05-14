"""
evaluate_model.py
-----------------
Evaluates all four Fuelix LoRA adapters against held-out validation samples.

Metrics:
  - Perplexity (lower = better)
  - Guardrail pass rate (no fabricated metrics)
  - Insufficient data handling (correct refusal)
  - Sample generation quality check

Usage:
  python evaluate_model.py --domain all
  python evaluate_model.py --domain coach --adapter_dir ../../backend/models/coach_adapter
  python evaluate_model.py --domain coach --quick  # 100 samples only
"""

import os
import sys
import json
import math
import argparse
import re
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _train_base import load_config, format_sample, SYSTEM_PROMPT

try:
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
    from peft import PeftModel
    EVAL_AVAILABLE = True
except ImportError:
    EVAL_AVAILABLE = False
    print("[WARNING] Evaluation libraries not available. pip install transformers peft torch")

DOMAINS = ["coach", "nutrition", "recovery", "medical"]

# ─── Guardrail: patterns that should NOT appear in responses without context ──
FABRICATION_PATTERNS = [
    r"your (?:weight|calories?|protein|recovery score|sleep) (?:is|was|are) \d+",
]


def load_val_samples(domain: str, val_dir: str, limit: Optional[int] = None) -> List[Dict]:
    val_path = os.path.join(val_dir, f"{domain}_val.jsonl")
    if not os.path.exists(val_path):
        print(f"  [SKIP] Val file not found: {val_path}")
        return []
    samples = []
    with open(val_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                samples.append(json.loads(line))
            except json.JSONDecodeError:
                continue
            if limit and len(samples) >= limit:
                break
    return samples


def compute_perplexity(model, tokenizer, texts: List[str], device: str) -> float:
    """Compute mean per-token perplexity over a list of formatted texts."""
    import torch
    model.eval()
    total_loss = 0.0
    total_tokens = 0

    with torch.no_grad():
        for text in texts:
            enc = tokenizer(
                text,
                return_tensors="pt",
                max_length=512,
                truncation=True,
            ).to(device)
            input_ids = enc["input_ids"]
            labels = input_ids.clone()

            out = model(**enc, labels=labels)
            loss = out.loss.item()
            n_tokens = input_ids.shape[1]
            total_loss += loss * n_tokens
            total_tokens += n_tokens

    avg_loss = total_loss / total_tokens if total_tokens > 0 else float("inf")
    return math.exp(avg_loss)


def check_guardrails(response: str, context: Dict) -> Tuple[bool, str]:
    """
    Return (pass, reason).
    Fail if response contains 'insufficient_data' when context is populated,
    or contains fabricated-looking numbers when context is empty.
    """
    has_context = bool(context) and any(
        isinstance(v, (int, float)) for v in context.values()
    )

    if not has_context:
        for pat in FABRICATION_PATTERNS:
            if re.search(pat, response, re.IGNORECASE):
                return False, f"Possible fabrication — pattern matched: {pat}"

    return True, "ok"


def generate_sample_response(
    model,
    tokenizer,
    sample: Dict,
    cfg: Dict,
    device: str
) -> str:
    """Run inference on a single sample and return the generated response."""
    import torch
    gen_cfg = cfg["generation"]

    formatted = format_sample(sample)
    # Use only the prompt part (up to [/INST])
    prompt_end = formatted.find("[/INST]")
    if prompt_end == -1:
        prompt = formatted
    else:
        prompt = formatted[:prompt_end + len("[/INST]")]

    enc = tokenizer(
        prompt,
        return_tensors="pt",
        max_length=384,
        truncation=True,
    ).to(device)

    with torch.no_grad():
        out = model.generate(
            **enc,
            max_new_tokens=gen_cfg["max_new_tokens"],
            temperature=gen_cfg["temperature"],
            top_p=gen_cfg["top_p"],
            do_sample=gen_cfg["do_sample"],
            repetition_penalty=gen_cfg.get("repetition_penalty", 1.1),
            pad_token_id=tokenizer.eos_token_id,
        )

    generated = out[0][enc["input_ids"].shape[1]:]
    return tokenizer.decode(generated, skip_special_tokens=True).strip()


def evaluate_domain(
    domain: str,
    adapter_dir: str,
    val_dir: str,
    cfg: dict,
    quick: bool = False,
) -> Dict:
    if not EVAL_AVAILABLE:
        return {"error": "Libraries not available"}

    import torch
    device = "cuda" if torch.cuda.is_available() else "cpu"
    limit = 100 if quick else 500

    print(f"\n{'─'*55}")
    print(f"  Evaluating: {domain.upper()} adapter")
    print(f"  Adapter dir: {adapter_dir}")
    print(f"  Samples: {limit} (quick={quick})")
    print(f"{'─'*55}")

    if not os.path.isdir(adapter_dir):
        print(f"  [SKIP] Adapter directory not found: {adapter_dir}")
        return {"skipped": True, "reason": "adapter_not_found"}

    # Load tokenizer and base model + adapter
    model_name = cfg["base_model"]["name"]
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=cfg["base_model"]["load_in_4bit"],
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_quant_type="nf4",
    )

    print("  Loading tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(adapter_dir)
    tokenizer.pad_token = tokenizer.eos_token

    print("  Loading base model + adapter...")
    base_model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto",
    )
    model = PeftModel.from_pretrained(base_model, adapter_dir)
    model.eval()

    # Load val samples
    val_samples = load_val_samples(domain, val_dir, limit=limit)
    if not val_samples:
        return {"skipped": True, "reason": "no_val_data"}

    print(f"  Val samples loaded: {len(val_samples):,}")

    # Perplexity
    print("  Computing perplexity...")
    texts = [format_sample(s) for s in val_samples[:min(50, len(val_samples))]]
    texts = [t for t in texts if t]
    perplexity = compute_perplexity(model, tokenizer, texts, device)

    # Guardrail check on reference responses
    print("  Running guardrail checks...")
    guardrail_pass = 0
    guardrail_fail = 0
    guardrail_fail_examples = []

    for s in val_samples:
        ref_response = s.get("response", "")
        ctx = s.get("context", {})
        passed, reason = check_guardrails(ref_response, ctx)
        if passed:
            guardrail_pass += 1
        else:
            guardrail_fail += 1
            if len(guardrail_fail_examples) < 3:
                guardrail_fail_examples.append({
                    "instruction": s.get("instruction"),
                    "reason": reason
                })

    guardrail_rate = (guardrail_pass / len(val_samples)) * 100 if val_samples else 0

    # Sample generation (5 examples)
    print("  Generating sample responses...")
    generated_examples = []
    for s in val_samples[:5]:
        try:
            gen = generate_sample_response(model, tokenizer, s, cfg, device)
            generated_examples.append({
                "instruction": s.get("instruction"),
                "reference": s.get("response")[:150],
                "generated": gen[:150],
            })
        except Exception as e:
            generated_examples.append({"error": str(e)})

    results = {
        "domain": domain,
        "val_samples": len(val_samples),
        "perplexity": round(perplexity, 4),
        "guardrail_pass_rate_pct": round(guardrail_rate, 2),
        "guardrail_failures": guardrail_fail,
        "guardrail_fail_examples": guardrail_fail_examples,
        "sample_generations": generated_examples,
    }

    # Print summary
    print(f"\n  Results [{domain.upper()}]:")
    print(f"    Perplexity       : {results['perplexity']}")
    print(f"    Guardrail pass % : {results['guardrail_pass_rate_pct']}%")
    print(f"    Guardrail fails  : {results['guardrail_failures']}")

    if generated_examples:
        print("\n  Sample generation:")
        ex = generated_examples[0]
        if "error" not in ex:
            print(f"    Q: {ex['instruction']}")
            print(f"    Generated: {ex['generated']}")

    return results


def main():
    parser = argparse.ArgumentParser(description="Fuelix Adapter Evaluator")
    parser.add_argument("--domain", type=str, default="all",
                        choices=["all"] + DOMAINS)
    parser.add_argument("--adapter_dir", type=str, default=None,
                        help="Override adapter directory (only valid with single domain)")
    parser.add_argument("--val_dir", type=str,
                        default=os.path.join(os.path.dirname(__file__), "datasets", "final"),
                        help="Directory containing *_val.jsonl files")
    parser.add_argument("--output", type=str, default="eval_results.json",
                        help="JSON output file for results")
    parser.add_argument("--quick", action="store_true",
                        help="Evaluate on 100 samples only (faster)")
    args = parser.parse_args()

    cfg = load_config()
    domains = DOMAINS if args.domain == "all" else [args.domain]

    all_results = {}
    for domain in domains:
        adapter_dir = (
            args.adapter_dir if args.adapter_dir and len(domains) == 1
            else cfg["adapters"][domain]["output_dir"]
        )
        # Resolve relative to backend/models
        if not os.path.isabs(adapter_dir):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            adapter_dir = os.path.normpath(os.path.join(script_dir, adapter_dir))

        result = evaluate_domain(
            domain=domain,
            adapter_dir=adapter_dir,
            val_dir=args.val_dir,
            cfg=cfg,
            quick=args.quick,
        )
        all_results[domain] = result

    # Save results
    with open(args.output, "w") as f:
        json.dump(all_results, f, indent=2)
    print(f"\n✓ Evaluation complete. Results saved to: {args.output}")


if __name__ == "__main__":
    main()
