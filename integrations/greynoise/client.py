import aiohttp
from typing import Dict, Any
from core.config import settings
from utils.logger import setup_logger

logger = setup_logger("greynoise_client")

class GreyNoiseClient:
    """
    Async client for GreyNoise API.
    GreyNoise collects and analyzes data on IPs that scan the internet,
    helping analysts filter out background noise from real threats.
    Ref: https://docs.greynoise.io/reference/get_v3-community-ip
    """
    def __init__(self):
        self.api_key = settings.GREYNOISE_API_KEY
        self.base_url = "https://api.greynoise.io/v3"
        self.headers = {
            "key": self.api_key,
            "Accept": "application/json"
        }

    async def quick_check(self, ip: str) -> Dict[str, Any]:
        """
        Quick check: determines if an IP is internet background noise.
        Returns: noise (bool), riot (bool), classification (benign/malicious/unknown)
        """
        if not self.api_key:
            return {"error": "GreyNoise API key missing"}

        url = f"{self.base_url}/community/{ip}"
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        logger.info(
                            f"GreyNoise: {ip} → noise={data.get('noise')}, "
                            f"classification={data.get('classification', 'unknown')}"
                        )
                        return data
                    elif resp.status == 404:
                        return {"ip": ip, "noise": False, "riot": False, "classification": "unknown"}
                    return {"error": f"GreyNoise returned {resp.status}"}
            except Exception as e:
                logger.error(f"GreyNoise error for {ip}: {e}")
                return {"error": str(e)}

    async def context(self, ip: str) -> Dict[str, Any]:
        """Full context lookup for an IP (requires paid plan)."""
        if not self.api_key:
            return {"error": "GreyNoise API key missing"}

        url = f"{self.base_url}/gnql/stats"
        params = {"query": f"ip:{ip}"}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=self.headers, params=params) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return {"error": f"GreyNoise returned {resp.status}"}
            except Exception as e:
                return {"error": str(e)}
