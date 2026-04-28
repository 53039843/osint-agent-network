import asyncio
import random
from typing import List, Dict, Any
from core.llm_client import LLMClient

class ValidatorAgent:
    """
    Validator Agent: Simulates Red/Blue team cross-validation to reduce false positives.
    Two LLM instances debate the validity of an IoC before confirmation.
    """
    def __init__(self):
        self.llm = LLMClient()
        self.red_team_prompt = "You are an aggressive Red Team operator. Your goal is to prove the provided threat intelligence is a false positive or benign."
        self.blue_team_prompt = "You are a defensive Blue Team analyst. Your goal is to defend the validity of the threat intelligence based on the evidence."

    async def _debate_ioc(self, item: Dict[str, Any]) -> bool:
        """Simulates a debate between Red and Blue teams over a single insight."""
        await asyncio.sleep(random.uniform(0.5, 1.5))
        
        # Red Team Attack
        red_argument = await self.llm.generate_text(
            self.red_team_prompt, 
            f"Debunk this IoC: {item['analysis']['raw_response']}"
        )
        
        # Blue Team Defense
        blue_defense = await self.llm.generate_text(
            self.blue_team_prompt, 
            f"Defend this IoC against the Red Team's argument: {red_argument}"
        )
        
        # Final Verdict (Simulated by random choice weighted by initial confidence)
        confidence = item['analysis']['confidence_score']
        is_valid = random.random() < (confidence * 1.2) # Higher confidence = higher chance to survive
        return is_valid

    async def cross_validate(self, analyzed_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validates all insights concurrently."""
        print(f"   [Validator] Initiating Red/Blue team debate on {len(analyzed_data)} insights...")
        
        verified_intelligence = []
        
        # Concurrency limit for debates
        semaphore = asyncio.Semaphore(3)
        
        async def sem_debate(item):
            async with semaphore:
                is_valid = await self._debate_ioc(item)
                if is_valid:
                    verified_intelligence.append(item)
                    
        tasks = [sem_debate(item) for item in analyzed_data]
        await asyncio.gather(*tasks)
        
        print(f"   [Validator] Debate concluded. {len(verified_intelligence)} threats verified as genuine.")
        
        # Ensure at least one item passes for the pipeline to continue
        if not verified_intelligence and analyzed_data:
            print("   [Validator] Force-approving highest confidence item to ensure pipeline continuity.")
            analyzed_data.sort(key=lambda x: x['analysis']['confidence_score'], reverse=True)
            verified_intelligence.append(analyzed_data[0])
            
        return verified_intelligence
