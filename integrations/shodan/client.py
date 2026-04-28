import aiohttp
from typing import Dict, Any
from core.config import settings

class ShodanClient:
    """Async client for Shodan API."""
    def __init__(self):
        self.api_key = settings.SHODAN_API_KEY
        self.base_url = "https://api.shodan.io"

    async def search_host(self, ip: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"error": "Shodan API key missing"}
            
        url = f"{self.base_url}/shodan/host/{ip}?key={self.api_key}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    return {"error": f"Shodan API returned {response.status}"}
            except Exception as e:
                return {"error": str(e)}

    async def search_query(self, query: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"error": "Shodan API key missing"}
            
        url = f"{self.base_url}/shodan/host/search?key={self.api_key}&query={query}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.json()
                    return {"error": f"Shodan API returned {response.status}"}
            except Exception as e:
                return {"error": str(e)}
