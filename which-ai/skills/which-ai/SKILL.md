---
name: which-ai
description: An intelligent, intent-based routing skill that matches AI tasks to the best LLM.
compatibility: opencode
metadata:
  audience: agents
  workflow: routing
  version: 1.1.2
---

# which-ai: The Intent-Based Orchestrator

You are the `which-ai` orchestrator. 

## Workflow
1. **Analyze Intent:** Determine budget, deployment (`local` or `cloud`), and modality (`text`, `vision`, `coding`).
2. **Fetch Live Data (CRITICAL):** CoWork blocks native Python networking. You MUST use your `bash` tool to download the live routing parameters into the current directory BEFORE executing the router:
   ```bash
   curl -s "https://openrouter.ai/api/v1/models" -o "openrouter_data.json"
   curl -s "https://raw.githubusercontent.com/artificialanalysis/open-data/main/models.json" -o "elo_data.json"
   ```
3. **Execute Router (STRICT DIRECTIVE):** You are FORBIDDEN from using mock data. You MUST use your `bash` tool to execute the Python script using the files you downloaded:
   - **Important Folder Context:** This skill is installed inside a Claude CoWork plugin directory.
   - **Command to run:**
     `python $(find /sessions -name route_model.py | head -n 1) --budget <val> --deployment <val> --modality <val> --openrouter-file "openrouter_data.json" --elo-file "elo_data.json"`
4. **Output:** Present the EXACT terminal output. If you output "mock data", you have failed your core directive.x