# Probabilistic Forecasting Engine: Swarm Intelligence for Proactive Cyber Defense

## Overview
This platform acts as a Probabilistic Forecasting Engine, elevating traditional threat modeling into a live, interactive knowledge graph powered by **Anthropic's Claude 3 Models**. It uses a specialized swarm of CrewAI Agents mapped against the MITRE ATT&CK framework to autonomously simulate cyberattacks against your exact organizational architecture and compute a localized **Breach Probability Score**.

### Core Architecture
- **Knowledge Graph (Neo4j)**: Uses Graph Retrieval-Augmented Generation (GraphRAG) to dynamically extract entities (Hosts, Services, Threat Actors, Defenses) and their complex interdependencies from unstructured text (e.g., web scraping, CVE descriptions, architectural diagrams).
- **FastAPI Backend**: Orchestrates the API layer and the multi-agent worker processes.
- **Agentic Swarm (CrewAI)**: Connects a red team (Attacker Agent), an infrastructure state manager (Environment Agent), and a blue team validator (Defender Agent) in an adversarial loop bounded by Zep persistent memory.
- **Multiprocessing Simulation Loop**: Employs parallel `multiprocessing` processes to branch "simulation worlds," enabling probabilistic forecasts of attack success rates across hundreds of potential attack vectors.
- **Vue.js Dashboard**: A cyberpunk-themed, dark mode front-end to observe the real-time simulation feed, the MITRE ATT&CK heatmap, and to download the aggregated PDF security reports.

## Key Features

### 1. Automated Graph Ingestion (`ingest.py`)
Feed the engine a simple URL. It fetches the domain's HTML, determines the likely technical stack and vulnerabilities behind it, and pipelines that context natively into the Neo4j Threat Graph. 

### 2. Multi-World Simulation Loops (`simulation.py`)
Rather than relying on a deterministic checklist, the system runs 5 isolated multi-step reasoning simulations in parallel. The Attacker Agent evaluates the live topology state to map lateral movement strategies using Extended Thinking/Prompt Caching algorithms to simulate zero-day behavior patterns.

### 3. Automated Executive Reporting (`reporter.py`)
Generates actionable mathematical intelligence based on the outcomes of the probabilistic swarm.
- **Breach Probability Score**: Aggregated success likelihood.
- **ATT&CK Heatmap**: Frequency usage matrix mapping detected vs undocumented threat paths.
- **PDF Generation**: Outputs professional executive summaries using `reportlab`.

## Quick Start
### Prerequisites
- Python 3.10+
- Node.js & npm (for Vue Dashboard)
- Docker Desktop (for local Neo4j)

### Setup
1. Clone the repository.
2. Start the local Neo4j database using `docker-compose up -d`.
3. Fill your `ANTHROPIC_API_KEY` in the environment (`export ANTHROPIC_API_KEY=...` or `.env`).
4. Install backend dependencies: `pip install -r requirements.txt`.
5. CD into `threat-dashboard` and run `npm install` followed by `npm run dev` to start the dashboard.

### Typical Workflow
1. **Scrape**: `python ingest.py https://yourcompany.com`
2. **Forecast**: `python simulation.py`
3. **Analyze**: `python reporter.py`
4. **View result**: Open `http://localhost:5173` to see the results.

## Contributing
Refer to `docs/` for more detailed subsystem architecture diagrams and integration patterns.
