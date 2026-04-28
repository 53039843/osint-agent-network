import pytest
from agents.collector import CollectorAgent

@pytest.mark.asyncio
async def test_collector_initialization():
    agent = CollectorAgent(sources=["test_source_1", "test_source_2"])
    assert len(agent.sources) == 2
    assert "test_source_1" in agent.sources

@pytest.mark.asyncio
async def test_gather_intelligence():
    agent = CollectorAgent(sources=["mock_twitter"])
    results = await agent.gather_intelligence("APT32")
    
    assert isinstance(results, list)
    assert len(results) > 0
    assert "source" in results[0]
    assert results[0]["source"] == "mock_twitter"
    assert "content" in results[0]
