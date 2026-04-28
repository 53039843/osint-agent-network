import pytest
import os
from integrations.shodan.client import ShodanClient
from integrations.virustotal.client import VirusTotalClient
from integrations.misp.client import MISPClient

os.environ["DEBUG_MODE"] = "true"

@pytest.mark.asyncio
async def test_shodan_returns_error_without_key():
    client = ShodanClient()
    result = await client.search_host("8.8.8.8")
    assert "error" in result

@pytest.mark.asyncio
async def test_virustotal_returns_error_without_key():
    client = VirusTotalClient()
    result = await client.get_domain_report("example.com")
    assert "error" in result

@pytest.mark.asyncio
async def test_misp_returns_error_without_key():
    client = MISPClient()
    result = await client.create_event("Test Event")
    assert "error" in result
