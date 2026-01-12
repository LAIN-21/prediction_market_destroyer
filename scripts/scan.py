import sys
from pathlib import Path
import yaml

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.readers.polymarket import read_polymarket
from src.strategies.yes_no import find_yes_no_arbs


def main():
    config_path = project_root / "config" / "settings.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    snapshots = read_polymarket()
    arbs = find_yes_no_arbs(snapshots, config)

    if not arbs:
        print("No arbitrage candidates found.")
        return

    for a in arbs:
        print("=" * 60)
        print(a["question"])
        print(f"YES ask: {a['yes_ask']} (size {a['yes_size']})")
        print(f"NO  ask: {a['no_ask']} (size {a['no_size']})")
        print(f"Total : {a['raw_total']:.4f}")
        print(f"Edge  : {a['edge']:.4f}")
        print(f"Resolution risk: {a['resolution_risk']}")


if __name__ == "__main__":
    main()
