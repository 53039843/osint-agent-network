from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import scans, iocs

app = FastAPI(
    title="OSINT Agent Network API",
    description=(
        "Production-grade REST API for the Multi-Agent OSINT analysis system. "
        "Powered by Xiaomi MiMo V2.5 with integrations for Shodan, VirusTotal, "
        "AbuseIPDB, GreyNoise, AlienVault OTX, Censys, and MISP."
    ),
    version="0.3.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scans.router)
app.include_router(iocs.router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "version": "0.3.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
