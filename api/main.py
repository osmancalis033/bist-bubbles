from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import os

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"], allow_headers=["*"])

API_KEY = os.environ.get("TWELVE_API_KEY", "")

STOCKS = [
    "THYAO","GARAN","AKBNK","YKBNK","SISE","KCHOL","SAHOL","TCELL",
    "BIMAS","ASELS","FROTO","TOASO","TUPRS","ARCLK","EREGL","PETKM",
    "ENKAI","SODA","KOZAL","KOZAA","MAVI","CCOLA","TTKOM","PGSUS",
    "TAVHL","MGROS","ULKER","DOHOL","EKGYO","ISCTR","HALKB","VAKBN",
    "LOGO","AEFES","OTKAR","TRKCM","VESTL","GUBRF","DOAS","HEKTS",
]

@app.get("/api/quotes")
async def quotes():
    if not API_KEY:
        raise HTTPException(500, "API key eksik")
    
    symbols = ",".join(STOCKS)
    url = f"https://api.twelvedata.com/quote?symbol={symbols}&exchange=BIST&apikey={API_KEY}"
    
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.get(url)
        if r.status_code != 200:
            raise HTTPException(502, f"TwelveData {r.status_code}")
        raw = r.json()

    result = []
    # Tek hisse dict, çok hisse dict of dicts döner
    items = raw if isinstance(raw, dict) and "symbol" not in raw else {STOCKS[0]: raw}

    for sym, item in items.items():
        try:
            if item.get("status") == "error":
                continue
            close   = float(item.get("close", 0) or 0)
            open_   = float(item.get("open", close) or close)
            chg     = float(item.get("change", 0) or 0)
            chg_pct = float(item.get("percent_change", 0) or 0)
            vol     = float(item.get("volume", 0) or 0)

            result.append({
                "symbol":                     sym + ".IS",
                "shortName":                  item.get("name", sym),
                "regularMarketPrice":         close,
                "regularMarketChange":        chg,
                "regularMarketChangePercent": chg_pct,
                "marketCap":                  close * vol if vol > 0 else 1e9,
                "regularMarketVolume":        vol,
                "fiftyTwoWeekLow":            float(item.get("fifty_two_week", {}).get("low", 0) or 0),
                "fiftyTwoWeekHigh":           float(item.get("fifty_two_week", {}).get("high", 0) or 0),
            })
        except:
            continue

    return {"data": [x for x in result if x["regularMarketPrice"] > 0]}

@app.get("/api/spark")
async def spark(period: str = "1d"):
    return {"data": []}

@app.get("/health")
def health():
    return {"status": "ok"}