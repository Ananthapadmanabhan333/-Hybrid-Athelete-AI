"""
dataset_cleaner.py
------------------
Validates and cleans all JSONL dataset files before training.

Checks:
  1. Valid JSON on every line
  2. Required keys present: instruction, context, response
  3. Minimum response length (no empty responses)
  4. No hallucinated athlete metrics in responses (guardrail check)
  5. Removes duplicates by instruction+response hash

Usage:
  python dataset_cleaner.py --input datasets/coach_dataset.jsonl
                             --output datasets/coach_dataset_clean.jsonl
"""

import json
import hashlib
import os
import re
import argparse
from typing import List, Dict, Any

# ─── Guardrail patterns that indicate fabricated metrics ──────────────────────
# If a response contains these without a corresponding context key, it's suspect.
FABRICATED_METRIC_PATTERNS = [
    r"\b\d+\s?(?:lbs?|kg|calories?|kcal|bpm|mmhg|mg/dl|%)\b",
]

REQUIRED_KEYS = {"instruction", "context", "response"}
MIN_RESPONSE_CHARS = 20
MAX_RESPONSE_CHARS = 4000
MIN_INSTRUCTION_CHARS = 5


def _hash_sample(sample: Dict) -> str:
    key = sample.get("instruction", "") + sample.get("response", "")
    return hashlib.md5(key.encode()).hexdigest()


def _has_suspicious_invention(sample: Dict) -> bool:
    """
    Basic guardrail: if response contains specific numbers but context is empty,
    flag it. We're conservative here — don't reject, just flag.
    """
    response = sample.get("response", "")
    context = sample.get("context", {})

    # If context is populated with numbers, numbers in response are fine
    if any(isinstance(v, (int, float)) for v in context.values()):
        return False

    # If context is essentially empty and response has specific metrics, flag
    if not context or context == {}:
        for pat in FABRICATED_METRIC_PATTERNS:
            if re.search(pat, response, re.IGNORECASE):
                return True
    return False


def clean_file(input_path: str, output_path: str, verbose: bool = False) -> Dict[str, int]:
    stats = {
        "total_read": 0,
        "invalid_json": 0,
        "missing_keys": 0,
        "too_short_response": 0,
        "too_long_response": 0,
        "too_short_instruction": 0,
        "duplicates_removed": 0,
        "guardrail_warnings": 0,
        "written": 0,
    }

    seen_hashes = set()
    cleaned = []

    print(f"  Reading: {input_path}")
    with open(input_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            stats["total_read"] += 1
            line = line.strip()
            if not line:
                continue

            # 1. Valid JSON
            try:
                sample = json.loads(line)
            except json.JSONDecodeError:
                stats["invalid_json"] += 1
                if verbose:
                    print(f"    [L{line_num}] Invalid JSON — skipping")
                continue

            # 2. Required keys
            if not REQUIRED_KEYS.issubset(sample.keys()):
                stats["missing_keys"] += 1
                continue

            instruction = str(sample.get("instruction", "")).strip()
            response = str(sample.get("response", "")).strip()

            # 3. Length checks
            if len(response) < MIN_RESPONSE_CHARS:
                stats["too_short_response"] += 1
                continue

            if len(response) > MAX_RESPONSE_CHARS:
                # Truncate rather than discard
                sample["response"] = response[:MAX_RESPONSE_CHARS]
                stats["too_long_response"] += 1

            if len(instruction) < MIN_INSTRUCTION_CHARS:
                stats["too_short_instruction"] += 1
                continue

            # 4. Deduplicate
            h = _hash_sample(sample)
            if h in seen_hashes:
                stats["duplicates_removed"] += 1
                continue
            seen_hashes.add(h)

            # 5. Guardrail warning (log but do NOT remove — deterministic context may be empty dict)
            if _has_suspicious_invention(sample):
                stats["guardrail_warnings"] += 1

            # Normalize whitespace
            sample["instruction"] = instruction
            sample["response"] = response.strip()

            cleaned.append(sample)

    # Write output
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for s in cleaned:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")

    stats["written"] = len(cleaned)
    return stats


def print_stats(stats: Dict[str, int]):
    print(f"\n  {'─'*40}")
    print(f"  Total read            : {stats['total_read']:>10,}")
    print(f"  Invalid JSON          : {stats['invalid_json']:>10,}")
    print(f"  Missing required keys : {stats['missing_keys']:>10,}")
    print(f"  Response too short    : {stats['too_short_response']:>10,}")
    print(f"  Response too long     : {stats['too_long_response']:>10,}")
    print(f"  Instruction too short : {stats['too_short_instruction']:>10,}")
    print(f"  Duplicates removed    : {stats['duplicates_removed']:>10,}")
    print(f"  Guardrail warnings    : {stats['guardrail_warnings']:>10,}")
    print(f"  ✓ Written             : {stats['written']:>10,}")
    retention = (stats['written'] / stats['total_read'] * 100) if stats['total_read'] > 0 else 0
    print(f"  Retention rate        : {retention:>9.1f}%")
    print(f"  {'─'*40}")


def main():
    parser = argparse.ArgumentParser(description="Fuelix Dataset Cleaner")
    parser.add_argument("--input", type=str, required=True, help="Input JSONL path")
    parser.add_argument("--output", type=str, required=True, help="Output cleaned JSONL path")
    parser.add_argument("--verbose", action="store_true", help="Verbose error output")
    args = parser.parse_args()

    print(f"\n[CLEANER] {args.input} → {args.output}")
    stats = clean_file(args.input, args.output, verbose=args.verbose)
    print_stats(stats)
    print("✓ Cleaning complete.\n")


if __name__ == "__main__":
    main()
