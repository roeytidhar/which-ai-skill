import argparse
import sys
import os

# Forces Python to look in the current script's directory for modules
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from engine import ModelRouter

BUDGET_LABELS = {
    "free": 0.0,
    "low": 10.0,
    "medium": 50.0,
    "high": 100.0,
}

def parse_budget(value: str) -> float:
    """Accept both numeric values and labels like 'free', 'low', 'medium', 'high'."""
    label = value.strip().lower()
    if label in BUDGET_LABELS:
        return BUDGET_LABELS[label]
    try:
        return float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"invalid budget value: '{value}'. Use a number or one of: {', '.join(BUDGET_LABELS.keys())}"
        )

def main():
    parser = argparse.ArgumentParser(description="Intent-based LLM routing using open data.")
    parser.add_argument("--budget", type=parse_budget, default=5.00)
    parser.add_argument("--deployment", choices=["cloud", "local"], default="cloud")
    parser.add_argument("--modality", choices=["text", "vision", "coding"], default="text")
    parser.add_argument("--openrouter-file", type=str, default="", help="Path to pre-downloaded openrouter models json")
    parser.add_argument("--elo-file", type=str, default="", help="Path to pre-downloaded elo models json")
    args = parser.parse_args()

    router = ModelRouter(args.budget, args.deployment, args.modality, args.openrouter_file, args.elo_file)
    result = router.get_recommendation()
    
    if "error" in result:
        print(f"### 🤖 which-ai Error\n> {result['error']}")
        sys.exit(0)
        
    print(f"### 🤖 which-ai Recommendation")
    print(f"* **Recommended Model:** `{result['id']}`")
    print(f"* **Intent Parsed:** Deployment: `{args.deployment.upper()}` | Modality: `{args.modality.upper()}`")
    print(f"* **Intelligence Score:** `{result['score']:.0f}` Elo *(Source: {result['source']})*")
    
    if args.deployment == "local":
        print(f"* **System Memory Detected:** `{router.local_ram:.1f} GB RAM`")
        print(f"* **Model RAM Required:** `~{result['required_ram']:.1f} GB`")
        
    print(f"* **Price:** `${result['price']:.2f}` / 1M input tokens")

if __name__ == "__main__":
    main()