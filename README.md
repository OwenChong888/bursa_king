🏛️ BursaKing: The Quantitative ForgeAn Agentic Intelligence Swarm for Bursa Malaysia InvestorsBursaKing is an advanced financial analysis platform designed to bridge the gap between raw quantitative market data and qualitative investor sentiment. Built for the Gemini Nexus: The Agentverse workshop (Track B), it leverages a coordinated swarm of Gemini 3.1 agents to provide retail investors with actionable insights.🛰️ System Architecture (A2A Flow)BursaKing utilizes an Agent-to-Agent (A2A) workflow. The system doesn't just "chat"; it orchestrates a specialized sequence where data flows from specialized tools into a reasoning engine to ensure high-fidelity financial reporting.User Request: A ticker (e.g., 1155.KL) is sent via the Flutter UI.Quant-Contextualization: The FastAPI server pre-fetches 30-day OHLC data to "prime" the environment.Agent Handoff: The QuantAgent validates the technical history while the IntelAgent performs parallel sentiment analysis.Unified Output: Results are merged into a single JSON payload containing both the interactive candlestick chart data and the structured intelligence report.🤖 Agent ProfilesAgentRoleResponsibilityQuantAgentThe Data ForgerSpecialized in numerical data retrieval, historical price mapping, and OHLC data formatting for the Syncfusion chart engine.IntelAgentThe Market StrategistResponsible for qualitative analysis. It scans market news, interprets technical trends, and issues the final "GOOD SIGN" or "BAD SIGN" verdict.🛠️ Setup Instructions1. PrerequisitesFlutter SDK (Stable)Python 3.10+Google Gemini API Key (Gemini 3.1 Pro recommended)2. Backend Setup (Python)Navigate to the /server directory:Bash# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Configure Environment
# Create a .env file and add:
# GEMINI_API_KEY=your_actual_key_here

# Start the server
python server.py
3. Frontend Setup (Flutter)Navigate to the /app directory:Bash# Fetch dependencies
flutter pub get

# Run the application (Chrome recommended for demo)
flutter run -d chrome
🛡️ Technical ResilienceQuota Management: Implemented an intelligent fallback mechanism and error handling to manage 429 RESOURCE_EXHAUSTED errors during high-traffic periods.Data Grounding: Every "Intel Report" is grounded in real-time Yahoo Finance headlines with direct source links to prevent LLM hallucinations.A2A Observability: The server monitors tool outputs in real-time to bridge the gap between Python's data processing and Flutter's UI requirements.Developed by Chong Tang Jing (OwenChong888) | Electronic Engineering @ Universiti Teknologi Malaysia (UTM)
