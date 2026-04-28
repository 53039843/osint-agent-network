import asyncio
import json
import os
import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any

class ReporterAgent:
    """
    Report Generation Agent: Aggregates verified intelligence and outputs STIX 2.1 compliant reports.
    """
    def __init__(self):
        self.report_dir = "/home/ubuntu/osint-agent-network/reports"
        os.makedirs(self.report_dir, exist_ok=True)

    def _create_stix_bundle(self, verified_intelligence: List[Dict[str, Any]], target: str) -> Dict[str, Any]:
        """Generates a STIX 2.1 Bundle containing Indicators and Observations."""
        bundle_id = f"bundle--{uuid.uuid4()}"
        
        objects = []
        for item in verified_intelligence:
            indicator_id = f"indicator--{uuid.uuid4()}"
            indicator = {
                "type": "indicator",
                "spec_version": "2.1",
                "id": indicator_id,
                "created": datetime.now(timezone.utc).isoformat() + "Z",
                "modified": datetime.now(timezone.utc).isoformat() + "Z",
                "name": f"Threat Intelligence for {target} from {item['source']}",
                "description": item['content'],
                "pattern": f"[file:hashes.'SHA-256' = '{uuid.uuid4().hex}']", # Mock pattern
                "pattern_type": "stix",
                "valid_from": datetime.now(timezone.utc).isoformat() + "Z",
                "labels": ["malicious-activity"]
            }
            objects.append(indicator)
            
        bundle = {
            "type": "bundle",
            "id": bundle_id,
            "objects": objects
        }
        return bundle

    async def generate_stix_report(self, verified_intelligence: List[Dict[str, Any]], target: str) -> str:
        """Saves the STIX bundle to a JSON file."""
        print(f"   [Reporter] Compiling {len(verified_intelligence)} verified threats into STIX 2.1 format...")
        
        bundle = self._create_stix_bundle(verified_intelligence, target)
        
        filename = f"stix_report_{target.replace(' ', '_')}_{int(datetime.now().timestamp())}.json"
        filepath = os.path.join(self.report_dir, filename)
        
        # Simulate disk I/O and processing
        await asyncio.sleep(0.5)
        
        with open(filepath, 'w') as f:
            json.dump(bundle, f, indent=4)
            
        print(f"   [Reporter] STIX report saved successfully to {filepath}")
        return filepath
