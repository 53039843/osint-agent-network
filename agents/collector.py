import asyncio
import random
import time
from typing import List, Dict, Any

class CollectorAgent:
    """
    Data Collection Agent: Scrapes forums, blogs, and social media for potential threat intelligence.
    Simulates asynchronous API calls to various OSINT sources.
    """
    def __init__(self, sources: List[str] = None):
        self.sources = sources or ["twitter_api", "reddit_api", "pastebin_scraper", "darkweb_forum"]
        
    async def fetch_from_source(self, source: str, target: str) -> List[Dict[str, Any]]:
        """Simulates fetching data from a single source."""
        await asyncio.sleep(random.uniform(0.5, 2.0)) # Simulate network latency
        
        # Generate mock data
        num_items = random.randint(10, 50)
        results = []
        for i in range(num_items):
            # 10% chance to include an image URL
            has_image = random.random() < 0.1
            item = {
                "id": f"{source}_{int(time.time())}_{i}",
                "source": source,
                "timestamp": int(time.time()) - random.randint(0, 86400),
                "content": f"Discussing {target} vulnerabilities and exploits. Payload found.",
                "author": f"user_{random.randint(1000, 9999)}",
                "image_url": f"https://example.com/malware_screenshot_{i}.png" if has_image else None
            }
            results.append(item)
        return results

    async def gather_intelligence(self, target: str) -> List[Dict[str, Any]]:
        """Gathers data from all configured sources concurrently."""
        print(f"   [Collector] Initiating parallel collection across {len(self.sources)} sources for '{target}'...")
        
        tasks = [self.fetch_from_source(source, target) for source in self.sources]
        results_lists = await asyncio.gather(*tasks)
        
        # Flatten the list of lists
        all_results = [item for sublist in results_lists for item in sublist]
        print(f"   [Collector] Collection complete. Retrieved {len(all_results)} raw items.")
        return all_results
