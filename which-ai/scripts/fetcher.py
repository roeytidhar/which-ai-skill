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

def fetch_openrouter_models(openrouter_file: str = "") -> List[Dict[str, Any]]:
    """Fetches live pricing, context, and release dates from OpenRouter."""
    if openrouter_file:
        try:
            with open(openrouter_file, 'r', encoding='utf-8') as f:
                return json.loads(f.read())['data']
        except Exception as e:
            print(f"Error reading local OpenRouter file: {e}")
            
    try:
        req = urllib.request.Request('https://openrouter.ai/api/v1/models', headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return json.loads(response.read().decode())['data']
    except Exception as e:
        print(f"Error fetching OpenRouter data: {e}. Using offline fallback directory.")
        return [
            {"id": "meta-llama/llama-3.2-1b-instruct", "pricing": {"prompt": "0"}, "context_length": 128000, "architecture": {"modality": "text"}, "created": 1727136000},
            {"id": "meta-llama/llama-3.2-3b-instruct", "pricing": {"prompt": "0"}, "context_length": 128000, "architecture": {"modality": "text"}, "created": 1727136000},
            {"id": "microsoft/phi-3-mini-128k-instruct", "pricing": {"prompt": "0"}, "context_length": 128000, "architecture": {"modality": "text"}, "created": 1713830400},
            {"id": "google/gemma-2-2b-it", "pricing": {"prompt": "0"}, "context_length": 8192, "architecture": {"modality": "text"}, "created": 1722470400},
            {"id": "mistralai/mistral-7b-instruct-v0.3", "pricing": {"prompt": "0.05"}, "context_length": 32768, "architecture": {"modality": "text"}, "created": 1716336000},
            {"id": "qwen/qwen-2.5-coder-7b-instruct", "pricing": {"prompt": "0.15"}, "context_length": 32768, "architecture": {"modality": "text"}, "created": 1726704000},
            {"id": "anthropic/claude-3.5-sonnet", "pricing": {"prompt": "3.00"}, "context_length": 200000, "architecture": {"modality": "text"}, "created": 1718841600},
            {"id": "openai/gpt-4o", "pricing": {"prompt": "5.00"}, "context_length": 128000, "architecture": {"modality": "text, image"}, "created": 1715558400}
        ]

def fetch_elo_data(elo_file: str = "") -> Dict[str, float]:
    """Fetches real LMSYS Elo scores from a community open-data mirror."""
    scores = {}
    
    if elo_file:
        try:
            with open(elo_file, 'r', encoding='utf-8') as f:
                data = json.loads(f.read())
                for item in data:
                    model_id = item.get('model_id', '').lower()
                    elo = item.get('elo_score', 0)
                    if model_id and elo:
                        scores[model_id] = float(elo)
                        scores[model_id.split('/')[-1]] = float(elo)
            return scores
        except Exception as e:
            print(f"Error reading local Elo file: {e}")
            
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