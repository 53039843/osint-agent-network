import aiohttp
import json
from typing import Dict, Any, List
from core.config import settings
from utils.logger import setup_logger

logger = setup_logger("webhook_notifier")

class WebhookNotifier:
    """
    Sends alerts to external systems (Slack, Teams, Discord, custom webhooks)
    when high-confidence threats are verified.
    """
    def __init__(self):
        self.webhook_url = getattr(settings, "ALERT_WEBHOOK_URL", None)

    async def send_alert(self, target: str, verified_intel: List[Dict[str, Any]], report_url: str):
        """Sends a summarized alert payload."""
        if not self.webhook_url:
            logger.debug("No webhook URL configured. Skipping alert.")
            return

        high_conf_count = sum(1 for item in verified_intel if item.get("confidence_score", 0) > 0.8)

        payload = {
            "text": f"🚨 **OSINT Alert: High-confidence threats verified for {target}**",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"Pipeline completed for target: *{target}*\n\n"
                                f"• Total verified threats: {len(verified_intel)}\n"
                                f"• High confidence threats (>80%): {high_conf_count}\n\n"
                                f"<{report_url}|View Full STIX Report>"
                    }
                }
            ]
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.webhook_url, json=payload) as resp:
                    if resp.status in (200, 201, 204):
                        logger.info(f"Successfully sent webhook alert for {target}")
                    else:
                        logger.warning(f"Webhook alert failed with status {resp.status}")
            except Exception as e:
                logger.error(f"Failed to send webhook: {e}")
