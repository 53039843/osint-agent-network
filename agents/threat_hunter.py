import asyncio
import random
from typing import List, Dict, Any
from core.llm_client import LLMClient
from utils.ioc_extractor import extract_iocs
from utils.logger import setup_logger

logger = setup_logger("threat_hunter_agent")

MITRE_ATTACK_TECHNIQUES = {
    "T1566": "Phishing",
    "T1059": "Command and Scripting Interpreter",
    "T1078": "Valid Accounts",
    "T1190": "Exploit Public-Facing Application",
    "T1486": "Data Encrypted for Impact (Ransomware)",
    "T1071": "Application Layer Protocol (C2)",
    "T1027": "Obfuscated Files or Information",
    "T1055": "Process Injection",
    "T1003": "OS Credential Dumping",
    "T1021": "Remote Services (Lateral Movement)",
}

class ThreatHunterAgent:
    """
    Threat Hunter Agent: Proactively hunts for MITRE ATT&CK technique patterns
    within collected intelligence, enriching IoCs with TTP context.
    Operates as a secondary analysis pass after the main AnalyzerAgent.
    """
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = (
            "You are an expert threat hunter specializing in MITRE ATT&CK framework mapping. "
            "Given raw intelligence text, identify which ATT&CK techniques are referenced "
            "and extract associated IoCs. Return structured analysis."
        )

    async def _map_ttps(self, item: Dict[str, Any]) -> Dict[str, Any]:
        await asyncio.sleep(random.uniform(0.1, 0.4))
        content = item.get("content", "")

        # Fast regex-based IoC extraction first
        iocs = extract_iocs(content)

        # LLM-based TTP mapping
        user_prompt = f"Map MITRE ATT&CK techniques in this text:\n{content[:500]}"
        llm_response = await self.llm.generate_text(self.system_prompt, user_prompt)

        # Mock TTP detection based on keywords
        detected_ttps = []
        content_lower = content.lower()
        if any(kw in content_lower for kw in ["phish", "email", "attachment"]):
            detected_ttps.append("T1566")
        if any(kw in content_lower for kw in ["powershell", "bash", "cmd", "script"]):
            detected_ttps.append("T1059")
        if any(kw in content_lower for kw in ["encrypt", "ransom", "locked"]):
            detected_ttps.append("T1486")
        if any(kw in content_lower for kw in ["inject", "dll", "shellcode"]):
            detected_ttps.append("T1055")

        enriched = item.copy()
        enriched["iocs"] = iocs
        enriched["ttps"] = [
            {"id": t, "name": MITRE_ATTACK_TECHNIQUES.get(t, "Unknown")}
            for t in detected_ttps
        ]
        enriched["ttp_llm_analysis"] = llm_response
        return enriched

    async def hunt(self, analyzed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        logger.info(f"Threat hunting across {len(analyzed_data)} items for ATT&CK TTPs...")
        semaphore = asyncio.Semaphore(8)

        async def sem_hunt(item):
            async with semaphore:
                return await self._map_ttps(item)

        results = await asyncio.gather(*[sem_hunt(item) for item in analyzed_data])
        total_ttps = sum(len(r.get("ttps", [])) for r in results)
        logger.info(f"Threat hunt complete. Mapped {total_ttps} TTP instances.")
        return list(results)
