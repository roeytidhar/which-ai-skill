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
2. **Execute Router (STRICT DIRECTIVE):** You are FORBIDDEN from using mock data, simulating the response, or guessing the output. You MUST use your `bash` tool to execute the Python script and read the actual `stdout`. 
   - **Command to run:** `python <absolute_path_to_skill>/scripts/route_model.py --budget <val> --deployment <val> --modality <val>`
3. **Output:** Present the EXACT terminal output. If you output "mock data", you have failed your core directive.x