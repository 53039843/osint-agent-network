import aiohttp
import base64
from typing import Dict, Any, List
from core.config import settings
from utils.logger import setup_logger

logger = setup_logger("censys_client")

class CensysClient:
    """
    Async client for Censys Search API v2.
    Censys continuously scans the entire internet and provides
    detailed data on hosts, certificates, and websites.
    Ref: https://search.censys.io/api
    """
    def __init__(self):
        self.api_id = settings.CENSYS_API_ID
        self.api_secret = settings.CENSYS_API_SECRET
        self.base_url = "https://search.censys.io/api/v2"

        credentials = f"{self.api_id}:{self.api_secret}"
        self.auth_header = "Basic " + base64.b64encode(credentials.encode()).decode()
        self.headers = {
            "Authorization": self.auth_header,
            "Content-Type": "application/json"
        }

    async def search_hosts(self, query: str, per_page: int = 25) -> Dict[str, Any]:
        """Searches Censys for hosts matching the given query."""
        if not self.api_id or not self.api_secret:
            return {"error": "Censys API credentials missing"}

        url = f"{self.base_url}/hosts/search"
        payload = {"q": query, "per_page": per_page}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=self.headers, json=payload) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return {"error": f"Censys returned {resp.status}"}
            except Exception as e:
                logger.error(f"Censys search error: {e}")
                return {"error": str(e)}

    async def get_host(self, ip: str) -> Dict[str, Any]:
        """Retrieves detailed information about a specific host IP."""
        if not self.api_id:
            return {"error": "Censys API credentials missing"}

        url = f"{self.base_url}/hosts/{ip}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return {"error": f"Censys returned {resp.status}"}
            except Exception as e:
                return {"error": str(e)}
