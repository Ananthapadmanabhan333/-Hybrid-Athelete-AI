"""
merge_datasets.py
-----------------
Merges synthetic datasets with public dataset samples for each domain.
Shuffles deterministically and writes final training-ready JSONL files.

Output files:
  datasets/final/coach_train.jsonl
  datasets/final/coach_val.jsonl
  datasets/final/{nutrition,recovery,medical}_train.jsonl
  datasets/final/{nutrition,recovery,medical}_val.jsonl

Usage:
  python merge_datasets.py --domain all
  python merge_datasets.py --domain coach --synthetic_dir datasets --public_dir datasets/public
"""

import json
import os
import random
import argparse
from typing import List, Dict

random.seed(42)

DOMAINS = ["coach", "nutrition", "recovery", "medical"]


def load_jsonl(path: str) -> List[Dict]:
    """Load all valid samples from a JSONL file."""
    if not os.path.exists(path):
        print(f"  [SKIP] File not found: {path}")
        return []

    samples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                samples.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    print(f"  Loaded {len(samples):,} samples from: {path}")
    return samples


def write_jsonl(samples: List[Dict], path: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for s in samples:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    print(f"  ✓ Written {len(samples):,} → {path}")


def merge_domain(
    domain: str,
    synthetic_dir: str,
    public_dir: str,
    output_dir: str,
    train_split: float = 0.95,
):
    print(f"\n[MERGE] Domain: {domain}")

    # Prefer cleaned files if available, fall back to raw
    synth_clean = os.path.join(synthetic_dir, f"{domain}_dataset_clean.jsonl")
    synth_raw   = os.path.join(synthetic_dir, f"{domain}_dataset.jsonl")
    synth_path  = synth_clean if os.path.exists(synth_clean) else synth_raw

    pub_clean  = os.path.join(public_dir, f"{domain}_public_clean.jsonl")
    pub_raw    = os.path.join(public_dir, f"{domain}_public.jsonl")
    pub_path   = pub_clean if os.path.exists(pub_clean) else pub_raw

    synthetic_samples = load_jsonl(synth_path)
    public_samples    = load_jsonl(pub_path)

    all_samples = synthetic_samples + public_samples
    print(f"  Total before shuffle: {len(all_samples):,}")

    if not all_samples:
        print(f"  [WARN] No samples found for domain={domain}. Skipping.")
        return

    # Tag source for traceability
    for s in synthetic_samples:
        s.setdefault("_source", "synthetic")
    for s in public_samples:
        s.setdefault("_source", "public")

    random.shuffle(all_samples)

    # Split
    split_idx = int(len(all_samples) * train_split)
    train_set = all_samples[:split_idx]
    val_set   = all_samples[split_idx:]

    print(f"  Train: {len(train_set):,}  |  Val: {len(val_set):,}")

    write_jsonl(train_set, os.path.join(output_dir, f"{domain}_train.jsonl"))
    write_jsonl(val_set,   os.path.join(output_dir, f"{domain}_val.jsonl"))


def main():
    parser = argparse.ArgumentParser(description="Fuelix Dataset Merger")
    parser.add_argument("--domain", type=str, default="all",
                        choices=["all"] + DOMAINS)
    parser.add_argument("--synthetic_dir", type=str, default="datasets",
                        help="Directory containing synthetic JSONL files")
    parser.add_argument("--public_dir", type=str, default="datasets/public",
                        help="Directory containing public JSONL files")
    parser.add_argument("--output_dir", type=str, default="datasets/final",
                        help="Output directory for final train/val splits")
    parser.add_argument("--train_split", type=float, default=0.95,
                        help="Fraction for training (rest = validation)")
    args = parser.parse_args()

    domains = DOMAINS if args.domain == "all" else [args.domain]

    for domain in domains:
        merge_domain(
            domain=domain,
            synthetic_dir=args.synthetic_dir,
            public_dir=args.public_dir,
            output_dir=args.output_dir,
            train_split=args.train_split,
        )

    print("\n✓ All domains merged and split.")


if __name__ == "__main__":
    main()
