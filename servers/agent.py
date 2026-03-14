import asyncio
import os
from dotenv import load_dotenv

from google.adk.agents import LlmAgent, SequentialAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import your upgraded tools
from servers.tools import get_bursa_price, get_stock_news

# Load environment variables (API Key)
load_dotenv()

# 1. Define Specialist Agents
# The Quant handles the numbers
quant_agent = LlmAgent(
    name="QuantAgent",
    model="gemini-2.5-flash",
    instruction="""
    You are a Bursa Malaysia Data Analyst. 
    1. The user will provide a stock ticker. 
    2. Use 'get_bursa_price' to fetch the current price and change percentage.
    3. State the price and change clearly.
    """,
    tools=[get_bursa_price]
)

# The Intel handles the "Why" and cites evidence
intel_agent = LlmAgent(
    name="IntelAgent",
    model="gemini-2.5-flash",
    instruction="""
    You are a Senior Investment Researcher.
    1. YOUR FIRST TASK: Use the 'get_stock_news' tool to find 3 recent headlines.
    2. If headlines are found: Summarize them and provide the [Source URL] as evidence.
    3. If headlines are NOT found: Explicitly state 'No major news catalysts found in the last 24 hours.' 
    4. Then, pivot to Technical Analysis using the current price and % change.
    """,
    tools=[get_stock_news]
)

# 2. Define the Orchestrator (Sequential Swarm)
bursa_swarm = SequentialAgent(
    name="BursaSentinelSwarm",
    sub_agents=[quant_agent, intel_agent]
)

# 3. Local Test Logic
async def test_swarm():
    print("🚀 Starting Bursa Sentinel Swarm Test...")
    
    # Initialize Session Service and Runner
    session_service = InMemorySessionService()
    runner = Runner(
        app_name="BursaSentinel",
        agent=bursa_swarm,
        session_service=session_service
    )
    
    # --- CRITICAL FIX: PRE-CREATE THE SESSION ---
    user_id = "hackathon_user_01"
    session_id = "session_test_001"
    
    await session_service.create_session(
        app_name="BursaSentinel",
        user_id=user_id,
        session_id=session_id
    )
    
    # Prepare User Input
    user_message = types.Content(
        role="user", 
        parts=[types.Part(text="1155.KL")] # Maybank
    )

    try:
        # Execute the swarm
        async for event in runner.run_async(
            new_message=user_message,
            user_id=user_id,
            session_id=session_id
        ):
            # Log the A2A (Agent-to-Agent) Handoff
            if hasattr(event, 'author') and event.author:
                print(f"Log: {event.author} is processing...")

            # Capture and print the final reasoning
            if hasattr(event, 'content') and event.content and event.content.parts:
                for part in event.content.parts:
                    if part.text:
                        print("\n--- 📈 SENTINEL ANALYSIS ---")
                        print(part.text)
            
            elif hasattr(event, 'error') and event.error:
                print(f"❌ Swarm Error: {event.error}")
                
    except Exception as e:
        print(f"💥 Execution Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_swarm())