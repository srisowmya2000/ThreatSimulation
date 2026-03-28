# 🕸️ ThreatGraph  
### AI-Powered Cyber Simulation • Swarm Intelligence • Attack Path Forecasting

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-111111?style=for-the-badge&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-Backend-111111?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/Vue.js-Dashboard-111111?style=for-the-badge&logo=vuedotjs" />
  <img src="https://img.shields.io/badge/Neo4j-Knowledge%20Graph-111111?style=for-the-badge&logo=neo4j" />
  <img src="https://img.shields.io/badge/CrewAI-Multi--Agent-111111?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Anthropic-Claude-111111?style=for-the-badge" />
</p>

<p align="center">
  <b>Probabilistic Forecasting Engine for Proactive Cyber Defense</b>
</p>

<p align="center">
  ThreatGraph is a locally hosted, AI-assisted cyber simulation platform that models attack paths, simulates adversary behavior, and estimates breach probability using swarm-style Red vs. Blue team reasoning.
</p>

---

## ⚠️ Defensive-Only Disclaimer

> **For educational, defensive, and authorized security testing only.**  
> Do **not** point the simulation at any infrastructure you do not explicitly own, operate, or have written permission to assess.  
> This project is designed for **defensive threat modeling, attack path analysis, and cyber resilience experimentation**.

---

## 📸 Live Dashboard Preview

<p align="center">
    <img width="1131" height="1238" alt="image" src="https://github.com/user-attachments/assets/f2fd27a2-6d9b-43bf-9bc3-8c202733b661" />
</p>

<p align="center">
  <i>Interactive dashboard showing adversary selection, active defenses, target modeling, and live simulation telemetry.</i>
</p>

⭐ If you find ThreatSimulation useful, starring the repo helps others discover it — thank you!
---

## 🚀 What ThreatGraph Does

ThreatGraph combines:

- **GraphRAG-style topology extraction**
- **Knowledge graph modeling with Neo4j**
- **Multi-agent Red Team / Blue Team simulation**
- **Adversary playbook selection**
- **Attack path correlation**
- **Probabilistic breach forecasting**
- **Live dashboard telemetry**

Instead of treating security as a checklist, ThreatGraph attempts to answer:

> **“Given this architecture, these defenses, and this threat actor — how likely is a meaningful breach path?”**



---

## 🧠 Core Concept

Traditional scanners answer:

- “What vulnerabilities exist?”

ThreatGraph aims to answer:

- **Which attack paths are actually plausible?**
- **Which controls meaningfully reduce breach probability?**
- **How would a specific threat actor chain weaknesses together?**
- **What happens when multiple agents explore the topology in parallel?**

This makes the project useful for:

- proactive cyber defense
- threat modeling
- attack path analysis
- security architecture reviews
- tabletop simulation concepts
- AI-assisted adversary emulation (defensive context)

---

## 🏗️ High-Level Architecture

```text
                ┌──────────────────────────────┐
                │   Target Domain / Infra URL  │
                └──────────────┬───────────────┘
                               │
                               ▼
                 ┌─────────────────────────────┐
                 │  GraphRAG / Topology Ingest │
                 │  Public Infra + Tech Signals│
                 └──────────────┬──────────────┘
                                │
                                ▼
                 ┌─────────────────────────────┐
                 │   Neo4j Knowledge Graph     │
                 │ Hosts • Services • Controls │
                 │ Paths • Weaknesses • Assets │
                 └──────────────┬──────────────┘
                                │
                                ▼
             ┌────────────────────────────────────────┐
             │ Multi-Agent Simulation Orchestrator    │
             │ CrewAI Red / Blue Parallel Reasoning   │
             └───────┬───────────────────────┬────────┘
                     │                       │
                     ▼                       ▼
         ┌──────────────────────┐   ┌──────────────────────┐
         │ Red Team Agents      │   │ Blue Team Agents     │
         │ Attack path search   │   │ Defensive response   │
         │ TTP chaining         │   │ Control evaluation   │
         └──────────┬───────────┘   └──────────┬───────────┘
                    └──────────────┬────────────┘
                                   ▼
                    ┌────────────────────────────┐
                    │ Breach Probability Engine  │
                    │ Risk Score + Path Evidence │
                    └──────────────┬─────────────┘
                                   ▼
                    ┌────────────────────────────┐
                    │ Vue Dashboard + Telemetry  │
                    │ Logs • Score • Simulation  │
                    └────────────────────────────┘






