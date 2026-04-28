import aiohttp
from typing import Dict, Any
from core.config import settings
from utils.logger import setup_logger

logger = setup_logger("abuseipdb_client")

class AbuseIPDBClient:
    """
    Async client for AbuseIPDB API v2.
    AbuseIPDB is a project dedicated to helping combat the spread of hackers,
    spammers, and abusive activity on the internet.
    Ref: https://www.abuseipdb.com/api.html
    """
    def __init__(self):
        self.api_key = settings.ABUSEIPDB_API_KEY
        self.base_url = "https://api.abuseipdb.com/api/v2"
        self.headers = {
            "Key": self.api_key,
            "Accept": "application/json"
        }

    async def check_ip(self, ip: str, max_age_days: int = 90) -> Dict[str, Any]:
        """
        Checks an IP address against the AbuseIPDB database.
        Returns abuse confidence score (0-100) and report count.
        """
        if not self.api_key:
            return {"error": "AbuseIPDB API key missing"}

        url = f"{self.base_url}/check"
        params = {"ipAddress": ip, "maxAgeInDays": max_age_days, "verbose": ""}

        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        result = data.get("data", {})
                        logger.info(
                            f"AbuseIPDB: {ip} → score={result.get('abuseConfidenceScore')}%, "
                            f"reports={result.get('totalReports')}"
                        )
                        return result
                    return {"error": f"AbuseIPDB returned {resp.status}"}
            except Exception as e:
                logger.error(f"AbuseIPDB error for {ip}: {e}")
                return {"error": str(e)}

    async def bulk_check(self, ips: list) -> Dict[str, Any]:
        """Checks multiple IPs concurrently."""
        import asyncio
        tasks = [self.check_ip(ip) for ip in ips]
        results = await asyncio.gather(*tasks)
        return dict(zip(ips, results))
