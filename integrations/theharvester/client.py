import asyncio
import subprocess
import json
from typing import Dict, Any, List
from utils.logger import setup_logger

logger = setup_logger("theharvester_client")

class TheHarvesterClient:
    """
    Wrapper for theHarvester CLI tool.
    theHarvester is used for gathering emails, subdomains, hosts, employee names,
    open ports and banners from different public sources.
    Ref: https://github.com/laramies/theHarvester
    
    Requires theHarvester to be installed:
        pip install theHarvester
    """
    def __init__(self):
        self.sources = ["google", "bing", "linkedin", "twitter", "github", "dnsdumpster", "crtsh"]

    async def harvest(self, domain: str, limit: int = 500) -> Dict[str, Any]:
        """
        Runs theHarvester against a target domain and returns structured results.
        """
        logger.info(f"Running theHarvester against domain: {domain}")
        
        results = {"domain": domain, "emails": [], "hosts": [], "ips": []}
        
        for source in self.sources:
            cmd = [
                "theHarvester",
                "-d", domain,
                "-l", str(limit),
                "-b", source,
                "-f", f"/tmp/theharvester_{domain}_{source}"
            ]
            
            try:
                # Run in a thread pool to avoid blocking the event loop
                loop = asyncio.get_event_loop()
                proc_result = await loop.run_in_executor(
                    None,
                    lambda: subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                )
                
                if proc_result.returncode == 0:
                    # Parse output (simplified)
                    output = proc_result.stdout
                    emails = [line.strip() for line in output.split('\n') if '@' in line and domain in line]
                    results["emails"].extend(emails)
                    logger.info(f"  [{source}] Found {len(emails)} emails.")
                else:
                    logger.warning(f"  [{source}] theHarvester exited with code {proc_result.returncode}")
                    
            except FileNotFoundError:
                logger.warning("theHarvester not found. Install with: pip install theHarvester")
                return {"error": "theHarvester not installed", "install": "pip install theHarvester"}
            except subprocess.TimeoutExpired:
                logger.warning(f"  [{source}] Timed out after 60s")
                
        # Deduplicate
        results["emails"] = list(set(results["emails"]))
        return results

    async def harvest_emails(self, domain: str) -> List[str]:
        """Convenience method to return only emails."""
        result = await self.harvest(domain)
        return result.get("emails", [])
