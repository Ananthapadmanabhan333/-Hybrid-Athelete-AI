"""
train_coach_adapter.py
----------------------
Trains the Fuelix Coach LoRA adapter on hybrid athlete coaching data.

Target dataset size: ~5M samples
Domain: general coaching, strength programming, boxing, endurance

Usage:
  python train_coach_adapter.py
  python train_coach_adapter.py --output_dir /custom/path/coach_adapter
"""

import argparse
import sys
import os

# Allow running from project root or ml/fuelix_training directly
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _train_base import train_adapter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Fuelix Coach LoRA Adapter")
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Override output directory (default from config.yaml)"
    )
    args = parser.parse_args()

    print("\n" + "="*60)
    print("  FUELIX — COACH ADAPTER TRAINING")
    print("  Domain: Hybrid coaching, strength, boxing, endurance")
    print("="*60)

    train_adapter(domain="coach", output_dir=args.output_dir)
