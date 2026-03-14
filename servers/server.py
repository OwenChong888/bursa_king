import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import your swarm and tool from your other files
from servers.agent import bursa_swarm
from servers.tools import get_bursa_price 

app = FastAPI()

# 1. Setup CORS for Flutter Web & Mobile
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_service = InMemorySessionService()

@app.get("/")
async def health():
    return {"status": "Swarm Online", "model": "Gemini 3.1 Pro"}

@app.post("/analyze")
async def analyze_stock(ticker: str):
    user_id = "utm_student_chong"
    session_id = f"session_{ticker}" 

    # 2. Fetch fresh price data
    market_data = get_bursa_price(ticker)
    
    # Check if there was an error or if data is missing
    if "error" in market_data:
        return {
            "analysis": f"Market Data Error: {market_data['error']}",
            "history": []
        }

    # Now it's safe to access 'current_price'
    price_context = (
        f"Current Price: {market_data['current_price']}, "
        f"Change: {market_data.get('change_percent', 0)}%"
    )

    try:
        await session_service.create_session(
            app_name="BursaSentinel",
            user_id=user_id,
            session_id=session_id
        )
    except Exception:
        pass

    runner = Runner(
        app_name="BursaSentinel",
        agent=bursa_swarm,
        session_service=session_service
    )

    # 3. Prompt the Swarm (FIXED: using price_context)
    prompt = (
        f"Analyze {ticker}. Context: {price_context}. "
        "Calculate the % move, provide a clear 'GOOD SIGN' or 'BAD SIGN' verdict, "
        "and explain the 30-day trend shown in the data."
    )
    
    user_message = types.Content(role="user", parts=[types.Part(text=prompt)])
    final_analysis = ""

    try:
        print(f"🚀 Swarm analyzing: {ticker}")
        
        async for event in runner.run_async(
            new_message=user_message,
            user_id=user_id,
            session_id=session_id
        ):
            # Error Handling
            if hasattr(event, 'error') and event.error:
                print(f"❌ Swarm Error: {event.error}")
                return {"analysis": f"Error: {event.error}", "history": market_data.get("history", [])}

            # Capture IntelAgent's final response
            if hasattr(event, 'content') and event.content:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        final_analysis = part.text

        # 4. Return combined JSON payload
        return {
            "analysis": final_analysis,
            "history": market_data.get("history", []),
            "current_price": market_data.get("current_price"),
            "change_percent": market_data.get("change_percent")
        }

    except Exception as e:
        print(f"💥 Server Error: {e}")
        return {"analysis": f"Internal Server Error: {str(e)}", "history": []}

if __name__ == "__main__":
    # Use reload=True only for development
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)