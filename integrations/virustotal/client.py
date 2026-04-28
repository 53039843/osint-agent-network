import aiohttp
from typing import Dict, Any
from core.config import settings

class VirusTotalClient:
    """Async client for VirusTotal v3 API."""
    def __init__(self):
        self.api_key = settings.VIRUSTOTAL_API_KEY
        self.base_url = "https://www.virustotal.com/api/v3"
        self.headers = {"x-apikey": self.api_key}

    async def get_file_report(self, file_hash: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"error": "VirusTotal API key missing"}
            
        url = f"{self.base_url}/files/{file_hash}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    return {"error": f"VirusTotal API returned {response.status}"}
            except Exception as e:
                return {"error": str(e)}

    async def get_domain_report(self, domain: str) -> Dict[str, Any]:
        if not self.api_key:
            return {"error": "VirusTotal API key missing"}
            
        url = f"{self.base_url}/domains/{domain}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as response:
                    if response.status == 200:
                        return await response.json()
                    return {"error": f"VirusTotal API returned {response.status}"}
            except Exception as e:
                return {"error": str(e)}
