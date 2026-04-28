import asyncio
import random
from typing import List, Dict, Any
from core.llm_client import LLMClient

class AnalyzerAgent:
    """
    Multi-modal Analyzer Agent: Uses LLMs (like Xiaomi MiMo) to parse images and text, 
    performing long-chain reasoning to extract Indicators of Compromise (IoCs).
    """
    def __init__(self):
        self.llm = LLMClient()
        self.system_prompt = (
            "You are an expert cybersecurity analyst. "
            "Extract potential Indicators of Compromise (IoCs), Tactics, Techniques, and Procedures (TTPs) "
            "from the provided text and images. Output structured JSON."
        )

    async def _analyze_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        """Analyzes a single item using the LLM client."""
        # Simulate processing time based on content length/type
        await asyncio.sleep(random.uniform(0.1, 0.5))
        
        insight = {}
        if item.get("image_url"):
            # Multi-modal reasoning for images
            user_prompt = f"Analyze this screenshot related to {item['content']} for malware signatures or C2 infrastructure."
            llm_response = await self.llm.analyze_image(self.system_prompt, item["image_url"], user_prompt)
            insight["type"] = "multi_modal_analysis"
        else:
            # Text-only reasoning
            user_prompt = f"Analyze the following text for threat intelligence: {item['content']}"
            llm_response = await self.llm.generate_text(self.system_prompt, user_prompt)
            insight["type"] = "text_analysis"
            
        insight["raw_response"] = llm_response
        insight["confidence_score"] = random.uniform(0.4, 0.99) # Mock confidence score
        
        # Combine original item with insights
        analyzed_item = item.copy()
        analyzed_item["analysis"] = insight
        return analyzed_item

    async def process(self, raw_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Processes raw data in batches to avoid rate limits."""
        print(f"   [Analyzer] Commencing multi-modal reasoning on {len(raw_data)} items...")
        
        # In a real scenario, we would filter out obvious noise before sending to LLM
        # For simulation, we randomly select a subset to analyze
        sample_size = max(5, len(raw_data) // 5)
        data_to_analyze = random.sample(raw_data, sample_size)
        
        # Process concurrently with a semaphore to limit concurrency
        semaphore = asyncio.Semaphore(5)
        
        async def sem_analyze(item):
            async with semaphore:
                return await self._analyze_item(item)
                
        tasks = [sem_analyze(item) for item in data_to_analyze]
        analyzed_results = await asyncio.gather(*tasks)
        
        # Filter out low confidence results
        high_value_insights = [res for res in analyzed_results if res["analysis"]["confidence_score"] > 0.7]
        
        print(f"   [Analyzer] Reasoning complete. Extracted {len(high_value_insights)} high-confidence IoCs.")
        return high_value_insights
