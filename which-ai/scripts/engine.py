import re
import time
from typing import Dict, Any
import hardware
import fetcher

class ModelRouter:
    OPEN_BRANDS = ['llama', 'qwen', 'mistral', 'gemma', 'deepseek', 'pixtral', 'phi']

    def __init__(self, budget: float, deployment: str, modality: str):
        self.budget = budget
        self.deployment = deployment
        self.modality = modality
        self.is_local = (deployment == "local")
        self.local_ram = hardware.get_system_ram_gb() if self.is_local else 999.0
        
        # Load the real Elo scores into memory
        self.elo_data = fetcher.fetch_elo_data()

    def estimate_elo(self, model_id: str, price_per_m: float, context: int, created_timestamp: int) -> float:
        """Fallback heuristic: Estimates Elo for brand new models that aren't on the leaderboard yet."""
        elo = 1050.0 # Base modern model score
        model_name_lower = model_id.lower()
        
        # 1. Parameter Bonus
        param_match = re.search(r'([0-9]+(?:\.[0-9]+)?)b', model_name_lower)
        if param_match:
            elo += float(param_match.group(1)) * 1.5
            
        # 2. Recency Bonus
        current_time = time.time()
        safe_timestamp = created_timestamp if created_timestamp > 0 else (current_time - 31536000)
        age_in_days = (current_time - safe_timestamp) / (60 * 60 * 24)
        if age_in_days < 180:
            elo += (180 - age_in_days) * 0.6 
            
        # 3. Market Tier Proxy
        if not self.is_local:
            if price_per_m >= 10.0: elo += 100
            elif price_per_m >= 2.0: elo += 50
            
        # 4. Context & Modality
        elo += min((context / 10000), 25.0)
        if self.modality == "coding" and ("coder" in model_name_lower or "code" in model_name_lower):
            elo += 40
            
        return min(elo, 1320.0) # Cap the estimate so it doesn't break the scale

    def get_recommendation(self) -> Dict[str, Any]:
        models_data = fetcher.fetch_openrouter_models()
            
        valid_models = []
        for model in models_data:
            model_id = model.get('id', '')
            price_per_m = float(model.get('pricing', {}).get('prompt', 0)) * 1000000
            context = int(model.get('context_length', 0))
            architecture = model.get('architecture', {}).get('modality', '').lower()
            created_timestamp = int(model.get('created', 0))
            
            if self.is_local:
                if not any(brand in model_id.lower() for brand in self.OPEN_BRANDS): continue
                req_ram = hardware.estimate_ram_required(model_id)
                if req_ram > (self.local_ram - 1.5): continue
                price_per_m = 0.0
                
            if self.modality == "vision" and 'image' not in architecture: continue
            if price_per_m > self.budget and not self.is_local: continue
                
            # HYBRID SCORING: Try to get real Elo, otherwise estimate it
            slug = model_id.split('/')[-1].lower()
            real_elo = self.elo_data.get(model_id.lower()) or self.elo_data.get(slug)
            
            if real_elo:
                final_score = real_elo
                score_source = "LMSYS/Community Mirror"
            else:
                final_score = self.estimate_elo(model_id, price_per_m, context, created_timestamp)
                score_source = "Dynamic Heuristic Estimate"
                
            valid_models.append({
                'id': model_id, 'price': price_per_m, 'score': final_score,
                'source': score_source,
                'required_ram': hardware.estimate_ram_required(model_id) if self.is_local else 0
            })

        if not valid_models:
            return {"error": f"No models matched your criteria (Budget: ${self.budget}, RAM: {self.local_ram:.1f}GB)."}
            
        return sorted(valid_models, key=lambda x: x['score'], reverse=True)[0]