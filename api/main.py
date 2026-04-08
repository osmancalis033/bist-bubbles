from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio

app = FastAPI(title="BIST Bubbles API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

YAHOO_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json",
}

STOCKS = [
    "THYAO","GARAN","AKBNK","YKBNK","SISE","KCHOL","SAHOL","TCELL",
    "BIMAS","ASELS","FROTO","TOASO","TUPRS","ARCLK","EREGL","PETKM",
    "ENKAI","SODA","KOZAL","KOZAA","MAVI","CCOLA","TTKOM","PGSUS",
    "TAVHL","MGROS","ULKER","DOHOL","EKGYO","ISCTR","HALKB","VAKBN",
    "LOGO","AEFES","OTKAR","TRKCM","VESTL","GUBRF","DOAS","HEKTS",
    "ANACM","ALARK","BRSAN","CIMSA","KORDS","NETAS","ZRGYO","KONTR",
    "KERVT","METRO","SELEC","SMRTG","ISGYO","TSKB","SASA","TURSG",
    "KCAER","EGEEN","CANTE","GLYHO","INDES","KAREL","PAPIL","TMSN",
]

def is_suffix(sym: str) -> str:
    return sym if sym.endswith(".IS") else sym + ".IS"

@app.get("/api/quotes")
async def get_quotes():
    symbols = ",".join(is_suffix(s) for s in STOCKS)
    fields = (
        "regularMarketPrice,regularMarketChangePercent,regularMarketChange,"
        "marketCap,regularMarketVolume,fiftyTwoWeekLow,fiftyTwoWeekHigh,"
        "shortName,fiftyTwoWeekChangePercent"
    )
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbols}&fields={fields}"

    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, headers=YAHOO_HEADERS)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Yahoo Finance error")
        data = r.json()

    results = data.get("quoteResponse", {}).get("result", [])
    return {"data": results, "count": len(results)}


@app.get("/api/spark")
async def get_spark(period: str = "1d"):
    PERIOD_MAP = {
        "1d":  ("1d",  "5m"),
        "5d":  ("5d",  "1d"),
        "1mo": ("1mo", "1d"),
        "3mo": ("3mo", "1wk"),
        "ytd": ("ytd", "1mo"),
    }
    if period not in PERIOD_MAP:
        raise HTTPException(status_code=400, detail="Invalid period")

    range_, interval = PERIOD_MAP[period]
    symbols = ",".join(is_suffix(s) for s in STOCKS)
    url = f"https://query1.finance.yahoo.com/v8/finance/spark?symbols={symbols}&range={range_}&interval={interval}"

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(url, headers=YAHOO_HEADERS)
        if r.status_code != 200:
            raise HTTPException(status_code=502, detail="Yahoo Finance error")
        data = r.json()

    results = data.get("spark", {}).get("result", [])
    return {"data": results}


@app.get("/health")
async def health():
    return {"status": "ok"}
