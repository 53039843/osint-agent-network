import aiohttp
from typing import Dict, Any, List
from utils.logger import setup_logger

logger = setup_logger("spiderfoot_client")

class SpiderFootClient:
    """
    Client for SpiderFoot HX REST API.
    SpiderFoot is an open-source OSINT automation tool that can scan targets
    across 200+ data sources.
    Ref: https://github.com/smicallef/spiderfoot
    """
    def __init__(self, base_url: str = "http://localhost:5001"):
        self.base_url = base_url

    async def start_scan(self, target: str, modules: List[str] = None) -> Dict[str, Any]:
        """Starts a new SpiderFoot scan for the given target."""
        url = f"{self.base_url}/startscan"
        payload = {
            "scanname": f"OAN_scan_{target}",
            "scantarget": target,
            "usecase": "all",
            "modulelist": ",".join(modules) if modules else "",
            "typelist": ""
        }
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, data=payload) as response:
                    if response.status == 200:
                        return await response.json()
                    return {"error": f"SpiderFoot returned {response.status}"}
            except aiohttp.ClientConnectorError:
                logger.warning("SpiderFoot instance not reachable. Is it running locally?")
                return {"error": "SpiderFoot not reachable. Start with: python sf.py -l 127.0.0.1:5001"}

    async def get_scan_results(self, scan_id: str) -> Dict[str, Any]:
        """Retrieves results for a completed scan."""
        url = f"{self.base_url}/scaneventresults"
        params = {"id": scan_id, "eventtype": "ALL"}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        return await response.json()
                    return {"error": f"SpiderFoot returned {response.status}"}
            except aiohttp.ClientConnectorError:
                return {"error": "SpiderFoot not reachable"}
