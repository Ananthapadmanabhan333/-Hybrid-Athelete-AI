"""
train_medical_adapter.py
------------------------
Trains the Fuelix Medical LoRA adapter.

Target dataset size: ~1M samples
Domain: lab value explanations, health risk flags, medical context for athletes

IMPORTANT: This adapter NEVER prescribes treatment or makes diagnoses.
           All outputs include mandatory medical disclaimer injection.

Usage:
  python train_medical_adapter.py
  python train_medical_adapter.py --output_dir /custom/path/medical_adapter
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _train_base import train_adapter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Fuelix Medical LoRA Adapter")
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Override output directory (default from config.yaml)"
    )
    args = parser.parse_args()

    print("\n" + "="*60)
    print("  FUELIX — MEDICAL ADAPTER TRAINING")
    print("  Domain: Lab value explanations and health risk flags")
    print("  !! GUARDRAIL: No diagnosis, no prescription !!")
    print("="*60)

    train_adapter(domain="medical", output_dir=args.output_dir)
