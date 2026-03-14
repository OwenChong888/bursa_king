import yfinance as yf
import pandas as pd

def get_bursa_price(ticker: str):
    try:
        # 1. Clean the ticker (ensure it ends in .KL for Bursa)
        ticker = ticker.strip().upper()
        if not ticker.endswith(".KL"):
            ticker = f"{ticker}.KL"

        stock = yf.Ticker(ticker)
        # 2. Fetch history (1 month)
        hist = stock.history(period="1mo")

        if hist.empty:
            return {"error": f"No market data found for {ticker}. Check the ticker symbol."}

        # 3. Format history for Flutter
        chart_history = []
        for date, row in hist.iterrows():
            chart_history.append({
                "date": date.strftime('%Y-%m-%d'),
                "open": round(float(row['Open']), 3),
                "high": round(float(row['High']), 3),
                "low": round(float(row['Low']), 3),
                "close": round(float(row['Close']), 3),
            })

        # 4. Return complete dictionary (This prevents the KeyError in server.py)
        return {
            "current_price": round(float(hist['Close'].iloc[-1]), 2),
            "change_percent": round(((hist['Close'].iloc[-1] - hist['Close'].iloc[-2]) / hist['Close'].iloc[-2]) * 100, 2),
            "history": chart_history
        }

    except Exception as e:
        print(f"❌ Tools Error: {e}")
        return {"error": str(e)}
    
def get_stock_news(ticker: str):
    try:
        # Standardize ticker for Bursa
        if ".KL" not in ticker.upper():
            ticker = f"{ticker.upper()}.KL"
            
        stock = yf.Ticker(ticker)
        news = stock.news
        
        if not news or len(news) == 0:
            return "No recent news found for this ticker on Yahoo Finance."
            
        formatted_news = ""
        for article in news[:3]: # Take the top 3
            formatted_news += f"Headline: {article['title']}\nLink: {article['link']}\n\n"
        return formatted_news
    except Exception as e:
        return f"Tool Error: {str(e)}"