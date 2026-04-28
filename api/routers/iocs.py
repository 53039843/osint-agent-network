from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from utils.ioc_extractor import extract_iocs, defang_ioc
from integrations.virustotal.client import VirusTotalClient
from integrations.abuseipdb.client import AbuseIPDBClient
from integrations.greynoise.client import GreyNoiseClient
from utils.logger import setup_logger
import asyncio

logger = setup_logger("api_iocs")
router = APIRouter(prefix="/api/v1/iocs", tags=["IoC Lookup"])


class TextExtractRequest(BaseModel):
    text: str


class IPLookupRequest(BaseModel):
    ip: str


@router.post("/extract", summary="Extract IoCs from raw text")
async def extract_from_text(request: TextExtractRequest):
    """
    Runs regex-based IoC extraction on the provided text.
    Returns all detected IPs, domains, hashes, CVEs, emails, etc.
    """
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    iocs = extract_iocs(request.text)
    defanged = {
        ioc_type: [defang_ioc(i) for i in items]
        for ioc_type, items in iocs.items()
    }

    return {
        "raw_iocs": iocs,
        "defanged_iocs": defanged,
        "total_count": sum(len(v) for v in iocs.values())
    }


@router.post("/enrich/ip", summary="Enrich an IP address across multiple threat intel sources")
async def enrich_ip(request: IPLookupRequest):
    """
    Queries AbuseIPDB, GreyNoise, and VirusTotal concurrently for a given IP.
    """
    ip = request.ip.strip()
    if not ip:
        raise HTTPException(status_code=400, detail="IP address cannot be empty")

    logger.info(f"Enriching IP: {ip}")

    vt = VirusTotalClient()
    abuse = AbuseIPDBClient()
    gn = GreyNoiseClient()

    vt_result, abuse_result, gn_result = await asyncio.gather(
        vt.get_domain_report(ip),
        abuse.check_ip(ip),
        gn.quick_check(ip)
    )

    return {
        "ip": ip,
        "virustotal": vt_result,
        "abuseipdb": abuse_result,
        "greynoise": gn_result
    }
