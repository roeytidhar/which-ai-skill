import urllib.request
import json
import ssl
from typing import List, Dict, Any

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

def fetch_openrouter_models() -> List[Dict[str, Any]]:
    """Fetches live pricing, context, and release dates from OpenRouter."""
    try:
        req = urllib.request.Request('https://openrouter.ai/api/v1/models', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())['data']
    except Exception as e:
        print(f"Error fetching OpenRouter data: {e}")
        return []

def fetch_elo_data() -> Dict[str, float]:
    """Fetches real LMSYS Elo scores from a community open-data mirror."""
    scores = {}
    try:
        # Pulls from an open community JSON mirror
        url = 'https://raw.githubusercontent.com/artificialanalysis/open-data/main/models.json'
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            for item in data:
                model_id = item.get('model_id', '').lower()
                elo = item.get('elo_score', 0)
                if model_id and elo:
                    scores[model_id] = float(elo)
                    # Also map the slug (e.g., 'llama-3-70b' without the provider prefix)
                    scores[model_id.split('/')[-1]] = float(elo)
    except Exception:
        pass # Fails gracefully if offline
    return scores