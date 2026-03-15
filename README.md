# 🏛️ BursaKing: The Quantitative Forge
**An Agentic Intelligence Swarm for Bursa Malaysia Investors**

BursaKing is an advanced financial analysis platform designed to bridge the gap between raw quantitative market data and qualitative investor sentiment. Built for the **Gemini Nexus: The Agentverse** workshop (Track B), it leverages a coordinated swarm of Gemini 3.1 agents to provide retail investors with actionable insights.

---

## 🛰️ System Architecture (A2A Flow)

BursaKing utilizes an **Agent-to-Agent (A2A)** workflow. The system doesn't just "chat"; it orchestrates a specialized sequence where data flows from specialized tools into a reasoning engine to ensure high-fidelity financial reporting.

* **User Request:** A ticker (e.g., `1155.KL`) is sent via the Flutter UI.
* **Quant-Contextualization:** The FastAPI server pre-fetches 30-day OHLC data to "prime" the environment.
* **Agent Handoff:** The **QuantAgent** validates the technical history while the **IntelAgent** performs parallel sentiment analysis.
* **Unified Output:** Results are merged into a single JSON payload containing both the interactive candlestick chart data and the structured intelligence report.

---

## 🤖 Agent Profiles

| Agent | Role | Responsibility |
| :--- | :--- | :--- |
| **QuantAgent** | The Data Forger | Specialized in numerical data retrieval, historical price mapping, and OHLC data formatting for the Syncfusion chart engine. |
| **IntelAgent** | The Market Strategist | Responsible for qualitative analysis. It scans market news, interprets technical trends, and issues the final "GOOD SIGN" or "BAD SIGN" verdict. |

---

## 📂 Project Structure

```text
BURSA_SENTINEL/
├── app/                  # Flutter Frontend (The "Face")
│   ├── lib/              # UI logic and Chart implementation
│   └── pubspec.yaml      # Flutter dependencies
├── server/               # Python Backend (The "Brain")
│   ├── agent.py          # Swarm definition & Agent profiles
│   ├── server.py         # FastAPI endpoints & Orchestration
│   ├── tools.py          # Financial & News tool definitions
│   └── requirements.txt  # Python dependencies
├── .env.example          # Template for Gemini API keys
├── .gitignore            # Git exclusion rules
└── README.md             # Project documentation monitors tool outputs in real-time to bridge the gap between Python's data processing and Flutter's UI requirements.
```
## 🛠️ Setup Instructions

### 1. Prerequisites
* **Flutter SDK** (Stable Channel)
* **Python 3.10+**
* **Google Gemini API Key**

### 2. Backend Installation
```bash
# Navigate to server folder
cd server

# Create and activate virtual environment
python -m venv venv

# Activate on Windows:
.\venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Start the server (Ensure .env is created with GEMINI_API_KEY)
python server.py
```

### 2. Frontend Installation
```bash
# Navigate to app folder
cd app

# Fetch dependencies
flutter pub get

# Run the application
```
🛡️ Technical Resilience
Quota Management: Implemented intelligent fallback logic to handle 429 RESOURCE_EXHAUSTED errors during high-traffic periods.

Data Grounding: Reports are grounded in real-time Yahoo Finance headlines with direct source links to prevent hallucinations.

A2A Observability: The server monitors tool outputs in real-time to bridge the gap between Python's data processing and Flutter's UI requirements.

https://github.com/OwenChong888/bursa_king/blob/576af9ff7c9f23cf0736af054a299b254194db22/mind_map.png

Developed by Chong Tang Jing (OwenChong888) | Electronic Engineering @ Universiti Teknologi Malaysia (UTM)
