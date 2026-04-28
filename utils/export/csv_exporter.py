import csv
import os
from datetime import datetime
from typing import List, Dict, Any
from utils.logger import setup_logger

logger = setup_logger("csv_exporter")

def export_to_csv(verified_intel: List[Dict[str, Any]], target: str, output_dir: str = "reports") -> str:
    """
    Exports verified intelligence into a flat CSV format for easy import
    into SIEMs or Excel analysis.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_target = target.replace(" ", "_").lower()
    filepath = os.path.join(output_dir, f"intel_{safe_target}_{timestamp}.csv")

    headers = [
        "Target", "Source", "Confidence", "Content_Snippet",
        "IoCs", "MITRE_TTPs", "Enrichment_Summary", "Author"
    ]

    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()

        for item in verified_intel:
            iocs_str = ", ".join(f"{k}:{v}" for k, v in item.get("iocs", {}).items())
            ttps_str = ", ".join(t.get("id", "") for t in item.get("ttps", []))
            enrich_str = str(item.get("enrichment", {}))[:100]

            row = {
                "Target": target,
                "Source": item.get("source", "unknown"),
                "Confidence": round(item.get("analysis", {}).get("confidence_score", 0.0), 2),
                "Content_Snippet": item.get("content", "")[:150].replace("\n", " "),
                "IoCs": iocs_str,
                "MITRE_TTPs": ttps_str,
                "Enrichment_Summary": enrich_str,
                "Author": item.get("author", "unknown")
            }
            writer.writerow(row)

    logger.info(f"CSV export completed: {filepath}")
    return filepath
