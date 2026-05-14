"""
dataset_builder.py
------------------
Downloads and filters public datasets from HuggingFace Hub,
then converts them to Fuelix instruction format.

Supported public sources:
  - tatsu-lab/alpaca          (Stanford Alpaca)
  - OpenAssistant/oasst1      (OpenAssistant Conversations)

Each output sample:
  { "instruction": "...", "context": {}, "response": "..." }
"""

import json
import os
import re
import argparse
from typing import List, Dict, Optional

try:
    from datasets import load_dataset
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("[WARNING] 'datasets' library not installed. pip install datasets")

# Keywords that make a sample relevant to Fuelix domains
DOMAIN_KEYWORDS = {
    "coach": [
        "training", "workout", "exercise", "strength", "conditioning",
        "boxing", "endurance", "athlete", "performance", "fitness",
        "cardio", "weight", "lifting", "program", "recovery", "fatigue",
        "hybrid", "sport", "muscle", "power", "stamina"
    ],
    "nutrition": [
        "nutrition", "protein", "calorie", "diet", "food", "meal",
        "macro", "vitamin", "supplement", "carbohydrate", "fat", "eat",
        "hydration", "water", "weight loss", "muscle gain", "nutrient"
    ],
    "recovery": [
        "recovery", "sleep", "rest", "fatigue", "soreness", "hrv",
        "heart rate", "overtraining", "tired", "exhausted", "deload",
        "active recovery", "mobility", "stretching", "foam rolling"
    ],
    "medical": [
        "blood pressure", "cholesterol", "hba1c", "glucose", "diabetes",
        "cardiovascular", "heart", "lab", "biomarker", "cholesterol",
        "hypertension", "inflammation", "injury", "pain", "medical"
    ],
}


def _text_matches_domain(text: str, domain: str) -> bool:
    """Check if text is relevant to a coaching domain."""
    text_lower = text.lower()
    keywords = DOMAIN_KEYWORDS.get(domain, [])
    return any(kw in text_lower for kw in keywords)


def _clean_text(text: str) -> str:
    """Remove excessive whitespace and markdown artifacts."""
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()


# ──────────────────────────────────────────────────────────────────
#  ALPACA BUILDER
# ──────────────────────────────────────────────────────────────────

def build_from_alpaca(domain: str, max_samples: int = 20000) -> List[Dict]:
    """
    Load tatsu-lab/alpaca and filter samples relevant to 'domain'.
    Returns samples in Fuelix instruction format.
    """
    if not HF_AVAILABLE:
        print("[SKIP] datasets library not available. Skipping Alpaca.")
        return []

    print(f"  Loading alpaca dataset for domain={domain}...")
    try:
        ds = load_dataset("tatsu-lab/alpaca", split="train")
    except Exception as e:
        print(f"  [ERROR] Failed to load alpaca: {e}")
        return []

    samples = []
    for row in ds:
        instruction = row.get("instruction", "")
        inp = row.get("input", "")
        output = row.get("output", "")

        if not instruction or not output:
            continue

        combined = instruction + " " + inp
        if not _text_matches_domain(combined, domain):
            continue

        ctx = {"source": "alpaca"}
        if inp:
            ctx["additional_context"] = _clean_text(inp)

        samples.append({
            "instruction": _clean_text(instruction),
            "context": ctx,
            "response": _clean_text(output)
        })

        if len(samples) >= max_samples:
            break

    print(f"  ✓ Alpaca [{domain}]: {len(samples):,} samples collected")
    return samples


# ──────────────────────────────────────────────────────────────────
#  OPENASSISTANT BUILDER
# ──────────────────────────────────────────────────────────────────

def build_from_oasst(domain: str, max_samples: int = 10000) -> List[Dict]:
    """
    Load OpenAssistant/oasst1, extract user→assistant pairs,
    filter for domain relevance.
    """
    if not HF_AVAILABLE:
        print("[SKIP] datasets library not available. Skipping OASST.")
        return []

    print(f"  Loading oasst1 dataset for domain={domain}...")
    try:
        ds = load_dataset("OpenAssistant/oasst1", split="train")
    except Exception as e:
        print(f"  [ERROR] Failed to load oasst1: {e}")
        return []

    # Build message tree: parent_id → list of children
    messages = {row["message_id"]: row for row in ds}

    samples = []
    for msg_id, row in messages.items():
        if row["role"] != "prompter":
            continue
        if row["lang"] != "en":
            continue

        user_text = row.get("text", "")
        if not _text_matches_domain(user_text, domain):
            continue

        # Find the top-ranked assistant reply
        children = [m for m in messages.values() if m.get("parent_id") == msg_id
                    and m["role"] == "assistant"]
        if not children:
            continue

        # Pick best-ranked child
        children.sort(key=lambda m: m.get("rank", 999))
        assistant_text = children[0].get("text", "")
        if not assistant_text:
            continue

        samples.append({
            "instruction": _clean_text(user_text),
            "context": {"source": "oasst1"},
            "response": _clean_text(assistant_text)
        })

        if len(samples) >= max_samples:
            break

    print(f"  ✓ OASST [{domain}]: {len(samples):,} samples collected")
    return samples


# ──────────────────────────────────────────────────────────────────
#  COMBINED BUILDER
# ──────────────────────────────────────────────────────────────────

def build_public_dataset(domain: str, output_path: str, max_per_source: int = 10000):
    """
    Combine all public dataset sources for a given domain and write to JSONL.
    """
    print(f"\n[PUBLIC DATASET] Building for domain: {domain}")

    all_samples = []
    all_samples.extend(build_from_alpaca(domain, max_samples=max_per_source))
    all_samples.extend(build_from_oasst(domain, max_samples=max_per_source))

    if not all_samples:
        print(f"  [WARN] No public samples found for domain={domain}")
        return 0

    # Deduplicate by instruction text
    seen = set()
    deduped = []
    for s in all_samples:
        key = s["instruction"][:100]
        if key not in seen:
            seen.add(key)
            deduped.append(s)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for s in deduped:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    print(f"  ✓ Written {len(deduped):,} public samples → {output_path}")
    return len(deduped)


def main():
    parser = argparse.ArgumentParser(description="Fuelix Public Dataset Builder")
    parser.add_argument("--domain", type=str, default="all",
                        choices=["all", "coach", "nutrition", "recovery", "medical"])
    parser.add_argument("--max_per_source", type=int, default=10000,
                        help="Max samples to pull from each public dataset source")
    parser.add_argument("--output_dir", type=str, default="datasets/public")
    args = parser.parse_args()

    domains = ["coach", "nutrition", "recovery", "medical"] if args.domain == "all" else [args.domain]

    total = 0
    for domain in domains:
        out_path = os.path.join(args.output_dir, f"{domain}_public.jsonl")
        n = build_public_dataset(domain, out_path, args.max_per_source)
        total += n

    print(f"\n✓ Public dataset build complete. Total samples: {total:,}")


if __name__ == "__main__":
    main()
