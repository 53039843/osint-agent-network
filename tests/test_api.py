import pytest
import os
os.environ["DEBUG_MODE"] = "true"

from httpx import AsyncClient
from app import app


@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_extract_iocs_from_text():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/iocs/extract",
            json={"text": "C2 server at 192.168.1.100. Hash: a3f5b2c1d4e6f7890a1b2c3d4e5f67890a1b2c3d4e5f67890a1b2c3d4e5f6789. CVE-2021-44228"}
        )
    assert response.status_code == 200
    data = response.json()
    assert "raw_iocs" in data
    assert data["total_count"] > 0


@pytest.mark.asyncio
async def test_extract_empty_text_returns_400():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/api/v1/iocs/extract",
            json={"text": ""}
        )
    assert response.status_code == 400
