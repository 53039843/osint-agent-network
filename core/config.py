import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    # LLM
    MIMO_API_KEY: str = Field(default_factory=lambda: os.getenv("MIMO_API_KEY", ""))
    MIMO_BASE_URL: str = Field(default="https://api.xiaomimimo.com/v1")
    MIMO_MODEL: str = Field(default="mimo-v2.5-multimodal")

    # Database
    DATABASE_URL: str = Field(
        default_factory=lambda: os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./oan.db")
    )

    # Redis / Celery
    REDIS_URL: str = Field(
        default_factory=lambda: os.getenv("REDIS_URL", "redis://localhost:6379/0")
    )

    # OSINT Integrations
    SHODAN_API_KEY: str = Field(default_factory=lambda: os.getenv("SHODAN_API_KEY", ""))
    VIRUSTOTAL_API_KEY: str = Field(default_factory=lambda: os.getenv("VIRUSTOTAL_API_KEY", ""))
    MISP_URL: str = Field(default_factory=lambda: os.getenv("MISP_URL", "https://misp.local"))
    MISP_AUTH_KEY: str = Field(default_factory=lambda: os.getenv("MISP_AUTH_KEY", ""))
    ABUSEIPDB_API_KEY: str = Field(default_factory=lambda: os.getenv("ABUSEIPDB_API_KEY", ""))
    OTX_API_KEY: str = Field(default_factory=lambda: os.getenv("OTX_API_KEY", ""))
    CENSYS_API_ID: str = Field(default_factory=lambda: os.getenv("CENSYS_API_ID", ""))
    CENSYS_API_SECRET: str = Field(default_factory=lambda: os.getenv("CENSYS_API_SECRET", ""))
    GREYNOISE_API_KEY: str = Field(default_factory=lambda: os.getenv("GREYNOISE_API_KEY", ""))

    # App
    DEBUG_MODE: bool = Field(
        default_factory=lambda: os.getenv("DEBUG_MODE", "false").lower() == "true"
    )
    MAX_RETRIES: int = Field(default=3)
    SOURCES: list[str] = Field(default=["twitter", "reddit", "hacker_news", "pastebin"])
    TARGET_KEYWORDS: list[str] = Field(default=[])

settings = Settings()
