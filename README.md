# Simple quantum stock analyser

Quantum inspired web app that uses yfinace for real stock data, and simple quantum mechanic equasions.
 
## Live URL
 
**Frontend**: https://quantstockanalyser.vercel.app/

**Backend**: https://quantstockanalyser.onrender.com

## How to use
in the "TICKER..." bracket you put in your stock name that is recognised by yahoo finance (if you're not sure if the name will be recognised you can check at: https://finance.yahoo.com/?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAIlZx8oCgU-9PuLiTiejMql5M5dESiZdq3h4kvCypenMClHk9cWoGMbR9LcjgD4eIeKEluTK-lswiXsTuQyTMaJHXVjpd1_imwN1ftvANSweM4z4rTVEQyVH0YysOJYR7cqq4Doue9tbXVI1eS9mApOyd5ACK520nd03QRGmw2_D) after you put your stock in you can hit analyse and the app will output the analysis. The black dot on the right bottom of the screen is an AI chat box that you are free to use by clicking on it. If you want to analyse another stock you can refresh the page.
 
## What it does
 
Ater entering a given stock the app fetches the last 3 months of real stock data from Yahoo Finance, runs a simple quantum-inspired math using probability amplitudes (α, β, γ) for bull, neutral and bear states, than it applyies Hadamard-like mixing and quantum interference based on volume-weighted momentum, it also calculates quantum metrics like entanglement, coherence, and Heisenberg uncertainty, thean it reaturns a 30-day price chart with a 7-day quantum prediction line.
You can also ask the AI chat some questions about the analysis (uses GROQ API)
 
## How the quantum math works
 
The model treats each stock as a quantum system in superposition across three states:
**Returns** 
daily % price changes calculated from closing prices
**Amplitude extraction**
fraction of bull/neutral/bear days as raw amplitudes (α, β, γ)
**Interference**
recent volume-weighted momentum boosts
**Normalization**
enforces quantum probability rule: |α|^2 + |β|^2 + |γ|^2 = 1 
**Wave function collapse**
the dominant state is the predicted direction
**Metrics**
uses: Von Neumann entropy, off-diagonal coherence, Heisenberg uncertainty
 
## Tech Stack
 
**Backend**
- Python + FastAPI
- yfinance (Yahoo Finance data)
- NumPy (math)
- Groq API with LLaMA 3.3 70B
 
**Frontend**
- Plain HTML
- Canvas API for price chart + prediction line
- DM Sans + DM Mono fonts
 
**Deployment**
- Backend: Render
- Frontend: Vercel
 
## Project Structure
 
```
quantstockanalyzer/
backend/
    main.py           
        quantum.py        
        requirements.txt  
        .env              
    frontend/
        index.html        
```
 
## Running locally
 
**Backend**
```bash
cd backend
pip install -r requirements.txt
cp .env.example .env  # add a GROQ_API_KEY
uvicorn main:app --reload
```
 
**Frontend**
```bash
cd frontend
python -m http.server 5500
```
 
Then open `http://127.0.0.1:5500` in your browser.
 
## Environment Variables
 
`GROQ_API_KEY` | Your Groq API key from console.groq.com |
 
## Disclaimer
 
Please do not use this as actual financial guide lines this was made for informational and enjoyment purposes only!
 
