"""
train_recovery_adapter.py
-------------------------
Trains the Fuelix Recovery LoRA adapter.

Target dataset size: ~1.5M samples
Domain: recovery scoring, sleep, HRV, fatigue interpretation, deload advice

Usage:
  python train_recovery_adapter.py
  python train_recovery_adapter.py --output_dir /custom/path/recovery_adapter
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _train_base import train_adapter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Fuelix Recovery LoRA Adapter")
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Override output directory (default from config.yaml)"
    )
    args = parser.parse_args()

    print("\n" + "="*60)
    print("  FUELIX — RECOVERY ADAPTER TRAINING")
    print("  Domain: Recovery, sleep, HRV, fatigue management")
    print("="*60)

    train_adapter(domain="recovery", output_dir=args.output_dir)
