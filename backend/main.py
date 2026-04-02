from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import yfinance as yf
import os
from groq import Groq
from dotenv import load_dotenv
from quantum import run_quantum_analysis

load_dotenv()

app = FastAPI(title="Quant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatRequest(BaseModel):
    ticker: str
    quantum: dict
    stock: dict
    history: list
    message: str

@app.get("/")
def root():
    return {"status": "quant api running"}

@app.get("/api/analyze/{ticker}")
def analyze(ticker: str):
    ticker = ticker.upper().strip()

    try:
        t = yf.Ticker(ticker)
        hist = t.history(period="3mo")
        info = t.info

        if hist.empty:
            raise HTTPException(status_code = 404, detail = f"no data found for {ticker}, check if it's used by yfinance")
        
        closes = hist["Close"].tolist()
        volumes = hist["Volume"].tolist()

        current_price = closes[-1]
        prev_price = closes[-2] if len(closes) > 1 else closes[-1]
        change_pct = ((current_price - prev_price) / prev_price) * 100
        high_52week = info.get("fiftyTwoWeekHigh", "n/a")
        low_52week = info.get("fiftyTwoWeekLow", "n/a")
        market_cap = info.get("marketCap", "n/a")
        pe_ratio = info.get("trailingPE", "n/a")
        company_name = info.get("longName", ticker)
        sector = info.get("sector", "unknown")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail = f"Stock data error: {str(e)}")
    
    quantum = run_quantum_analysis(closes, volumes)

    return {
        "ticker": ticker,
        "quantum": quantum,
        "company": company_name,
        "sector": sector,
        "stock": {
            "price": round(current_price, 2), 
            "change": round(change_pct, 2),
            "high": high_52week,
            "low": low_52week,
            "market_cap": market_cap,
            "pe_ratio": pe_ratio,
            "closes": [round(c,2) for c in closes [-30:]]
        }

    }

@app.post("/api/chat")
def chat(request: ChatRequest):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Groq API key not found")
    
    client = Groq(api_key=api_key)

    system_promt = f"""You are Quant, a quantum-inspired AI stock analyst. 
    You have analyzed{request.ticker} at ${request.stock.get('price', '?')}USD, {request.stock.get('change', '?')}% today.
    Quantum readings: bull {request.quantum.get('bull_pct', '?').upper()}.
    Keep responces max 2-4 sentances. Plain text only no emojis or markdowns"""
    
    messages = [{"role": "system", "content": system_promt}]
    for h in request.history[-10:]:
        messages.append({"role": h["role"], "content": h["content"]})
    messages.append({"role": "user", "content": request.message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        max_tokens=300
    )

    return {"reply": response.choices[0].message.content}


    


        