import os
from pydantic import BaseModel, Field

class Settings(BaseModel):
    # LLM Settings
    MIMO_API_KEY: str = Field(default_factory=lambda: os.getenv("MIMO_API_KEY", ""))
    MIMO_BASE_URL: str = Field(default="https://api.xiaomimimo.com/v1")
    MIMO_MODEL: str = Field(default="mimo-v2.5-multimodal")
    
    # App Settings
    DEBUG_MODE: bool = Field(default_factory=lambda: os.getenv("DEBUG_MODE", "false").lower() == "true")
    MAX_RETRIES: int = Field(default=3)
    
    # OSINT Settings
    SOURCES: list[str] = Field(default=["twitter", "reddit", "hacker_news", "pastebin"])
    TARGET_KEYWORDS: list[str] = Field(default=[])

settings = Settings()
