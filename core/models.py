from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any
from datetime import datetime

class RawIntelligence(BaseModel):
    id: str
    source: str
    timestamp: int
    content: str
    author: str
    image_url: Optional[HttpUrl] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AnalysisInsight(BaseModel):
    type: str
    raw_response: str
    confidence_score: float
    iocs: List[str] = Field(default_factory=list)
    ttps: List[str] = Field(default_factory=list)

class AnalyzedIntelligence(RawIntelligence):
    analysis: AnalysisInsight

class VerifiedIntelligence(AnalyzedIntelligence):
    verified_by: str = "red_blue_team_debate"
    verification_timestamp: datetime = Field(default_factory=datetime.utcnow)
    debate_summary: str = ""
