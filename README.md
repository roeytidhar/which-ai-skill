<p align="center">
  <img src="which-ai.png" width="800" alt="Which AI Branding">
</p>

# Which AI 🤖

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub release](https://img.shields.io/github/v/release/roeytidhar/which-ai-skills.svg)](https://github.com/roeytidhar/which-ai-skills/releases)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

**Stop guessing which AI model to use.**

The biggest bottleneck in building real AI systems today isn't just the brain. It is the choice. There are hundreds of LLMs and one of the biggest pains is trying to choose the right one without having to be a technical expert in every single benchmark.

If you’re still hardcoding “model-name” into your code, your system is likely already outdated.

---

## Use Cases 💡

- **Dynamic Agent Orchestration**: Automatically route tasks to the most cost-effective or highest intelligence model at runtime.
- **Hardware-Aware Local Deployment**: Ensure local models only run if the system has sufficient RAM and power.
- **Real-Time Benchmarking**: Pull live Elo scores and pricing data to ensure your system always uses the current "best-in-class" model.
- **Automated Agent Generation**: A mandatory requirement for systems that spin up new autonomous agents on the fly.

---

## Key Features ⚙️

| Feature | Description | Real-Time Data Source |
| :--- | :--- | :--- |
| **Hardware Scanning** | Verifies local RAM and power availability for model compatibility. | System Context |
| **Performance Metrics** | Pulls live intelligence (Elo) scores for accuracy matching. | LMBMT / Community |
| **Cost Optimization** | Filters and selects models based on real-time input/output pricing. | OpenRouter API |
| **Intent-Based Routing** | Matches model modality (Coding, Vision, Logic) to task intent. | Skill Heuristics |

---

## Installation & Integration 🚀

### Claude Code & OpenCode
This skill is designed as an atomic, tool-calling primitive.
1. Clone the repository.
2. Copy the `which-ai` folder into your project's skills directory.
3. Ensure your agent has permission to execute bash/python scripts.

### Claude CoWork
Which AI is a first-class Claude CoWork plugin.
1. Open **Claude CoWork**.
2. Click the `+` icon in the **Browse plugins** menu.
3. Select **Add marketplace from GitHub**.
4. Sync `roeytidhar/which-ai-skills`.
5. Install the **Which AI** card.

---

## How it Works 🧠

Which AI acts as a **Real-Time Decision Primitive**. When queried, it bypasses the "static choice" bottleneck by decoupling the decision layer from the execution layer.

1. **Query:** Agent sends parameters (budget, modality, target environment).
2. **Scan:** Which AI fetches live marketplace data and scans local system resources.
3. **Route:** The skill returns the optimal model ID, allowing the agent to proceed with the best possible context.

---

## Contributing 🤝

This is the first of many skills building towards simplified agentic systems. We welcome contributions that add new data sources or platform integrations.

[GitHub Repository](https://github.com/roeytidhar/which-ai-skills)

#AI #AgenticSystems #OpenSource #LLMOps #Claude #WhichAI #Engineering
