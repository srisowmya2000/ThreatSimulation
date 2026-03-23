# ThreatGraph: AI Cyber Simulation Pipeline 🛡️

ThreatGraph is a locally hosted, multi-agent cybersecurity simulation engine. It extracts real-world public infrastructure topologies (via GraphRAG) and deploys autonomous Red and Blue Team AI agents to actively simulate Advanced Persistent Threat (APT) kill chains against a targeted network perimeter, visually outputting a calculated Breach Probability Forecast.

## ⚠️ Disclaimer
**FOR EDUCATIONAL AND DEFENSIVE PURPOSES ONLY.** 
This tool synthesizes dynamically orchestrated network intrusions and attack pathways. Do NOT point the simulation `target_url` at any infrastructure you do not explicitly own, operate, or have legal authorization to test. The authors are not responsible for any misuse.

## Core Technology Stack
* **Backend:** FastAPI, Python, Uvicorn, CrewAI, Neo4j
* **Frontend:** Vue.js, Vite, Axios, TailwindCSS
* **AI Model Pipeline:** Anthropic (Claude 3 Haiku/Sonnet via structured JSON generation)

## Strict Requirements
* **Python 3.12** (Critical: Python 3.14+ is natively incompatible with the underlying CrewAI and Pydantic bindings. You MUST use Python 3.12 to avoid terminal crashes.)
* **Node.js** (v18+)
* **Anthropic API Key** 

---

## Installation & Setup

### 1. Backend Setup
Open a terminal and navigate to the backend directory:

```bash
cd threat-graph-backend

# Create a Python 3.12 virtual environment (Required)
python3.12 -m venv venv
source venv/bin/activate

# Install the simulation and AI dependencies
pip install -r requirements.txt

# Store your Anthropic token securely
cp .env.example .env
# Open the .env file and add your ANTHROPIC_API_KEY
```

### 2. Frontend Setup
Open a second terminal window and navigate to the dashboard directory:

```bash
cd threat-dashboard

# Install frontend Node modules
npm install
```

---

## Running the Architecture Locally
Because this project utilizes both an API layer and a graphical frontend, you must spin up both services identically in separate terminal windows.

**1. Start the Backend Simulation Engine:**
```bash
cd threat-graph-backend
source venv/bin/activate
uvicorn main:app --reload --port 8000
```
*(Leave this terminal running in the background).*

**2. Start the Interactive Dashboard:**
```bash
cd threat-dashboard
npm run dev
```

### Initiating a Cyber Simulation
1. Once both servers are running, open your web browser to `http://localhost:5173/`.
2. Input your defensive telemetry in the "Active Defenses" box.
3. Select an adversary from the dropdown (e.g., *APT29, LockBit, Cl0p*).
4. Enter an authorized target domain architecture URL.
5. Click **Initiate Assault**. The backend GraphRAG pipeline will spin up parallel parallelized environments and stream the live exploit logs to the UI!
