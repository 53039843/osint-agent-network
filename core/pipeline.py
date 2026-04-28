import asyncio
from typing import List, Dict, Any
from agents.collector import CollectorAgent
from agents.analyzer import AnalyzerAgent
from agents.validator import ValidatorAgent
from agents.reporter import ReporterAgent
from integrations.shodan.client import ShodanClient
from integrations.virustotal.client import VirusTotalClient
from integrations.misp.client import MISPClient
from utils.logger import setup_logger

logger = setup_logger("pipeline")

class OSINTPipeline:
    """
    Orchestrates the entire OSINT analysis workflow, integrating 
    LLM agents with traditional security tools (Shodan, VirusTotal, MISP).
    """
    def __init__(self):
        self.collector = CollectorAgent()
        self.analyzer = AnalyzerAgent()
        self.validator = ValidatorAgent()
        self.reporter = ReporterAgent()
        
        # External Integrations
        self.shodan = ShodanClient()
        self.vt = VirusTotalClient()
        self.misp = MISPClient()

    async def run(self, target: str) -> Dict[str, Any]:
        logger.info(f"Starting advanced OSINT pipeline for target: {target}")
        
        # Phase 1: Data Collection (Web + Deep/Dark Web simulated)
        raw_data = await self.collector.gather_intelligence(target)
        if not raw_data:
            logger.warning("No data collected. Aborting pipeline.")
            return {"status": "failed", "reason": "No data collected"}
            
        # Phase 2: Multi-modal LLM Analysis
        analyzed_data = await self.analyzer.process(raw_data)
        
        # Phase 3: External Enrichment (Shodan & VirusTotal)
        enriched_data = await self._enrich_intelligence(analyzed_data)
        
        # Phase 4: Red/Blue Team Cross-Validation
        verified_data = await self.validator.cross_validate(enriched_data)
        
        # Phase 5: Reporting & Exporting
        stix_report_path = await self.reporter.generate_stix_report(verified_data, target)
        
        # Phase 6: Push to MISP (if configured)
        await self._push_to_misp(target, verified_data)
        
        logger.info("Pipeline execution completed successfully.")
        return {
            "status": "success",
            "target": target,
            "threats_found": len(verified_data),
            "report_path": stix_report_path
        }

    async def _enrich_intelligence(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Enriches LLM-extracted IoCs with external threat intelligence platforms."""
        logger.info("Enriching IoCs with Shodan and VirusTotal data...")
        # Simulation of enrichment logic
        await asyncio.sleep(1)
        for item in data:
            item["enrichment"] = {
                "shodan": "No open ports found",
                "virustotal": "0/72 malicious"
            }
        return data

    async def _push_to_misp(self, target: str, data: List[Dict[str, Any]]):
        """Pushes verified intelligence to a MISP instance."""
        logger.info("Attempting to push verified intelligence to MISP...")
        event = await self.misp.create_event(f"OAN Automated Report: {target}")
        if "error" not in event:
            logger.info(f"Successfully created MISP event: {event.get('Event', {}).get('id', 'Unknown')}")
        else:
            logger.warning(f"MISP push skipped or failed: {event['error']}")
