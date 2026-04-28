import pytest
import os
os.environ["DEBUG_MODE"] = "true"

from agents.analyzer import AnalyzerAgent
from agents.validator import ValidatorAgent
from agents.summarizer import SummarizerAgent
from agents.threat_hunter import ThreatHunterAgent

MOCK_RAW_DATA = [
    {
        "id": f"mock_{i}",
        "source": "reddit",
        "timestamp": 1714291200,
        "content": f"APT29 using PowerShell to inject shellcode into lsass.exe. C2 at 198.51.100.{i}",
        "author": f"user_{i}",
        "image_url": None
    }
    for i in range(10)
]

MOCK_ANALYZED_DATA = [
    {
        **item,
        "analysis": {
            "type": "text_analysis",
            "raw_response": "Detected T1055 Process Injection and T1059 PowerShell usage.",
            "confidence_score": 0.85
        }
    }
    for item in MOCK_RAW_DATA
]


@pytest.mark.asyncio
async def test_analyzer_returns_list():
    agent = AnalyzerAgent()
    result = await agent.process(MOCK_RAW_DATA)
    assert isinstance(result, list)


@pytest.mark.asyncio
async def test_analyzer_filters_low_confidence():
    agent = AnalyzerAgent()
    result = await agent.process(MOCK_RAW_DATA)
    for item in result:
        assert item["analysis"]["confidence_score"] > 0.7


@pytest.mark.asyncio
async def test_validator_returns_nonempty():
    agent = ValidatorAgent()
    result = await agent.cross_validate(MOCK_ANALYZED_DATA)
    assert len(result) >= 1


@pytest.mark.asyncio
async def test_summarizer_returns_string():
    agent = SummarizerAgent()
    summary = await agent.summarize(MOCK_ANALYZED_DATA[:3], "APT29")
    assert isinstance(summary, str)
    assert len(summary) > 0


@pytest.mark.asyncio
async def test_threat_hunter_maps_ttps():
    agent = ThreatHunterAgent()
    result = await agent.hunt(MOCK_ANALYZED_DATA[:5])
    assert len(result) == 5
    for item in result:
        assert "ttps" in item
        assert "iocs" in item
