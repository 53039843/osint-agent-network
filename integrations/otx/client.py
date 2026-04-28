import aiohttp
from typing import Dict, Any, List
from core.config import settings
from utils.logger import setup_logger

logger = setup_logger("otx_client")

class OTXClient:
    """
    Async client for AlienVault OTX (Open Threat Exchange) API.
    OTX is the world's largest open threat intelligence community,
    providing free access to a global map of threats.
    Ref: https://otx.alienvault.com/api
    """
    def __init__(self):
        self.api_key = settings.OTX_API_KEY
        self.base_url = "https://otx.alienvault.com/api/v1"
        self.headers = {"X-OTX-API-KEY": self.api_key}

    async def get_indicator(self, indicator_type: str, indicator: str, section: str = "general") -> Dict[str, Any]:
        """
        Retrieves threat intelligence for a given indicator.
        indicator_type: IPv4, domain, hostname, url, FileHash-MD5, FileHash-SHA256, CVE
        """
        if not self.api_key:
            return {"error": "OTX API key missing"}

        url = f"{self.base_url}/indicators/{indicator_type}/{indicator}/{section}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return {"error": f"OTX returned {resp.status}"}
            except Exception as e:
                logger.error(f"OTX error for {indicator}: {e}")
                return {"error": str(e)}

    async def search_pulses(self, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Searches OTX pulses (threat reports) by keyword."""
        if not self.api_key:
            return [{"error": "OTX API key missing"}]

        url = f"{self.base_url}/search/pulses"
        params = {"q": query, "limit": limit}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("results", [])
                    return [{"error": f"OTX returned {resp.status}"}]
            except Exception as e:
                logger.error(f"OTX pulse search error: {e}")
                return [{"error": str(e)}]

    async def get_pulse_details(self, pulse_id: str) -> Dict[str, Any]:
        """Retrieves full details of a specific OTX pulse."""
        if not self.api_key:
            return {"error": "OTX API key missing"}

        url = f"{self.base_url}/pulses/{pulse_id}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return {"error": f"OTX returned {resp.status}"}
            except Exception as e:
                return {"error": str(e)}
