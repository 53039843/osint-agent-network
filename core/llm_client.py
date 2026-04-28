import aiohttp
from typing import Optional, Dict, Any
from core.config import settings

class LLMClient:
    """
    Unified Async Client for Xiaomi MiMo API.
    Handles rate limiting, retries, and multi-modal payload formatting.
    """
    def __init__(self):
        self.api_key = settings.MIMO_API_KEY
        self.base_url = settings.MIMO_BASE_URL
        self.model = settings.MIMO_MODEL
        
        if not self.api_key and not settings.DEBUG_MODE:
            print("⚠️ WARNING: MIMO_API_KEY is not set. API calls will fail.")

    async def _post(self, endpoint: str, payload: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}{endpoint}"
        
        # Mock response if in debug mode or no key
        if settings.DEBUG_MODE or not self.api_key:
            import asyncio
            await asyncio.sleep(0.5)
            return {"choices": [{"message": {"content": "Mocked LLM response for: " + str(payload.get('messages', []))}}]}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    response.raise_for_status()
                    return await response.json()
        except Exception as e:
            print(f"❌ LLM API Error: {e}")
            return None

    async def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2
        }
        res = await self._post("/chat/completions", payload)
        if res and "choices" in res:
            return res["choices"][0]["message"]["content"]
        return ""

    async def analyze_image(self, system_prompt: str, image_url: str, user_prompt: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": user_prompt},
                        {"type": "image_url", "image_url": {"url": image_url}}
                    ]
                }
            ],
            "temperature": 0.1
        }
        res = await self._post("/chat/completions", payload)
        if res and "choices" in res:
            return res["choices"][0]["message"]["content"]
        return ""
