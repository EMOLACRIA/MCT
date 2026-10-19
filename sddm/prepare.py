"""Prepare a selected greeter skin without installing or authenticating."""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import adapter_assets

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--theme', choices=adapter_assets.THEMES)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    adapter_assets.stage_greeter(adapter_assets.selected(args.theme), args.destination)
