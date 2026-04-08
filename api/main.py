from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

HEADERS = {"User-Agent": "Mozilla/5.0"}

STOCKS = [
    "THYAO","GARAN","AKBNK","YKBNK","SISE","KCHOL","SAHOL","TCELL",
    "BIMAS","ASELS","FROTO","TOASO","TUPRS","ARCLK","EREGL","PETKM",
    "ENKAI","SODA","KOZAL","KOZAA","MAVI","CCOLA","TTKOM","PGSUS",
    "TAVHL","MGROS","ULKER","DOHOL","EKGYO","ISCTR","HALKB","VAKBN",
    "LOGO","AEFES","OTKAR","TRKCM","VESTL","GUBRF","DOAS","HEKTS",
]

@app.get("/api/quotes")
async def quotes():
    syms = ",".join(s + ".IS" for s in STOCKS)
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={syms}"
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.get(url, headers=HEADERS)
        if r.status_code != 200:
            raise HTTPException(502, "Yahoo error")
    return {"data": r.json().get("quoteResponse", {}).get("result", [])}

@app.get("/api/spark")
async def spark(period: str = "1d"):
    MAP = {"1d":("1d","5m"),"5d":("5d","1d"),"1mo":("1mo","1d"),"3mo":("3mo","1wk"),"ytd":("ytd","1mo")}
    rng, itv = MAP.get(period, ("1d","5m"))
    syms = ",".join(s + ".IS" for s in STOCKS)
    url = f"https://query1.finance.yahoo.com/v8/finance/spark?symbols={syms}&range={rng}&interval={itv}"
    async with httpx.AsyncClient(timeout=20) as c:
        r = await c.get(url, headers=HEADERS)
        if r.status_code != 200:
            raise HTTPException(502, "Yahoo error")
    return {"data": r.json().get("spark", {}).get("result", [])}

@app.get("/health")
async def health():
    return {"status": "ok"}