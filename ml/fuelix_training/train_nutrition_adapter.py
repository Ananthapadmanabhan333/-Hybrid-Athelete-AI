"""
train_nutrition_adapter.py
--------------------------
Trains the Fuelix Nutrition LoRA adapter.

Target dataset size: ~2M samples
Domain: nutrition analysis, macro tracking, meal planning, hydration

Usage:
  python train_nutrition_adapter.py
  python train_nutrition_adapter.py --output_dir /custom/path/nutrition_adapter
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _train_base import train_adapter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Fuelix Nutrition LoRA Adapter")
    parser.add_argument(
        "--output_dir",
        type=str,
        default=None,
        help="Override output directory (default from config.yaml)"
    )
    args = parser.parse_args()

    print("\n" + "="*60)
    print("  FUELIX — NUTRITION ADAPTER TRAINING")
    print("  Domain: Nutrition analysis, macros, meal planning")
    print("="*60)

    train_adapter(domain="nutrition", output_dir=args.output_dir)
