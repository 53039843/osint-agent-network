from typing import List, Dict, Any
from core.llm_client import LLMClient
from utils.logger import setup_logger

logger = setup_logger("summarizer_agent")

class SummarizerAgent:
    """
    Summarizer Agent: Takes verified intelligence and produces a concise
    executive-level threat briefing in natural language.
    Designed to be consumed by non-technical stakeholders.
    """
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = (
            "You are a senior threat intelligence analyst writing an executive briefing. "
            "Summarize the provided threat intelligence data into a concise, clear, and actionable report. "
            "Use plain language. Avoid jargon. Highlight the most critical threats and recommended mitigations."
        )

    async def summarize(self, verified_intelligence: List[Dict[str, Any]], target: str) -> str:
        logger.info(f"Generating executive summary for target: {target}")

        intel_text = "\n".join([
            f"- Source: {item.get('source', 'unknown')} | "
            f"Content: {item.get('content', '')[:200]} | "
            f"Confidence: {item.get('analysis', {}).get('confidence_score', 0):.2f}"
            for item in verified_intelligence
        ])

        user_prompt = (
            f"Target: {target}\n\n"
            f"Verified Threat Intelligence ({len(verified_intelligence)} items):\n"
            f"{intel_text}\n\n"
            "Write a 3-paragraph executive briefing covering: "
            "(1) threat overview, (2) key IoCs and TTPs, (3) recommended mitigations."
        )

        summary = await self.llm.generate_text(self.system_prompt, user_prompt)
        logger.info("Executive summary generated successfully.")
        return summary
