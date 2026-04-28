import aiohttp
from typing import Dict, Any, List
from core.config import settings
from utils.logger import setup_logger

logger = setup_logger("misp_client")

class MISPClient:
    """Async client for MISP (Malware Information Sharing Platform) integration."""
    def __init__(self):
        self.misp_url = settings.MISP_URL
        self.auth_key = settings.MISP_AUTH_KEY
        self.headers = {
            "Authorization": self.auth_key,
            "Accept": "application/json",
            "Content-Type": "application/json"
        }

    async def create_event(self, info: str, distribution: int = 0, threat_level_id: int = 3, analysis: int = 0) -> Dict[str, Any]:
        """Creates a new event in MISP."""
        if not self.auth_key:
            logger.warning("MISP auth key missing. Skipping event creation.")
            return {"error": "MISP auth key missing"}
            
        url = f"{self.misp_url}/events/add"
        payload = {
            "Event": {
                "info": info,
                "distribution": distribution,
                "threat_level_id": threat_level_id,
                "analysis": analysis
            }
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, headers=self.headers, json=payload, ssl=False) as response:
                    if response.status == 200:
                        return await response.json()
                    return {"error": f"MISP API returned {response.status}"}
            except Exception as e:
                logger.error(f"MISP connection error: {e}")
                return {"error": str(e)}

    async def add_attributes_to_event(self, event_id: str, attributes: List[Dict[str, str]]) -> Dict[str, Any]:
        """Adds IoCs to an existing MISP event."""
        if not self.auth_key:
            return {"error": "MISP auth key missing"}
            
        url = f"{self.misp_url}/attributes/add/{event_id}"
        results = []
        
        async with aiohttp.ClientSession() as session:
            for attr in attributes:
                try:
                    async with session.post(url, headers=self.headers, json=attr, ssl=False) as response:
                        if response.status == 200:
                            results.append(await response.json())
                        else:
                            results.append({"error": f"Failed to add attribute: {response.status}"})
                except Exception as e:
                    results.append({"error": str(e)})
                    
        return {"results": results}
